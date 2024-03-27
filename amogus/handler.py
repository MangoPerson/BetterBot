import discord


async def handle(client: discord.Client, message: discord.Message):
    embed = discord.Embed(color=0x00ff00, title='Test', description='Among us')
    await message.channel.send(embed=embed)
