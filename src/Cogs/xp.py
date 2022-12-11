### Imports ###
import discord

from discord import Option
from discord.ext import commands


### Xp Cog ###
class xp(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot

    ### XP Command ###
    @commands.slash_command(name='xp', description='View the amount of xp you have')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def xp(self, ctx, user: Option(discord.Member, description='Member to check', Optional=True) = None):

        await ctx.defer()

        if user == None:
            user = ctx.author

        if self.bot.userDB.find_one({'_id': user.id}):
            xp = self.bot.userDB.find_one({'_id': user.id})['xp']
            await ctx.edit(content=f'{user}\'s xp is {xp}')
        else:
            await ctx.edit(content=f'{user}\'s xp is 0')

    ### Leaderboard Command ###
    @commands.slash_command(name='leaderboard', description='get who has the most XP')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leaderboard(self, ctx):

        await ctx.defer()
        people = ''
        count = 0

        for ex in self.bot.userDB.find().sort('xp', -1):
            people += f"{ex['name']} - {ex['xp']}xp \n"
            count += 1

            if count >= 10:
                break
        msg = discord.Embed(title='**Top 10**', description=f'{people}')
        await ctx.edit(embed=msg)
    

### Setup the Cog ###
def setup(bot: discord.Bot):
    bot.add_cog(xp(bot))