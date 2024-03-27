import PyDictionary
import random
import os
import google.generativeai as genai
import discord


def setup():
    # AI STUFF
    genai.configure(api_key=os.environ['AI_KEY'])
    model = genai.GenerativeModel('gemini-pro')

    # DISCORD SETUP
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)

    return client, model


def CheckIfCommandIsValid(message):
    Regmsg = message.content.lower().split(' ')
    if len(Regmsg) < 2:
        return False
    return True


def ReturnDefinition(word):
    try:
        return f'The definition of {word} is \n{PyDictionary.PyDictionary.meaning(word)}'
    except:
        return 'Something went wrong!'


def GenerateAiResponse(prompt, model):
    try:
        return model.generate_content(prompt).text
    except:
        return 'Something went wrong!'


def Mock(user, users, guild):

    # print(globals()[str(user).lower() + '_' + str(guild).lower()].name)
    # print(users)
    # print(guild)

    return

    if user not in [r[0] for r in users]:
        return 'Invalid user, possible user are'

    if user.IsBeingMocked:
        return 'User is already being mocked'
    else:
        user.IsBeingMocked = True
        user.UpdateMock()
        return 'User is now being mocked'