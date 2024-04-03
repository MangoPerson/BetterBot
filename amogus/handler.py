import discord

from amogus.gamestate import GameState

active_games = {}


async def handle_message(client: discord.Client, message: discord.Message):
    args = message.content.split(' ')[2:]

    if args[0] != 'create':
        try:
            game: GameState = active_games[message.guild.id]
        except KeyError:
            await message.channel.send(f'There is no among us game currently running. Use $bb amogus create to make one')
            return

    if args[0] == 'create':
        await message.channel.send('Creating...')

        new_game = GameState('test', True, message.guild)
        active_games[new_game.server.id] = new_game

        await new_game.generate_channels()

        await message.channel.send(f'New Among Us game created on {message.guild.name}')

    elif args[0] == 'listplayers':
        await message.channel.send(f'Current players: {", ".join([player.user.name for player in game.players])}')

    elif args[0] == 'addplayer':
        for member in message.mentions:
            if member.id in [player.user.id for player in game.players]:
                await message.channel.send(f'{member.name} has already been added to the game')
            elif member.bot:
                await message.channel.send(f'Unfortunately for {member.name} Bots cannot play AMOGUS')
            else:
                game.add_player(member)
                await message.channel.send(f'Added {member.name} to the game on {game.server}')

    elif args[0] == 'start':
        game.start_game()
    else:
        await message.channel.send(f'\"{args[0]}\" is not a valid among us subcommand. Valid commands are:\n'
                                   f'\tcreate\n'
                                   f'\tlistplayers\n'
                                   f'\taddplayer\n'
                                   f'\tstart\n'
                                   f'\tsettings\n')


async def handle_vc(client: discord.Client, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if after.channel == before.channel:
        return

    try:
        game: GameState = active_games[member.guild.id]
    except KeyError:
        return

    if not game.is_running:
        return
    if not game.is_vc:
        return
    if after.channel.category.name.lower() != game.category_name.lower():
        return

    if after.channel:
        role = discord.utils.get(member.guild.roles, name=game.role_prefix + after.channel.name)
        await member.add_roles(role)

    if before.channel:
        role = discord.utils.get(member.guild.roles, name=game.role_prefix + before.channel.name)
        await member.remove_roles(role)
