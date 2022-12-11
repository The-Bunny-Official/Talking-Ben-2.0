### Imports ###
import discord
import time

from discord import Option
from discord.ext import commands
from discord.ui import Button, View

### Bot info Cog class ###
class bot_info(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot

    ### Suggestion Command ###
    @commands.slash_command(name="suggest", description="Suggest something for the bot")
    async def suggest(self, ctx: discord.ApplicationContext, suggestion: Option(str, description='Suggestion', required=True)):
        bot = self.bot

        await ctx.defer(ephemeral=True)
        embed = discord.Embed(title='Suggestion', description=suggestion + '\n\nPlease vote.', color=discord.Color.green())
        msg = await self.bot.get_channel(bot.config["channels"]["suggestions"]).send(embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await ctx.edit(content='Suggestion sent!')


    ### Bot Command ###
    @commands.slash_command(name='bot', description='Get stats on ben')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bot(self, ctx):

        SupSer = Button(label='Support Server',
                        url='https://discord.gg/KP9fA3wY93')
        topgg = Button(label='Upvote Ben',
                       url='https://top.gg/bot/994213404371861544/vote')
        view = View()
        view.add_item(SupSer)
        view.add_item(topgg)
        members = 0

        for guild in self.bot.guilds:
            members += int(guild.member_count)
            
        if self.bot.userDB.find_one({'_id': ctx.author.id}):
            user = self.bot.userDB.find_one({'_id': ctx.author.id})

            if user['vip'] == 'True':
                msg = discord.Embed(
                    title='Stats', description=f'ping: {round(self.bot.latency * 1000)}ms\nServers in: {str(len(self.bot.guilds))} \nMembers: {members}\nBirthday: July 6th, 2022\nFavorite People: Not you\nBest Command: help', color=discord.Color.gold())
            else:
                msg = discord.Embed(
                    title='Stats', description=f'ping: {round(self.bot.latency * 1000)}ms\nServers in: {str(len(self.bot.guilds))} \nMembers: {members}\nBirthday: July 6th, 2022\nFavorite People: Not you\nBest Command: help')
        await ctx.respond(embed=msg, view=view)

    ### Ping Command ###
    @commands.slash_command(name='ping', description='Get\'s the ping or \"Latency\" of the Bot')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):

        pingC = round(self.bot.latency * 1000)

        if self.bot.userDB.find_one({'_id': ctx.author.id}):
            user = self.bot.userDB.find_one({'_id': ctx.author.id})

            if user['vip'] == 'True':
                msg = discord.Embed(title=f'{pingC}', color=discord.Color.gold())
            else:
                msg = discord.Embed(title=f'{pingC}ms')
        await ctx.respond(embed=msg)


### Setup the Cog ###
def setup(bot: discord.Bot):
    bot.add_cog(bot_info(bot))