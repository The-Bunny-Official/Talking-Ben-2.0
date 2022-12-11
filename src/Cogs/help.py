### Imports ###
import discord

from discord.ext import commands
from discord.ui import Button, View, select
from discord import Permissions, SelectOption


### Help Command - VIEW ###
class HelpView(View):
    def __init__(self, client):
        self.client: discord.Bot = client
        super().__init__(timeout=None)
    
    @select(
        custom_id="HelpSelect",
        placeholder="Category",
        max_values=1,
        options=[
            SelectOption(
                label='Links',
                description='Other links',
                value='links'
            ),
            SelectOption(
                label='User Commands',
                description='Commands available to everyone',
                value='user'
            ),
            SelectOption(
                label='Moderator',
                description='Commands available to certain perms',
                value='mod'
            ),
            SelectOption(
                label='VIP',
                description='VIP stuff',
                value='vip'
            ),
            SelectOption(
                label='Experience',
                description='Xp related stuff',
                value='xp'
            ),
            SelectOption(
                label='Default',
                description='Back to the first page',
                value='default'
            )
        ]
    )
    async def callback(self, select, interaction: discord.Interaction):
        value = select.values
        if value[0] == 'default':
            await interaction.response.edit_message(embed=discord.Embed(title="Talking Ben Help Page", description="The help page for the Talking Ben Bot.", color=discord.Color.green()).add_field(name="Prefix", value="Slash Commands [/]").add_field(name="How to chat?", value=f"Just ping me [<@{interaction.client.config['app_id']}>]").add_field(name="Basic Commands", value="help - ping - stats"))                                          
        elif value[0] == 'links':
            await interaction.response.edit_message(embed=discord.Embed(title='Links', description='Links and such').add_field(name='Terms Of Service', value="https://docs.google.com/document/d/10L4Z9fEvK5ltajJuIMDRsq6dVJ47yyPuQLpN6Xwzi6Q/").add_field(name='Privacy Policy', value='https://docs.google.com/document/d/1aEYcuQlBuAPYkzSny7HlaRNvZbhvITn98hV-DjdeiMU/'))
        elif value[0] == 'user':
            await interaction.response.edit_message(embed=discord.Embed(title="Commands - User", description="All the user available commands", color=discord.Color.green()).add_field(name="suggest", value="Make a suggestion").add_field(name="help", value="Get a help list").add_field(name="ping", value="returns bot ping in ms").add_field(name="bot", value="get stats on ben").add_field(name="hug <user>", value="Sends a hug to <user>").add_field(name="rps", value="Play rock paper scissors"))
        elif value[0] == 'mod':
            await interaction.response.edit_message(embed=discord.Embed(title="Moderation/Admin Commands", description="All the commands that Admins/Mods can use", color=discord.Color.green()).add_field(name="welcome_setup", value="Setup welcome messages within a server. Use {0} in place of a member ping."))
        elif value[0] == 'vip':
            await interaction.response.edit_message(embed=discord.Embed(title="VIP Commands", description="Simply use /vip_help :)", color=discord.Color.gold()))
        elif value[0] == 'xp':
            await interaction.response.edit_message(embed=discord.Embed(title="XP Commands", description="All commands available for XP", color=discord.Color.green()).add_field(name="xp", value="get the xp of you or another user").add_field(name="leaderboard", value="get the top 10 leaderboard"))

### Help Command Cog ###
class help(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot

    @commands.slash_command(name="help", description="Get some bot help")
    async def help(self, ctx: discord.ApplicationContext):
        await ctx.respond(embed=discord.Embed(title="Talking Ben Help Page", description="The help page for the Talking Ben Bot.", color=discord.Color.green()).add_field(name="Prefix", value="Slash Commands [/]").add_field(name="How to chat?", value=f"Just ping me [<@{self.bot.config['app_id']}>]").add_field(name="Basic Commands", value="help - ping - stats"), view=HelpView(self.bot))


### Setup the Cog ###
def setup(bot: discord.Bot):
    bot.add_cog(help(bot))