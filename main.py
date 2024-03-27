
import functions

client, model = functions.setup()

class DiscordPerson:
    def __init__(self, name, guild):
        self.TimesMocked = 0
        self.name = name
        self.IsBeingMocked = False
        self.ShouldMock = False
        self.guild = guild
    def UpdateMock(self):
        if self.IsBeingMocked == True:
            self.ShouldMock = True
            if self.TimesMocked + 1 % 3 == 0:
                self.ShouldMock = False
                self.IsBeingMocked = False
            else:
                self.TimesMocked += 1

    def ReturnStats(self):
        return vars(self)

def CheckIfCommandIsValid(message):
    Regmsg = message.content.lower().split(' ')
    if len(Regmsg) < 3:
        return False
    return True

@client.event
async def on_ready():
    global MemberNameTags
    print(f'logged in as {client.user}\n')
    MemberNameTags = []
    for server in client.guilds:
        for member in server.members:
            MemberNameTags.append((str(member.name).lower() + '@' + str(member.guild.name).lower()))

    for i in range(len(MemberNameTags)):
        globals()[f'{MemberNameTags[i]}'] = DiscordPerson(*MemberNameTags[i].split('@'))




@client.event
async def on_message(message):
    global MemberNameTags
    Regmsg = message.content.lower().split(' ')
    send = message.channel.send
    if message.author == client.user:
        return
    print(f'{message.author.name}\n{message.content}')
    if Regmsg[0] in ['$bb', '$betterbot']:

        if not CheckIfCommandIsValid(message):
            await send('Invalid command, please enter a proper command')
            return
        if Regmsg[1] in ['dict', 'dictionary', 'define']:
            await send(functions.ReturnDefinition(Regmsg[2]))

        if Regmsg[1] == 'ai':
            await send(functions.GenerateAiResponse([' '.join(str(x) for x in Regmsg[2:])][0], model))

        if Regmsg[1] == 'say':
            content = [' '.join(str(x) for x in Regmsg[2:])][0]
            await send(content)
            return
        if Regmsg[1] == 'mock':
            try:
                globals()[MemberNameTags]
            except:
                print(message.author.guild)
                ValidUsers = []
                for i in MemberNameTags:
                    if i.split('@')[1] == str(message.author.guild).lower():
                        ValidUsers.append(i.split('@')[0])

                await send(f'Invalid user to mock, valid people are:\n{ValidUsers}')

client.run()
