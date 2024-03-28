import PyDictionary
import random
import os
import google.generativeai as genai
import discord


# This will run on first setup
# Initializes the AI and Discord Imports
def setup():
    # AI STUFF
    genai.configure(api_key=os.environ['AI_KEY'])
    model = genai.GenerativeModel('gemini-pro')

    # DISCORD SETUP
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)

    return client, model

# Will ensure the command has the proper format and number of arguments
def CheckIfCommandIsValid(message):
    Regmsg = message.content.lower().split(' ')
    if len(Regmsg) < 2:
        return False
    return True

# This will return a definition of a word using PyDictionary
def ReturnDefinition(word):
    try:
        return f'The definition of {word} is \n{PyDictionary.PyDictionary.meaning(word)}'
    except:
        return 'Something went wrong!'

# This will use Google's API to return a respons from a given prompt
def GenerateAiResponse(prompt, model):
    try:
        return model.generate_content(prompt).text
    except:
        return 'Something went wrong!'

# This is overly complicated and I don't feel like explaining it
# It works, DONT TOUTCH IT
# pls :3
def Mock(user):
    if user.ShouldMock:
        return 'User is already being mocked'
    else:
        user.ShouldMock = True
        return 'User is now being mocked'

# It does what it says
def Stats(user):
    return user.ReturnStats()

# Again, does what it says
def ScrambleLetters(string):
    print(string)
    ReturnVal = ''
    for i in string:
        ReturnVal += random.choice((i.lower(), i.upper()))
    return ReturnVal