import discord
from objects import TicketType
from database.models import Guild
import typing
from objects.embeds import TicketEmbed, Success, Error
from helpers.functions import set_channel, set_type, set_handler

if typing.TYPE_CHECKING:
    from objects import Bot


class TicketView(discord.ui.View):
    def __init__(self, ctx: discord.ApplicationContext):
        super().__init__(timeout=None)
        self.add_item(self.CreateTicket(ctx))

    class CreateTicket(discord.ui.Button):
        def __init__(self, ctx: discord.ApplicationContext):
            self.ctx = ctx
            super().__init__(
                label="Create Ticket",
                style=discord.ButtonStyle.blurple,
                custom_id=f"{ctx.guild.id}-create-ticket"
            )

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_message(
                "Ticket created!",
                ephemeral=True
            )


class ConfigView(discord.ui.View):
    def __init__(self, ctx: discord.ApplicationContext, embed: discord.Embed, guild: Guild, bot: "Bot"):
        super().__init__(timeout=60)
        children = [
            self.ButtonTicketChannel(ctx, embed, guild, bot),
            self.ButtonTicketHandler(ctx, embed, guild, bot),
            self.SelectTicketType(ctx, embed, guild, bot),
        ]
        for child in children:
            self.add_item(child)

    class SelectTicketType(discord.ui.Select):
        def __init__(self, ctx: discord.ApplicationContext, embed: discord.Embed, guild: Guild, bot: "Bot"):
            self.ctx = ctx
            self.embed = embed
            self.guild = guild
            self.bot = bot
            super().__init__(
                placeholder="Ticket Type",
                custom_id=f"{ctx.interaction.id}-config_ticket_type",
                options=[discord.SelectOption(
                    label=tickettype.name,
                    value=str(tickettype.value),
                    description=tickettype.description
                ) for tickettype in TicketType],
                row=0
            )

        async def callback(self, interaction: discord.Interaction):
            selection = TicketType(int(self.values[0] or 0))

            status = await set_type(self.ctx, self.bot, selection)

            if not status[0]:
                await interaction.response.send_message(embed=Error(description=status[1]), ephemeral=True)

            else:
                self.embed.fields[0].value = selection.name

                await interaction.response.send_message(embed=Success(description=status[1]), ephemeral=True)
                await self.view.message.edit(embed=self.embed, view=self.view)
                return

    class ButtonTicketChannel(discord.ui.Button):
        def __init__(self, ctx: discord.ApplicationContext, embed: discord.Embed, guild: Guild, bot: "Bot"):
            self.ctx = ctx
            self.embed = embed
            self.guild = guild
            self.bot = bot
            super().__init__(
                label="Channel",
                style=discord.ButtonStyle.blurple,
                custom_id=f"{ctx.interaction.id}-config_ticket_channel",
                row=1
            )

        class ChannelModal(discord.ui.Modal):
            def __init__(
                self,
                ctx: discord.ApplicationContext,
                embed: discord.Embed,
                guild: Guild,
                bot: "Bot",
                button: discord.ui.Button
            ):
                self.ctx = ctx
                self.embed = embed
                self.guild = guild
                self.bot = bot
                self.view = button.view

                super().__init__(
                    discord.ui.InputText(
                        label="Channel ID",
                        placeholder="881224361015672863",
                        custom_id=f"{ctx.interaction.id}-config_ticket_channel_modal_input",
                        style=discord.InputTextStyle.short,
                        required=True
                    ),
                    title="Set Ticket Channel",
                    custom_id=f"{ctx.interaction.id}-config_ticket_channel_modal",
                )

            async def callback(self, interaction: discord.Interaction):
                channel_id = self.children[0].value
                channel = self.ctx.guild.get_channel(int(channel_id))

                await set_channel(self.ctx, channel)

                self.embed.fields[1].value = channel.mention

                embed = TicketEmbed(title="Create a Ticket",
                                    description="Click the button below to create a ticket.")

                await channel.send(embed=embed, view=TicketView(self.ctx))

                await interaction.response.send_message(embed=Success(description=f"Ticket channel set to {channel.mention}"), ephemeral=True)
                await self.view.message.edit(embed=self.embed, view=self.view)

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_modal(self.ChannelModal(
                self.ctx,
                self.embed,
                self.guild,
                self.bot,
                self
            ))

    class ButtonTicketHandler(discord.ui.Button):
        def __init__(self, ctx: discord.ApplicationContext, embed: discord.Embed, guild: Guild, bot: "Bot"):
            self.ctx = ctx
            self.embed = embed
            self.guild = guild
            self.bot = bot
            super().__init__(
                label="Handler",
                style=discord.ButtonStyle.blurple,
                custom_id=f"{ctx.interaction.id}-config_ticket_handler",
                row=1
            )

        class HandlerModal(discord.ui.Modal):
            def __init__(
                self,
                ctx: discord.ApplicationContext,
                embed: discord.Embed,
                guild: Guild,
                bot: "Bot",
                button: discord.ui.Button
            ):
                self.ctx = ctx
                self.embed = embed
                self.guild = guild
                self.bot = bot
                self.view = button.view

                super().__init__(
                    discord.ui.InputText(
                        label="Role ID",
                        placeholder="881224361015672863",
                        custom_id=f"{ctx.interaction.id}-config_ticket_handler_modal_input",
                        style=discord.InputTextStyle.short,
                        required=True
                    ),
                    title="Set Ticket Handler Role",
                    custom_id=f"{ctx.interaction.id}-config_ticket_handler_modal",
                )

            async def callback(self, interaction: discord.Interaction):
                handler_id = self.children[0].value
                handler = self.ctx.guild.get_role(int(handler_id))

                await set_handler(self.ctx, self.bot, handler)

                self.embed.fields[2].value = handler.mention

                await interaction.response.send_message(embed=Success(description=f"Ticket handler set to {handler.mention}"), ephemeral=True)
                await self.view.message.edit(embed=self.embed, view=self.view)

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_modal(self.HandlerModal(
                self.ctx,
                self.embed,
                self.guild,
                self.bot,
                self
            ))
