import discord


class Success(discord.Embed):
    def __init__(self, *args, **kwargs):
        kwargs.pop("color", None)
        super().__init__(
            *args,
            **kwargs,
            color=discord.Color.green()
        )

class Error(discord.Embed):
    def __init__(self, *args, **kwargs):
        kwargs.pop("color", None)
        super().__init__(
            *args,
            **kwargs,
            color=discord.Color.red()
        )

class TicketEmbed(discord.Embed):
    def __init__(self, *args, **kwargs):
        kwargs.pop("color", None)
        super().__init__(
            *args,
            **kwargs,
            color=discord.Color.blurple()
        )