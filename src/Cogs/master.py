### Imports ###
import discord
import random

from discord.ext import commands, tasks

### Master Cog ###
class master(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot

    ### Presence Cog ###
    @tasks.loop(seconds=60)
    async def update_presence(self):
        client = self.bot

        options = [f'with 4000+ people', f'in {len(client.guilds)} servers', 'with you', 'with curiosity', 'ping me to chat']
        options2 = ['music', 'music with Curiosity', 'The Bunny#1460 scream', 'pings']
        options3 = ['a race with curiosity', 'a race against my pings']
        options4 = ['a movie', 'a movie with Curiosity', 'The Bunny#1460 run away', 'my pings']
        statuses = [discord.Status.do_not_disturb, discord.Status.online, discord.Status.idle]
        playing = discord.ActivityType.playing
        listening = discord.ActivityType.listening
        #streaming = discord.ActivityType.streaming
        competing = discord.ActivityType.competing
        watching = discord.ActivityType.watching

        activityOp = [{'activity': playing, 'name': random.choice(options)}, 
        {'activity': listening, 'name': random.choice(options2)}, 
        {'activity': competing, 'name': random.choice(options3)}, 
        {'activity': watching, 'name': random.choice(options4)}]
        go_with = random.choice(activityOp)

        await client.change_presence(status=random.choice(statuses), activity=discord.Activity(type=go_with['activity'], name=go_with['name']))

    ### On ready event ###
    @commands.Cog.listener()
    async def on_ready(self):
        print("{0} is online".format(self.bot.user))
        self.update_presence.start()
        
    ### On message event - For handling pings
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        bot: discord.Bot = self.bot
        reply = random.choice(["Yes!!!", "No...", "HoHoHo!!!", "Ugh..."])

        if message.author == self.bot.user: return
        if message.author.bot: return
        if message.mention_everyone: return
        if message.content == None: return

        if bot.user.mentioned_in(message):
            userInfo = {"_id": message.author.id, 'name': message.author.name, 
                        'discriminator': message.author.discriminator, 'xp': 1, 'vip': False}
            
            try:
                if bot.userDB.find_one({"_id": message.author.id}):
                    bot.userDB.update_one({"_id": message.author.id}, {"$inc": {'xp': 1}})
                    user = bot.userDB.find_one({"_id": message.author.id})

                    if user["xp"] >= 5000:
                        bot.userDB.update_one({"_id": message.author.id}, {"$set": {"vip": True}})

                    if bot.userDB.find_one({"_id": message.author.id})["vip"] == True:
                        msg = discord.Embed(title=f"{reply}", description=message.content, color=discord.Color.gold())
                    else:
                        msg = discord.Embed(title=f"{reply}", description=message.content, color=discord.Color.green())
                else:
                    bot.userDB.insert_one(userInfo)
                    msg = discord.Embed(title=f"{reply}", description=message.content, color=discord.Color.green())

                await message.reply(embed=msg)
        
            except discord.Forbidden:
                await message.author.send(embed=discord.Embed(title="An error occurred", description="I do not have permission to send messages in the channel that you pinged me in.", color=discord.Color.red()))
                return

            except discord.NotFound:
                return

            except Exception as err:
                await message.reply(embed=discord.Embed(title="An error just occurred", description="This was caused by something unknown, but not to worry. Our devs has already seen this error and are working on a fix.", color=discord.Color.red()))
                await bot.get_channel(bot.config["channels"]["error"]).send(err)
                return


### Setup the Cog ###
def setup(bot: discord.Bot):
    bot.add_cog(master(bot))