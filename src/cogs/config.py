import discord
import typing
from database.models import (
    Guild,
    Ticket,
    TicketMessage,
    TicketUser
)

if typing.TYPE_CHECKING:
    from objects import Bot


class Config(discord.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
    
    set_cmd = discord.SlashCommandGroup(
        name="set",
        description="Configure Ticketeer settings.",
        checks=[lambda ctx: ctx.author.guild_permissions.manage_guild]
        )

    @set_cmd.command(name="channel")
    async def command_set_channel(ctx: discord.ApplicationContext, channel: discord.TextChannel):
        """
        Set the channel where tickets are handled.
        """
        guild = await Guild.get_or_create(id=ctx.guild.id)
        await guild.update(ticket_channel=channel.id)
        await ctx.send(f"Ticket channel set to {channel.mention}.")
    

def setup(bot: "Bot"):
    bot.add_cog(Config(bot))