import typing

import discord

from ticketeer.database.models import Guild, Ticket, TicketMessage, TicketUser
from ticketeer.objects.embeds import Error, Success, TicketEmbed, Info
from ticketeer.objects.views import TicketView, ConfigView
from ticketeer.objects import TicketType
from ticketeer.helpers.functions import set_channel, set_type, set_handler

if typing.TYPE_CHECKING:
    from ticketeer.objects import Bot


class Config(discord.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    set_cmd = discord.SlashCommandGroup(
        name="set",
        description="Configure Ticketeer settings.",
        checks=[lambda ctx: ctx.author.guild_permissions.manage_guild]
    )

    @set_cmd.command(name="config")
    async def command_set_config(self, ctx: discord.ApplicationContext):
        """
        Configure Ticketeer.
        """

        guild: Guild = (await Guild.get_or_create(id=ctx.guild.id))[0]

        embed = discord.Embed(
            title="Ticketeer Configuration",
            description="Each option can be set using the buttons below or their respective slash commands."
        )

        ticket_channel = ctx.guild.get_channel(
            guild.ticket_channel) or "No channel set."
        handler_role = ctx.guild.get_role(guild.handler_role) or "No role set."

        embed.add_field(name="Ticket Type", value=TicketType(
            guild.ticket_type or 0).name)
        embed.add_field(name="Ticket Channel", value=ticket_channel.mention if isinstance(
            ticket_channel, discord.TextChannel) else ticket_channel)
        embed.add_field(name="Ticket Handler Role", value=handler_role.mention if isinstance(
            handler_role, discord.Role) else handler_role)

        view = ConfigView(ctx, embed, guild, self.bot)

        await ctx.respond(
            embed=embed,
            view=view
        )

    @set_cmd.command(name="channel")
    async def command_set_channel(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(
            discord.TextChannel,
            description="The channel to set as the ticket channel.",
            required=False
        )
    ):
        """
        Set the channel where tickets are handled.
        """
        channel = channel or ctx.channel

        await set_channel(ctx, channel)

        embed = TicketEmbed(title="Create a Ticket",
                            description="Click the button below to create a ticket.")

        await channel.send(embed=embed, view=TicketView(ctx))
        await ctx.respond(embed=Success(description=f"Ticket channel set to {channel.mention}."))

    @set_cmd.command(name="type")
    async def command_set_type(
        self,
        ctx: discord.ApplicationContext,
        ticket_type: discord.Option(
            int,
            description="The type of ticket to create.",
            choices=[discord.OptionChoice(
                name=tickettype.name,
                value=tickettype,
            ) for tickettype in TicketType]
        )
    ):
        """
        Set the type of ticket to create.
        """
        status = await set_type(ctx, self.bot, TicketType(ticket_type))

        if not status[0]:
            await ctx.respond(embed=Error(description=status[1]))

        else:
            await ctx.respond(embed=Success(description=status[1]))

    @set_cmd.command(name="handler")
    async def command_set_handler(
        self,
        ctx: discord.ApplicationContext,
        role: discord.Option(
            discord.Role,
            description="The role to set as the ticket handler role.",
            required=True
        )
    ):
        """
        Set the role that can handle tickets.
        """
        await set_handler(ctx, self.bot, role)

        await ctx.respond(embed=Success(description=f"Ticket handler role set to {role.mention}."))


def setup(bot: "Bot"):
    bot.add_cog(Config(bot))
