from tortoise.models import Model
from tortoise.fields import (
    CharField,
    BigIntField,
    SmallIntField,
    ManyToManyField,
    ManyToManyRelation,
    BooleanField
)
from ticketeer.objects import TicketType
import discord
import shortuuid


class Ticket(Model):
    id = CharField(max_length=10, pk=True)
    guild = ManyToManyField(
        "ticketeer.Guild",
        related_name="tickets",
        on_delete="CASCADE"
    )
    users = ManyToManyField("ticketeer.TicketUser", related_name="ticket")
    closed = BooleanField(default=False)
    messages = ManyToManyField(
        "ticketeer.TicketMessage", related_name="ticket")

    class Meta:
        app = "ticketeer"


class TicketUser(Model):
    id = CharField(max_length=10, pk=True)
    discord_id = BigIntField()
    ticket: ManyToManyRelation[Ticket]

    is_member = BooleanField(default=False)
    is_handler = BooleanField(default=False)

    class Meta:
        app = "ticketeer"
    
    @classmethod
    async def create_from_list(cls, users: list[discord.User | discord.Member], ticket: Ticket, handler_role: discord.Role):
        ticket_users = []
        for user in users:
            is_handler = handler_role in user.roles
            ticket_user = await cls.create(
                id=shortuuid.random(length=8),
                discord_id=user.id,
                is_member=not is_handler,
                is_handler=is_handler
            )
            await ticket_user.ticket.add(ticket)
            ticket_users.append(ticket_user)
        return ticket_users


class Guild(Model):
    id = BigIntField(max_length=18, pk=True)
    tickets: ManyToManyRelation[Ticket]
    _ticket_type = SmallIntField(null=True, source_field="ticket_type")
    handler_role = BigIntField(null=True)
    ticket_channel = BigIntField(null=True)
    ticket_category = BigIntField(null=True)

    @property
    def ticket_type(self) -> TicketType:
        return TicketType(self._ticket_type or 0)

    class Meta:
        app = "ticketeer"


class TicketMessage(Model):
    id = BigIntField(max_length=18, pk=True)
    ticket: ManyToManyRelation[Ticket]
    author: ManyToManyRelation[TicketUser]
    content = CharField(max_length=2000)

    class Meta:
        app = "ticketeer"
