import discord

import functions
from dotenv import load_dotenv
import os
import amogus.handler as amogus
import uwu as uwu

load_dotenv()

client, model = functions.setup()

prefixes = ['$bb', '$betterbot']

class DiscordPerson:
    def __init__(self, name, guild):
        self.TimesMocked = 0
        self.name = name
        self.ShouldMock = False
        self.guild = guild
    def UpdateMock(self):
        self.TimesMocked += 1
        if (self.TimesMocked + 1) % 4 == 0:
            self.ShouldMock = False


    def ReturnStats(self):
        return vars(self)

# This code runs once the bot logs into the server(s)
@client.event
async def on_ready():
    # Make the user name tags global
    global MemberNameTags

    # Condfirmation on login
    print(f'logged in as {client.user}\n')

    # Generate usernames in the format "NAME@SERVER" all lowercase
    MemberNameTags = []
    for server in client.guilds:
        for member in server.members:
            MemberNameTags.append((str(member.name).lower() + '@' + str(member.guild.name).lower()))

    # Create global variables of all users with the DiscordPerson class
    for i in range(len(MemberNameTags)):
        globals()[f'{MemberNameTags[i]}'] = DiscordPerson(*MemberNameTags[i].split('@'))

# This will run every time a message is sent
@client.event
async def on_message(message):

    # This variable has the "name tags" for all of the user's DiscordPerson class
    global MemberNameTags

    # Converts the input into usable chunks
    Regmsg = message.content.lower().split(' ')

    # Shorthand for message.channel.send()
    send = message.channel.send

    # This will make the bot not talk to itself
    if message.author == client.user:
        return
    print(f'{message.author.name}\n{message.content}')

    # This will check if a user should be mocked
    if globals()[str(message.author.name).lower() + '@' + str(message.author.guild).lower()].ShouldMock:
        globals()[str(message.author.name).lower() + '@' + str(message.author.guild).lower()].UpdateMock()
        await send(functions.ScrambleLetters(message.content))

    # This will only run when the message starts with $bb or $betterbot
    if Regmsg[0] in prefixes:

        # Makes sure that the command has the prefix "$bb", a command "stats, mock, etc" and an argument, like user or word
        if not functions.CheckIfCommandIsValid(message):
            await send('Invalid command, please enter a proper command')
            return

        # Return definition of the given word
        if Regmsg[1] in ['dict', 'dictionary', 'define']:
            await send(functions.ReturnDefinition(Regmsg[2]))

        # Will generate an AI response with the user's prompt
        if Regmsg[1] == 'ai':
            await send(functions.GenerateAiResponse([' '.join(str(x) for x in Regmsg[2:])][0], model))

        # Will just copy what the user's message is
        if Regmsg[1] == 'say':
            content = [' '.join(str(x) for x in Regmsg[2:])][0]
            await send(content)
            return

        # Will initialize the mocking procedure
        # This will set the user's .ShouldMock attribute to true, and while
        # It is true, the bot will "mock" the user
        if Regmsg[1] == 'mock':
            try:
                # Get the user's class variable
                await send(functions.Mock(globals()[str(Regmsg[2]).lower() + '@' + str(message.author.guild).lower()]))
            except:
                # Return a list of possible users for a given server
                ValidUsers = []
                for i in MemberNameTags:
                    if i.split('@')[1] == str(message.author.guild).lower():
                        ValidUsers.append(i.split('@')[0])
                await send(f'Invalid user to mock, valid people are:\n{ValidUsers}')

        # Return Stats of a given user
        if Regmsg[1] == 'stats':
            try:
                await send(functions.Stats(globals()[str(Regmsg[2]).lower() + '@' + str(message.author.guild).lower()]))
            except:
                ValidUsers = []
                for i in MemberNameTags:
                    if i.split('@')[1] == str(message.author.guild).lower():
                        ValidUsers.append(i.split('@')[0])

                await send(f'Invalid user for stats, valid people are:\n{ValidUsers}')

        # MangoPerson PLEASE COMMENT THIS FUNCTION * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        # Cant comment this because idk what it does
        if Regmsg[1] == 'amogus':
            await amogus.handle_message(client, message)

        if Regmsg[1] == 'uwuify':
            await uwu.handle(client, message)

        # Does what you'd expect
        if Regmsg[1] == 'help':
            await send(functions.Help())


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await amogus.handle_vc(client, member, before, after)

client.run(os.environ['TOKEN'])
