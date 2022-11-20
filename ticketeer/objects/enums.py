from enum import Enum


tickettype_descriptions = {
    0: "No ticket type selected.",
    1: "Create private threads in a forum channel.",
    2: "Create public threads in a forum channel.",
    3: "Create private threads in a text channel.",
    4: "Create public threads in a text channel.",
    5: "Create private channels in a category.",
    6: "Create public channels in a category."
}


class StartupType(Enum):
    dev = 1
    prod = 2


class TicketType(Enum):
    none = 0
    forum_private = 1
    forum_public = 2
    text_private_thread = 3
    text_public_thread = 4
    text_private_channel = 5
    text_public_channel = 6

    @property
    def name(self):
        return super().name.replace("_", " ").title()

    @property
    def description(self) -> str:
        return tickettype_descriptions[self.value]
