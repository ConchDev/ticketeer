import discord
import typing

if typing.TYPE_CHECKING:
    from objects import Bot


class Config(discord.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
    

def setup(bot: "Bot"):
    bot.add_cog(Config(bot))