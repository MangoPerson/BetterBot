import random

import discord


def uwuify(text: str):
    result = (text
              .replace('r', 'w')
              .replace('R', 'W')
              .replace('l', 'w')
              .replace('L', 'W')
              .replace('—', '\~')
              .replace('-', '\~'))

    faces = ['(ꈍᴗꈍ)♡', '(〃￣ω￣〃)ゞ', '( ˶ˆ꒳ˆ˵ )', '( ੭•͈ω•͈)੭', '(,,>﹏<,,)', '(*＞ω＜*)♡', '(⸝⸝⸝O﹏ O⸝⸝⸝)', '⸜(｡˃ ᵕ ˂ )⸝', '(づ◡﹏◡)づ']

    result = f'UwU\~ {result} {random.choice(faces)}'
    return result


async def handle(client: discord.Client, message: discord.Message):
    if message.reference:
        message_replied = await message.channel.fetch_message(message.reference.message_id)
        text = message_replied.content

        await message.channel.send(f'「{uwuify(text)}」\n\t \~ {message.author.display_name}-ちゃん')
    else:
        text = ' '.join(message.content.split(' ')[2:])
        await message.channel.send(uwuify(text))
