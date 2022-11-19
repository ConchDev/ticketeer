from tortoise.models import Model
from tortoise.fields import (
    CharField,
    BigIntField,
    ManyToManyField,
    ManyToManyRelation,
    BooleanField
)

class Ticket(Model):
    id = CharField(max_length=18, pk=True)
    guild = ManyToManyField(
        "ticketeer.Guild",
        related_name="tickets",
        on_delete="CASCADE"
    )
    users = ManyToManyField("ticketeer.TicketUser", related_name="ticket")
    closed = BooleanField(default=False)
    messages = ManyToManyField("ticketeer.TicketMessage", related_name="ticket")

    class Meta:
        app = "ticketeer"

class TicketUser(Model):
    id = CharField(max_length=18, pk=True)
    ticket: ManyToManyRelation[Ticket]

    is_member = BooleanField(default=False)
    is_moderator = BooleanField(default=False)

    class Meta:
        app = "ticketeer"

class Guild(Model):
    id = BigIntField(max_length=18, pk=True)
    tickets: ManyToManyRelation[Ticket]
    mod_role = BigIntField(null=True)
    ticket_channel = BigIntField(null=True)
    ticket_category = BigIntField(null=True)

    class Meta:
        app = "ticketeer"

class TicketMessage(Model):
    id = BigIntField(max_length=18, pk=True)
    ticket: ManyToManyRelation[Ticket]
    author: ManyToManyRelation[TicketUser]
    content = CharField(max_length=2000)
    
    class Meta:
        app = "ticketeer"