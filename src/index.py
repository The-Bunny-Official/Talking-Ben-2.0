### Imports ###
import discord
import json
import os

from pymongo import MongoClient

### Varibles ###
intents: discord.Intents = discord.Intents.default()
intents.members = True
configFile = open("src/config.json", "r")

### bot Varibles ###
bot: discord.Bot = discord.Bot(intents=intents)
bot.config = json.load(configFile)
bot.dbMain = MongoClient(bot.config["mongo"]["URL"])
bot.dbMaster = bot.dbMain[bot.config["mongo"]["MainName"]]
bot.userDB = bot.dbMaster[bot.config["mongo"]["userName"]]
bot.guildDB = bot.dbMaster[bot.config["mongo"]["guildName"]]

if __name__ == "__main__":
    for file in os.listdir("src/Cogs"):
        if file.endswith(".py"):
            bot.load_extension(f'Cogs.' + file[:-3])
    bot.run(bot.config["token"])


