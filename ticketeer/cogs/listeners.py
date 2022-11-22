import discord
import typing
from io import StringIO
from ticketeer.database.models import Guild, Ticket, TicketMessage, TicketUser
from ticketeer.objects.embeds import Success, Error, Info
from ticketeer.objects import TicketType
from ticketeer.helpers.functions import unexpected_ticket_close
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

        ticket_type_name = guild.ticket_type.name.lower().replace("_", " ")

        private = "private" in ticket_type_name
        text = "text" in ticket_type_name
        forum = "forum" in ticket_type_name
        thread = "thread" in ticket_type_name
        channel = "channel" in ticket_type_name

        ticket_id = shortuuid.ShortUUID("abcdefghijklmnopqrstuvwxyz1234567890").random(length=8)
        handler_role = interaction.guild.get_role(guild.handler_role)

        if text and thread:
            channel_thread = await interaction.channel.create_thread(
                name=f"Ticket {interaction.user.name} - {ticket_id}",
                type=discord.ChannelType.private_thread if private else discord.ChannelType.public_thread,
            )

            ticket_users = [interaction.user]

            if handler_role:
                ticket_users.extend(
                    [member for member in handler_role.members])

            ticket = await Ticket.create(id=ticket_id)
            await ticket.guild.add(guild)

            ticket_users_obj = await TicketUser.create_from_list(ticket_users, ticket, handler_role)

            for user in ticket_users:
                await channel_thread.add_user(user)

            await ticket.users.add(*ticket_users_obj)
            await ticket.save()

        elif text and channel:
            category = interaction.guild.get_channel(guild.ticket_category)
            if not category:
                return

            if private:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(
                        read_messages=True, send_messages=True)
                }
            else:
                overwrites = {
                    interaction.user: discord.PermissionOverwrite(
                        read_messages=True, send_messages=True)
                }

            if handler_role:
                overwrites[handler_role] = discord.PermissionOverwrite(
                    read_messages=True, send_messages=True)

            channel = await interaction.guild.create_text_channel(
                name=f"{interaction.user.name}-ticket-{ticket_id}",
                category=category,
                reason=f"Ticket created by {interaction.user} ({interaction.user.id})",
                overwrites=overwrites
            )

            ticket = await Ticket.create(
                id=ticket_id
            )
            await ticket.guild.add(guild)

            users = [interaction.user]

            if handler_role:
                users.extend(handler_role.members)

            users = await TicketUser.create_from_list(users, ticket, handler_role)

            await ticket.users.add(*users)
            await ticket.save()

        await interaction.response.send_message(
            embed=Success(description="Ticket successfully created!"),
            ephemeral=True
        )

    @discord.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):
        try:
            id = message.channel.name[-8:]
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
        await ticket_message.author.add((await TicketUser.get_or_create(discord_id=message.author.id))[0])
        await ticket_message.save()

    @discord.Cog.listener(name="on_guild_channel_delete")
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        ticket_id = channel.name[-8:]
        status = await unexpected_ticket_close(channel, ticket_id)

        guild = await Guild.get_or_none(id=channel.guild.id)

        transcript_channel = channel.guild.get_channel(guild.transcript_channel)

        print(status)
        print(transcript_channel)
        print(guild)

        if not status[0] or not transcript_channel or not guild:
            return

        await transcript_channel.send(
            embed=Info(title="Ticket Transcript", description=f"Ticket {ticket_id} has been closed."),
            file=discord.File(status[1], filename=f"{ticket_id}.txt")
        )

    
    @discord.Cog.listener(name="on_raw_thread_delete")
    async def on_raw_thread_delete(self, payload: discord.RawThreadDeleteEvent):
        ...

def setup(bot: "Bot"):
    bot.add_cog(Listeners(bot))
