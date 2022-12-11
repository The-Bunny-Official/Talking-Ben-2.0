### Imports ###
import discord
import random

from discord.ext import commands
from discord import Permissions, Option

class fun(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot

    ### Reply Command - Message Command ###
    @commands.message_command(name='Reply To This', default_member_permissions=Permissions(manage_messages=True))
    @commands.guild_only()
    async def reply(self, ctx, message):

        try:
            msg = discord.Embed(title=f'{random.choice(["Yes!!!", "No...", "HoHoHo!!!", "Ugh..."])}', description=f'{message.content}')
            await message.reply(embed=msg)
            await ctx.respond('Success', ephemeral=True)

        except discord.Forbidden:
            print('I cannot post here in this channel')    

    ### Hug Command ###
    @commands.slash_command(name='hug', description='Send a hug to the member you pick')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, member: Option(discord.Member, description='The Member to hug', required=True)):

        msg = discord.Embed(
            description=f'{ctx.author.mention} sends a hug to {member.mention}.')
        await ctx.respond(embed=msg)
        await member.send(f'{ctx.author}, Sent you a hug')

    ### Rock Paper Scissors Command ###
    @commands.slash_command(name="rps", description="Play a game of rock paper scissors")
    async def rps(self, ctx: discord.ApplicationContext, 
        choice: Option(str, description="Rock, Paper, or scissors", choices=["Rock", "Paper", "Scissors"])
    ):
        CompChoice = random.choice(["Rock", "Paper", "Scissors"])
        choice: str = choice

        winnerEmbedComp: discord.Embed = discord.Embed(title="You WIN 🎉", description=f"You chose: {choice}\nThe Computer Chose: {CompChoice}", color=discord.Color.green())
        loserEmbedComp: discord.Embed = discord.Embed(title="You lose 😢", description=f"You chose: {choice}\nThe Computer Chose: {CompChoice}", color=discord.Color.red())
        drawEmbedComp: discord.Embed = discord.Embed(title="Draw 🤝", description=f"You chose: {choice}\nThe Computer Chose: {CompChoice}", color=discord.Color.yellow())

        if CompChoice == "Paper" and choice == "Scissors" or CompChoice == "Rock" and choice == "Paper" or CompChoice == "scissors" and choice == "rock":
            await ctx.respond(embed=winnerEmbedComp)
        elif CompChoice == choice:
            await ctx.respond(embed=drawEmbedComp)
        else:
            await ctx.respond(embed=loserEmbedComp)


### Setup the Cog ###
def setup(bot: discord.Bot):
    bot.add_cog(fun(bot))