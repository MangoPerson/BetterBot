

import random

import PyDictionary

import discord

import re



# AI STUFF

import google.generativeai as genai

genai.configure(api_key='NOT AVAILABLE')

model = genai.GenerativeModel('gemini-pro')



# DISCORD SETUP

intents = discord.Intents.all()

intents.message_content = True

client = discord.Client(intents=intents)





class DiscordPerson:

    def __init__(self, name):

        self.TimesMocked = 0

        self.name = name

        self.IsBeingMocked = False

        self.ShouldMock = False



    def UpdateMock(self):

        if self.IsBeingMocked == True:

            self.ShouldMock = True

            if self.TimesMocked + 1 >= 10:

                self.ShouldMock = False

                self.IsBeingMocked = False

                self.TimesMocked = 0

            else:

                self.TimesMocked += 1





    def ReturnStats(self):

        return {

            'Times Mocked': self.TimesMocked,

            'Name': self.name,

            'Is being mocked': self.IsBeingMocked

        }



# FIRST RUN THROUGH

@client.event

async def on_ready():

    print(f'We have logged in as {client.user}')

    global MEMBERS

    MEMBERS = []

    for member in client.get_all_members():

        MEMBERS.append(member)

    global MembersList

    MembersList = []

    MembersList = [str(MEMBERS[x]) for x in range(len(MEMBERS))]



    for i in range(len(MembersList)):

        globals()[f'{MembersList[i]}'] = DiscordPerson(MembersList[i])



@client.event

async def on_message(message):



    print(f'Message from {message.author}:\n{message.content}')

    if message.author == client.user:

        return

    # Test to see if user should be mocked

    try:

        if globals()[f'{message.author}'].ShouldMock:

            globals()[f'{message.author}'].UpdateMock()

            sentence = '*'

            for i in range(len(message.content.lower())):

                sentence += str(random.choice([message.content.lower()[i].upper(), message.content.lower()[i].lower()]))

            sentence += '*'





            await message.channel.send(sentence)

    except:

        await message.channel.send("Something went wrong!")

        raise Exception

        return



    if message.content.lower().startswith('$betterbot') or message.content.lower().startswith('$bb'):



        Regmsg = message.content.lower().split(' ')

        send = message.channel.send



        # ERROR CORRECTION

        if len(Regmsg) == 1:

            await send('Invalid command, please enter a proper command')

            return

        if len(Regmsg) < 3 :

            if Regmsg[1] == 'help':

                try:

                    await send('help: this command\n'

                               'say [prompt]: will say whatever is in the prompt\n'

                               '[dict, define, dictionary] [word]: using any of the first commands, it will define [word]\n'

                               'ai [prompt] will run prompt through an LLM\n'

                               'mock [user] will start mocking [user] for the next 10 prompts\n'

                               'stats [user] will return statistics about [user]')

                except:

                    await send('Something went wrong!')

                    raise Exception

                    return

                return

            await send('Invalid command, please enter a proper command')

            return





        # DICTIONARY CODE

        try:

            if Regmsg[1] in ['dict', 'dictionary', 'define']:

                if Regmsg[2] == '*help':

                    await send(f'The definition of help is :\n{PyDictionary.PyDictionary.meaning('help')}')

                    return

                if Regmsg[2] == 'help':

                    await send('To use the dictionary feature, write $bb [\'dict\', \'dictionary\', or \'define\'] WORD_TO_DEFINE \nTo define help, re-run the command with \'*help\'')

                    return

                await send(f'The definition of {Regmsg[2]} is :\n{PyDictionary.PyDictionary.meaning(Regmsg[2])}')

                return

        except:

            await send('Something went wrong!')

            raise Exception

            return



        # AI CODE

        try:

            if Regmsg[1] in ['ai']:

                await send('*Getting Response*')

                content = [' '.join(str(x) for x in Regmsg[2:])][0]

                print(model.generate_content(content).text)

                await send(model.generate_content(content).text)

                return

        except:

            await send('Something went wrong!')

            raise Exception

            return



        # SAY CODE

        try:

            if Regmsg[1] == 'say':

                content = [' '.join(str(x) for x in Regmsg[2:])][0]

                await send(content)

                return

        except:

            await send('Something went wrong!')

            raise Exception

            return



        # MOCKING CODE

        try:

            global MembersList

            if Regmsg[1] == 'mock':

                if Regmsg[2] not in MembersList:

                    await send(f'User \'{Regmsg[2]}\' is not a valid member.\nValid members are: \n{MembersList}')

                    return

                else:

                    if globals()[Regmsg[2]].IsBeingMocked == False:

                        globals()[Regmsg[2]].IsBeingMocked = True

                        globals()[Regmsg[2]].UpdateMock()

                        await send(f'User {Regmsg[2]} is now being mocked')

                    else:

                        await send(f'User {Regmsg[2]} is already being mocked')

                        return

        except:

            await send('Something went Wrong!')

            raise Exception

            return



        # STATS CODE

        try:

            if Regmsg[1] == 'stats':

                if Regmsg[2] not in MembersList:

                    await send(f'User \'{Regmsg[2]}\' is not a valid member.\nValid members are: \n{MembersList}')

                    return

                else:

                    await send(globals()[Regmsg[2]].ReturnStats())

                    return

        except:

            await send('Something wend wrong!')

            raise Exception

            return











client.run('NOT AVAILABLE')
