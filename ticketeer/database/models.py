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
