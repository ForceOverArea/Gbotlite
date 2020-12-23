import discord, os
from discord.utils import get
from discord.ext import commands, tasks
from internals import *

# this prefix is being picked as it simplifies later code without much effort.
intents = discord.Intents.default()
intents.members = True
bot = commands.AutoShardedBot(command_prefix="g.", intents=intents)


# Event listeners appear below this line


@bot.event
async def on_ready():
    # set bot presence
    await bot.change_presence(
        status=discord.Status.online, 
        activity=discord.Game(
            name="g.help"
        ))
    # matches the bot's nick to its username in all servers.
    for guild in bot.guilds:
        try:
            member = guild.get_member(bot.user.id)
            await member.edit(nick=bot.user.name)
        except:
            pass
    print(f"Successful login as {bot.user.name}\nGbot4 ready for action!")


@bot.event
async def on_guild_join(guild):
    """Create a settings channel on server join"""
    try:
        await discache(guild).create_cache()
        await discache(guild).channel.send(
            delete_after=60,
            embed=discord.Embed(
                title=f"Hi there, {guild.owner}!",
                description="This channel stores my settings specific to your server. Feel free to delete it if you don't want or need these features.",
                colour=discord.colour.blurple()
            )
        )
    except:
        await guild.owner.send(f"Hi {guild.owner}. Currently I can't save settings for your server, {guild}. Please type `g.newCache` in a channel I can see to create settings for your server. Thank you!", delete_after=60)


# Listed commands appear below this line


@bot.command()
async def newCache(ctx):
    
    await ctx.message.delete()

    check_admin(ctx)
    try:
        await discache(ctx.guild).create_cache()
    except:
        await ctx.send(
            delete_after=10,
            embed=discord.Embed(
                title=":warning: A server settings channel already exists",
                color=discord.Colour.blurple()
            )
        )


bot.remove_command("help")
@bot.command()
async def help(ctx, page=1):
    helpMessages = ["""
            **g.youtube <search...>**
            Searches YouTube and links the first result in chat.

            **g.wikipedia <search...>**
            Searches Wikipedia and provides a sample of the article in chat if possible.
            This will always provide a link to Wikipedia even if a specific result isn't found.

            **g.avatar <user>**
            Displays the given user's avatar in a larger window.

            **g.calculator <expression...>**
            Evaluates a given mathematical expression.
            Using 'ans' in your expression will use the last calculated value in its place.

            **g.reminder <role> <hours> <message...>**
            Pings a role with a given message after a specified number of hours have passed.
            Server admin required.
            """,
            """
            **g.newCache <None>**
            Creates a new settings cache. Server admin required.

            **g.role <user> <roles...>**
            Assigns a list of roles to user. Server admin required.

            **g.mute <user> <minutes>**
            Mutes a user for some number of minutes. 
            This may create a new role. Server admin required.

            **g.unmute <user>**
            Unmutes a muted user. Server admin required.

            **g.optin <role> <text...>**
            Creates an embed window containing specified text. 
            Ordinary server members can react to this message to gain the given role.
            Server admin required.

            **g.autorole <role>**
            Sets an existing role as the server's autorole.
            This role will be given automatically to new members. 
            Server admin required.

            **g.muterole <role>**
            Sets an existing role as the server's muterole.
            This role will be used by the 'g.mute' command. 
            Server admin required.

            **g.welcome <message...>**
            Sets a welcome message to ping new members with. 
            This requires the following to work:
            - Server admin on the part of the user
            - An existing settings cache
            - A designated system messages channel for the server 
            """,
            """
            **g.8ball <question...>**
            Does what a magic 8-ball does.

            **g.attack <victim...>**
            Prints a statement of your valiant assault on your most hated foe(s).

            **g.choose <list...>**
            Selects an item from a given comma-deliminated list.
            If the list argument is 'server' or 'voice', the selection will be a server member from one of those two respective groups.
            """]
    
    await ctx.send(
        embed=discord.Embed(
            title=":bookmark: Command help:",
            description=helpMessages[page-1],
            colour=discord.Colour.blurple()
        ).set_footer(text="type 'g.help' followed by 1, 2, or 3 to view different pages.")
    )


# Hidden/Dev commands appear below this line


@bot.command(hidden=True)
@commands.is_owner()
async def ping(ctx):
    """Prints "Pong!" in chat to indicate that the bot is operating normally."""
    await ctx.send("Pong!")


@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    """Loads a cog"""
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} successfully.")


@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    """Unloads a cog"""
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension} successfully.")
    

# all cog files are automatically loaded here
for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"loaded cog: {filename[:-3]}")


with open("token.txt", "r") as file:
    bot.run(file.read())