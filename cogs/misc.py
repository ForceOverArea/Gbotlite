import asyncio, discord, json, requests, youtube_search as yts
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.utils import get
from internals import *

class misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['yt'])
    async def youtube(self, ctx, query):
        """Search youtube and post the first result in chat"""
        query = " ".join(query)
        try:
            #get url suffix from search terms
            video_info = yts.YoutubeSearch(query, max_results=1).to_dict()

            #construct the url
            url = "https://www.youtube.com" + video_info[0]["url_suffix"]

            await ctx.send(url)

        except:
            await ctx.send(
                delete_after=10,
                embed=discord.Embed(
                    title=":confused: Couldn't post the video in chat for some reason",
                    colour=discord.Colour.gold()
                )
            )


    @commands.command(aliases=["wp"])
    async def wikipedia(self, ctx, *search_terms:str):
        
        def search_wikipedia(query):
    
            #replace spaces with _ as per wikipedia url format
            query = query.replace(" ", "_")

            #construct url of results
            base_url = "https://en.wikipedia.org/wiki/"
            search_url = base_url + query

            #get html and find all paragraphs
            article = requests.get(search_url)
            soup = BeautifulSoup(article.text, "html.parser")
            text = soup.findAll('p')

            #return blocks of text:
            chunks = [search_url]
            for paragraph in text:
                if len(str(paragraph.get_text()).replace(" ","").replace("\n","")) > 100:
                    chunks.append(paragraph.get_text().replace("  ","").replace("\n",""))
    
            return chunks
        
        search_terms = "_".join(search_terms)

        article = search_wikipedia(search_terms)[0:3]
        text = "\n\n".join(article[1:3])
        await ctx.send(
            embed=discord.Embed(
                title="According to Wikipedia:",
                colour=discord.Colour.blurple(),
                description=f"{text} \n\nFor further reading: {article[0]}"
            )
        )


    @commands.command()
    async def avatar(self, ctx, user:discord.User):
        """Show a given user's avatar"""
        try:
            await ctx.send(
                embed=discord.Embed(
                    title=f"{user}'s avatar:",
                    colour=discord.Colour.blurple()
                ).set_image(url=user.avatar_url)
            )
        except:
            await ctx.send(f"Looks like {user} has no avatar set.")


    @commands.command(aliases=['calc'])
    async def calculator(self, ctx, *expression:str):
        global ans

        #create ans variable if it doesn't exist
        try:
            ans
        except:
            ans = {}
            
        #construct the actual expression
        try:
            expression = "".join(expression).replace("ans",f"{ans[ctx.message.author.id]}")
        except:
            expression = "".join(expression).replace("ans","0")

        #try evaluating a normal expression
        try:
            ans[ctx.message.author.id] = eval(expression)
            await ctx.send(
                embed=discord.Embed(
                    title = f"expression: `{expression}`\nans: `{ans[ctx.message.author.id]}`",
                    colour=discord.Colour.blurple()
                )
            )
        except:
            await ctx.send(
                embed=discord.Embed(
                    title=":confused: Sorry, I couldn't calculate that",
                    colour=discord.Colour.gold()
                )
            )


    @commands.command(aliases=['cvrt'])
    async def convert(self, ctx, fro:str, to:str, value=1):
        with open("EES.json", "r") as file:
            sheet = json.load(file)

        for category in sheet:
            if (fro in sheet[category]) and (to in sheet[category]):
                conversion_factor = float(sheet[category][fro]/sheet[category][to])
                conversion = value*conversion_factor

        await ctx.send(f"{round(conversion, 5)} {to} per {value} {fro}")


    @commands.command()
    async def reminder(self, ctx, group:discord.Role, hours:float, *message):
       
        check_admin(ctx)
        message = " ".join(message)

        await ctx.send(
            delete_after=30,
            embed=discord.Embed(
                title=f":white_check_mark: Reminder set for {group.name}",
                colour=discord.Colour.green(),
                description=f"""
                channel: {ctx.channel.mention} 
                wait time time: {hours} hours
                reminder: '{message}'
                """
            )
        )
        await asyncio.sleep(hours*3600)
        await ctx.send(f"Reminder for {group.mention}: {message}")


def setup(bot):
    bot.add_cog(misc(bot))