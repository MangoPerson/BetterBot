import discord

from amogus.gamestate import GameState

active_games: list[GameState]


async def handle(client: discord.Client, message: discord.Message):
    args = message.content.split(' ')[2:]

    print(args)
