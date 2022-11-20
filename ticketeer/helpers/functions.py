from ticketeer.database.models import Guild, Ticket, TicketMessage, TicketUser
from ticketeer.objects import TicketType
from typing import TYPE_CHECKING
import discord

if TYPE_CHECKING:
    from objects import Bot


def requires_guild(func):
    async def wrapper(ctx: discord.ApplicationContext, *args, **kwargs):
        guild = (await Guild.get_or_create(id=ctx.guild.id))[0]

        kwargs["guild"] = guild

        return await func(ctx, *args, **kwargs)
    return wrapper


@requires_guild
async def set_channel(ctx: discord.ApplicationContext, channel: discord.ChannelType, **kwargs) -> bool:
    guild: Guild = kwargs["guild"]

    ticket_type = guild.ticket_type

    data = {"ticket_channel": channel.id}
    if ticket_type == TicketType.none:
        data["ticket_type"] = TicketType.forum_private if isinstance(
            channel, discord.ForumChannel) else TicketType.text_private_thread

    await guild.update_from_dict(data)
    await guild.save()
    return True


@requires_guild
async def set_type(ctx: discord.ApplicationContext, bot: "Bot", ticket_type: TicketType, **kwargs) -> bool | tuple[bool, str]:
    guild: Guild = kwargs["guild"]
    print(guild)

    channel = bot.get_channel(guild.ticket_channel)

    if ticket_type.name.lower().startswith("forum") and not isinstance(channel, discord.ForumChannel):
        return False, "The ticket channel must be a forum channel to use forum ticket types."

    elif ticket_type.name.lower().startswith("text") and not isinstance(channel, discord.TextChannel):
        return False, "The ticket channel must be a text channel to use text ticket types."

    else:
        await guild.update_from_dict({"_ticket_type": ticket_type.value})
        await guild.save()
        return True, "Ticket type set to {}.".format(ticket_type.name)


@requires_guild
async def set_handler(ctx: discord.ApplicationContext, bot: "Bot", role: discord.Role, **kwargs):
    guild: Guild = kwargs["guild"]

    await guild.update_from_dict({"handler_role": role.id})
    await guild.save()
    return True
