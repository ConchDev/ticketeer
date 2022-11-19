import typing

import discord

from database.models import Guild, Ticket, TicketMessage, TicketUser
from objects.embeds import Error, Success, TicketEmbed
from objects.views import TicketView

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
    async def command_set_channel(self, ctx: discord.ApplicationContext, channel: discord.Option(discord.TextChannel, description="The channel to set as the ticket channel.")):
        """
        Set the channel where tickets are handled.
        """
        guild: Guild = (await Guild.get_or_create(id=ctx.guild.id))[0]
        await guild.update_from_dict({"ticket_channel": channel.id})

        embed = TicketEmbed(title="Create a Ticket", description="Click the button below to create a ticket.")

        await channel.send(embed=embed, view=TicketView())

        await ctx.respond(embed=Success(description=f"Ticket channel set to {channel.mention}."))
    

def setup(bot: "Bot"):
    bot.add_cog(Config(bot))