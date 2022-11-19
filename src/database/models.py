from tortoise.models import Model
from tortoise.fields import (
    CharField,
    BigIntField,
    ManyToManyField,
    BooleanField
)

class Ticket(Model):
    id = CharField(max_length=18, pk=True)
    guild = ManyToManyField(
        "models.Guild",
        related_name="tickets",
        on_delete="CASCADE"
    )
    users = ManyToManyField("models.User", related_name="ticket")
    closed = BooleanField(default=False)
    messages = ManyToManyField("models.TicketMessage", related_name="ticket")

class TicketUser(Model):
    id = CharField(max_length=18, pk=True)
    ticket = ManyToManyField(
        "models.Ticket",
        related_name="users",
        through="ticketuser_ticket",
    )

    is_member = BooleanField(default=False)
    is_moderator = BooleanField(default=False)


class Guild(Model):
    id = BigIntField(max_length=18, pk=True)
    tickets = ManyToManyField(
        "models.Ticket",
        related_name="guild",
    )
    mod_role = BigIntField(null=True)
    ticket_channel = BigIntField(null=True)
    ticket_category = BigIntField(null=True)


class TicketMessage(Model):
    id = BigIntField(max_length=18, pk=True)
    ticket = ManyToManyField(
        "models.Ticket",
        related_name="messages",
        through="ticketmessage_ticket",
    )
    author = ManyToManyField("models.User", related_name="messages")
    content = CharField(max_length=2000)