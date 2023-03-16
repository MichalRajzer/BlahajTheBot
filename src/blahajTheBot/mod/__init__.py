import logging
from nextcord.ext import commands
import nextcord
import asyncio


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Use this to verify yourself!")
    async def verify(self, interaction: nextcord.Interaction) -> None:
        view = RuleVerifier()
        await interaction.response.send_message("Please verify yourself!", view=view)


class RuleVerifierDropdown(nextcord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            nextcord.SelectOption(
                label="Agree", description="You agree to follow rules", emoji="✅"
            ),
            nextcord.SelectOption(
                label="Deny", description="You don't agree to follow rules", emoji="❌"
            ),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(
            placeholder="Do You accept the rules?",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] != 'Agree':
            await interaction.response.send_message("Goodbye!")
            await asyncio.sleep(5)
            await interaction.user.kick(reason="You didn't agree to the rules >:(")
        else:
            await interaction.user.add_roles(
                interaction.guild.get_role(1045758940404777011))  # TODO Hardcoded role ID, will be changed later
            await interaction.response.send_message("Welcome aboard!")


class RuleVerifier(nextcord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(RuleVerifierDropdown())
