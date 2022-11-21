import discord
import typing
from ticketeer.database.models import Guild, Ticket, TicketMessage, TicketUser
from ticketeer.objects.embeds import Success, Error, Info
from ticketeer.objects import TicketType
import shortuuid

if typing.TYPE_CHECKING:
    from ticketeer.objects import Bot


class Listeners(discord.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @discord.Cog.listener(name="on_interaction")
    async def on_interaction(self, interaction: discord.Interaction):
        if not interaction.is_component() or not interaction.message.author == self.bot.user:
            return

        data = interaction.custom_id.split("-")
        if len(data) != 2:
            return

        if not int(data[0]) == interaction.guild.id or not data[1] == "create_ticket":
            return

        guild: Guild = await Guild.get_or_none(id=data[0])

        if not guild:
            return
        
        if guild.ticket_type == TicketType.none:
            await interaction.response.send_message(
                embed=Error(
                    title="Ticket Creation Failed",
                    description="Ticket creation is disabled on this server."
                ),
                ephemeral=True
            )
            return
        
        if guild.ticket_channel is None:
            await interaction.response.send_message(
                embed=Error(
                    title="Ticket Creation Failed",
                    description="Ticket channel is not set."
                ),
                ephemeral=True
            )
            return
        
        private = "private" in guild.ticket_type.name.lower()
        text = "text" in guild.ticket_type.name.lower()
        forum = "forum" in guild.ticket_type.name.lower()
        thread = "thread" in guild.ticket_type.name.lower()
        channel = "channel" in guild.ticket_type.name.lower()

        ticket_id = shortuuid.random(length=8)

        if text and thread:
            channel_thread = await interaction.channel.create_thread(
                name=f"Ticket {interaction.user.name} - {ticket_id}",
                type=discord.ChannelType.private_thread if private else discord.ChannelType.public_thread,
            )

        elif text and channel:
            # TODO: Create channel within guild.category
            ...
        
        ticket_users = [interaction.user]

        if role := interaction.guild.get_role(guild.handler_role):
            ticket_users.extend([member for member in role.members])

        ticket = await Ticket.create(id=ticket_id)
        await ticket.guild.add(guild)

        ticket_user_objs = []

        for user in ticket_users:
            ticket_user = await TicketUser.create(
                id=shortuuid.random(length=8),
                discord_id=interaction.user.id,
                is_member=not role in user.roles,
                is_handler=role in user.roles
            )
            await ticket_user.ticket.add(ticket)
            ticket_user_objs.append(ticket_user)

            await channel_thread.add_user(user)

        await ticket.users.add(*ticket_user_objs)
        await ticket.save()
        
        await interaction.response.send_message(
            embed=Success(description="Ticket successfully created!"),
            ephemeral=True
        )

    @discord.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):
        try:
            id = message.channel.name[:8]
        except:
            return
        ticket = await Ticket.get_or_none(id=id)
        if not ticket:
            return

        ticket_message = await TicketMessage.create(
            id=message.id,
            content=message.content
        )
        await ticket_message.ticket.add(ticket)
        await ticket_message.author.add(await TicketUser.get_or_create(discord_id=message.author.id))
        await ticket_message.save()

def setup(bot: "Bot"):
    bot.add_cog(Listeners(bot))
