from enum import Enum


class StartupType(Enum):
    dev = 1
    prod = 2


class TicketType(Enum):
    forum_private = 1
    forum_public = 2
    text_private_thread = 3
    text_public_thread = 4
    text_public_channel = 5
    text_private_channel = 6