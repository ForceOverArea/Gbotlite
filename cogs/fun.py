import discord, random
from discord.ext import commands


class fun(commands.Cog):


    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx):
        """Does what a magic 8-ball does
            Prints a random yes/no message in response to a question
        """
        yes = [
        "Probably", 
        "Seems likely", 
        "I don't see why not", 
        "Yes", 
        "Highly likely", 
        "As sure as the sun rises in the east"
        ]

        no = [
        "I don't think so", 
        "Not gonna happen", 
        "No", 
        "Probably not lol", 
        "Your chances are slim", 
        "As sure as the sun rises in the west"
        ]

        messages = yes + no
        await ctx.send(random.choice(messages))

    
    @commands.command()
    async def attack(self, ctx, *victim):
        """Attack another server member in chat
            Prints a message saying that you attacked another server member in some way
        """
        victim = " ".join(victim)
        weapons = [
            "a garden rake", 
            "an old hoe", 
            "a tennis racket", 
            "the Wardcliff Coil", 
            "the power of God himself", 
            "a stuffed animal", 
            "biological warfare", 
            "an enchanted diamond sword",
            "justice rained from above",
            "EVA Unit 01's Prog knife",
            "an N-2 mine",
            "the Terrablade",
            "the exploding bodies necromancer skill from Diablo III",
            "poor music taste",
            "Gjallarhorn as if they were doing a Crota's end run",
            "a blue shell",
            "the accusation that their favorite song originated from Tik Tok",
            "the BFG",
            "the harsh reality that we'll all die someday and everything we do and obtain is meaningless",
            "Metagross's choice banded quad-boosted meteor mash stacked with a critical hit",
            "absolutely nothing",
            "their bare hands",
            "cyber warfare"
            ]
        await ctx.send(f"{ctx.message.author.mention} attacked {victim} with {random.choice(weapons)}")


    @commands.command()
    async def choose(self, ctx, *items):
        """Choose a random item from a given list
            using 'm' or 'member' instead of a list will default to picking a random server member.
        """

        items = " ".join(items).split(",")
        
        if items[0] in ['server','members','member']:
            selection = self.bot.user.mention
            while selection == self.bot.user.mention:
                selection = random.choice(ctx.guild.members).mention
        elif items[0] in ['voice','vc','channel']:
            selection = self.bot.user.mention
            while selection == self.bot.user.mention:
                selection = random.choice(ctx.message.author.voice.channel.members).mention
        else:
            selection = random.choice(items)
        
        await ctx.send(f"{selection} has been chosen.")

            
def setup(bot):
    bot.add_cog(fun(bot))