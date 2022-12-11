### Imports ###
import discord

from discord.ext import commands

### VIP COG###
class vip(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot

    ### Vips command ###
    @commands.slash_command(name='vips', description='Get a list of all fellow VIPS')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def vips(self, ctx):

        if self.bot.userDB.find_one({'_id': ctx.author.id}):
            user = self.bot.userDB.find_one({'_id': ctx.author.id})

            if user['vip'] == True:
                add = ''
                for person in self.bot.userDB.find({'vip': True}):
                    add += '<@' + str(person['_id']) + '> '
                msg = discord.Embed(title='VIPS', description=add)
                await ctx.respond(embed=msg)
            else:
                await ctx.respond('You are not a VIP.', ephemeral=True)

    ### Vip help command ###
    @commands.slash_command(name='vip_help', description='Get info about being a VIP')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def vip_help(self, ctx):

        vip_help_embed = discord.Embed(
            title='VIP HELP', description='All the info on being a VIP')
        vip_help_embed.add_field(
            name='Perks', value='Get access to all VIP commands plus an indicator that you are a vip when Ben Replys', inline=False)
        vip_help_embed.add_field(name='How to unlock', value='Unlock VIP by gettting 5000 xp. You can check XP by using /xp')
        await ctx.respond(embed=vip_help_embed)


### Setup the Cog ###
def setup(bot: discord.Bot):
    bot.add_cog(vip(bot))