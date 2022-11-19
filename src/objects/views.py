import discord

class TicketView(discord.ui.View):
    ctx: discord.ApplicationContext

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Create Ticket",
        style=discord.ButtonStyle.blurple,
        custom_id=f"{ctx.guild.id}"
        )
    async def create_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Ticket created!",
            ephemeral=True
        )
    
    @classmethod
    async def create(cls: "TicketView", ctx: discord.ApplicationContext):
        view = cls()
        view.ctx = ctx
        return view