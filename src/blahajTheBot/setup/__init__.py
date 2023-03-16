import logging
from nextcord.ext import commands
import nextcord


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("Setup cog loaded!")

    @nextcord.slash_command(description="Use this to setup Blahaj!")
    @commands.has_permissions(administrator=True)
    async def setup(self, interaction: nextcord.Interaction) -> None:
        view = SetupMenu()
        await interaction.response.send_message("Please select what you want to setup", view=view)
        await interaction.response.defer()
        logging.info(view.values)


class SetupMenu(nextcord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(SetupDropdown())


class SetupDropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label="Channels", description="Setup the special channels", emoji="📁"
            ),
            nextcord.SelectOption(
                label="Roles", description="Setup the roles", emoji="👥"
            ),
            nextcord.SelectOption(
                label="Moderation", description="Setup the moderation", emoji="🛡️"
            ),
            nextcord.SelectOption(
                label="Miscellaneous", description="Setup miscellaneous things", emoji="🔧"
            ),
        ]
        super().__init__(
            placeholder="Select what you want to setup",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        view = GenericView()
        if self.values[0] == 'Channels':
            view.add_item(ChannelSelector())
            await interaction.response.send_message("Please select a channel", view=view)
        elif self.values[0] == 'Roles':

            await interaction.response.send_message("Please select a role", view=view)


class GenericView(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    def add_item(self, item: any) -> None:
        return super().add_item(item)


class ChannelSelector(nextcord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(placeholder="Select a channel")


class GenericSelector(nextcord.ui.Select):
    def __init__(self, options: list, placeholder: str):
        super().__init__(placeholder=placeholder, options=options)
