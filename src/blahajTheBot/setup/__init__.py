import logging
from nextcord.ext import commands
import nextcord
from db import Configs_DB
from typing import Dict, List


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("Setup cog loaded!")
        self.db = Configs_DB()

    def get_config(self, guildId: int) -> Dict[str, str | None]:
        """Gets the complete config for the guild."""
        config = {'guild_id': guildId,
                  'memberCountChannel': None, 'verifiedRoleID': None}  # TODO: Add more configs
        for key in config:
            if config[key] is None:
                config[key] = self.db.get_config(guildId, key)
        return config

    @nextcord.slash_command(description="Use this to setup Blahaj!")
    @commands.has_permissions(administrator=True)
    async def setup(self, interaction: nextcord.Interaction) -> None:
        view = SetupMenu(db=self.db)
        await interaction.response.send_message("Please select what you want to setup", view=view, ephemeral=True)


# TW This is terrible code but idk how to do this better :")
class SetupMenu(nextcord.ui.View):
    def __init__(self, db: Configs_DB):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(SetupDropdown(db=db))


class SetupDropdown(nextcord.ui.Select):
    def __init__(self, db: Configs_DB):
        self.db = db
        options = [
            nextcord.SelectOption(
                label="Channels", description="Setup the special channels", emoji="📁"
            ),
            nextcord.SelectOption(
                label="Roles", description="Setup the roles", emoji="👥"
            ),
            nextcord.SelectOption(
                label="Moderation", description="Setup the moderation", emoji="🔨"
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
        logging.info(self.values)
        view = GenericView()
        if self.values[0] == 'Channels':
            view.add_item(ChannelSelector(db=self.db))
            view.add_item(BackButton(db=self.db))
            view.add_item(FinishButton())
            await interaction.response.send_message("Please select a channel", view=view, ephemeral=True)
        elif self.values[0] == 'Roles':
            view.add_item(RoleSelector(db=self.db))
            view.add_item(BackButton(db=self.db))
            view.add_item(FinishButton())
            await interaction.response.send_message("Please select a role that is goining to be assigned to a user once verified", view=view, ephemeral=True)
        elif self.values[0] == 'Moderation':
            view.add_item(BackButton(db=self.db))
            view.add_item(FinishButton())
            await interaction.response.send_message("WIP", view=view, ephemeral=True)
        elif self.values[0] == 'Miscellaneous':
            view.add_item(BackButton(db=self.db))
            view.add_item(FinishButton())
            await interaction.response.send_message("WIP", view=view, ephemeral=True)
        else:
            await interaction.response.send_message("How did You get here?", ephemeral=True)


class GenericView(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    def add_item(self, item: any) -> None:
        return super().add_item(item)


class ChannelSelector(nextcord.ui.ChannelSelect):
    def __init__(self, db: Configs_DB):
        self.db = db
        super().__init__(placeholder="Select a channel")

    async def callback(self, interaction: nextcord.Interaction) -> None:
        logging.info(self.values)
        resp = self.db.set_config(interaction.guild.id,
                                  'memberCountChannel', self.values[0].id)
        if resp:
            await interaction.response.send_message("Channel set!", ephemeral=True)
        else:
            await interaction.response.send_message("Something went wrong :((", ephemeral=True)


class RoleSelector(nextcord.ui.RoleSelect):
    def __init__(self, db):
        self.db = db
        super().__init__(placeholder="Select the role")

    async def callback(self, interaction: nextcord.Interaction) -> None:
        resp = self.db.set_config(interaction.guild.id,
                                  'verifiedRoleID', self.values[0].id)
        if resp:
            await interaction.response.send_message("Role set!", ephemeral=True)
        else:
            await interaction.response.send_message("Something went wrong :((", ephemeral=True)


class GenericSelector(nextcord.ui.Select):
    def __init__(self, db: Configs_DB, options: List[nextcord.SelectOption], placeholder: str):
        self.db = db
        super().__init__(placeholder=placeholder, options=options)


class BackButton(nextcord.ui.Button):
    def __init__(self, db: Configs_DB):
        self.db = db
        super().__init__(label="Back", style=nextcord.ButtonStyle.red)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        menu = SetupMenu(db=self.db)
        await interaction.response.send_message("Please select what you want to setup", view=menu, ephemeral=True)


class FinishButton(nextcord.ui.Button):
    def __init__(self):
        super().__init__(label="Finish", style=nextcord.ButtonStyle.green)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.send_message("Setup finished!", ephemeral=True)
