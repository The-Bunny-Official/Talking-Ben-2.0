### Imports ###
import discord

from pymongo import MongoClient
from discord.ext import commands
from discord import Permissions, Option

### Welcome Cog ###
class welcome(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot

    ### Welcome Setup commands ###
    @commands.slash_command(name="welcome_setup", description="Setup welcome messages within your server.", default_member_permissions=Permissions(manage_guild=True))
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def welcome_setup(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel, description="Channel to send welcome messages to", required=True), message: Option(str, description="Custom message, use {0} to ping the member", required=False)):
        if message == None or message == "":
            message = "Hello!!! Welcome {0}"
        data = {"_id": ctx.guild.id, "RecieveWelcome": True, "WelcomeChannel": channel.id, "WelcomeMessage": message}
        db = self.bot.guildDB
        bot = self.bot
        await ctx.defer()
        
        if db.find_one({"_id": data["_id"]}):
            if db.find_one({"_id": data["_id"], "RecieveWelcome": True, "WelcomeChannel": channel.id}):
                db.delete_one({"_id": data["_id"]})
                await ctx.edit(embed=discord.Embed(title="Welcome Messages Disabled", description=f"Channel <#{channel.id}> will no longer recieve welcome messages", color=discord.Color.green()))
                return
        
        else:
            db.insert_one(data)

            try:
                await channel.send(embed=discord.Embed(title="Welcome Messages", description="This channel will now recieve welcome messages", color=discord.Color.green()))
                await ctx.edit(embed=discord.Embed(title="Welcome Messages", description="Succefully setup welcome messages", color=discord.Color.green()))
            
            except commands.MissingPermissions:
                await ctx.edit(embed=discord.Embed(title="Welcome Messages Failure", description="The welcome messages failed because I do not have the proper permission to send messages inn that channel.", color=discord.Color.red()))

            except Exception as err:
                await ctx.edit(embed=discord.Embed(title="An error just occurred", description="This was caused by something unknown, but not to worry. Our devs has already seen this error and are working on a fix.", color=discord.Color.red()))
                await bot.get_channel(bot.config["channels"]["error"]).send(err)
                return

    ### Handle when a member joins ###
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        db = self.bot.guildDB
        if db.find_one({"_id": member.guild.id, "RecieveWelcome": True}):
            channel: int = db.find_one({"_id": member.guild.id})["WelcomeChannel"]
            message: str = db.find_one({"_id": member.guild.id})["WelcomeMessage"]
            await self.bot.get_channel(channel).send(message.format(member.mention))


### Setup the Cog ###
def setup(bot: discord.Bot):
    bot.add_cog(welcome(bot))