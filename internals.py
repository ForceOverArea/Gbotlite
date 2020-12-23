import discord
from discord.utils import get


def check_admin(ctx):
    assert(ctx.author.guild_permissions.administrator)


class discache():
    """
    Represents the settings for this bot.
    
    Settings are stored in an embed window in a hidden 
    server channel dedicated to the bot's settings for
    that specific server. The bot will parse through 
    up to 20 messages in this channel to find the 
    embed window and can convert its 'description'
    contents to dict format for manipulation.

    This class takes a guild argument to access the 
    discord.py cache for reading/writing data.
    """
    def __init__(self, guild):
        self.guild = guild
        self.channel = discord.utils.get(guild.channels, name="gbot-config")


    async def create_cache(self):
        """Create a 'secret' channel to store settings info in"""
        channels = self.guild.channels
        assert("gbot-config" not in [c.name for c in channels])
        overwrites = {
                self.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                self.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
        channel = await self.guild.create_text_channel("gbot-config", overwrites=overwrites)

        await channel.send(
            embed=discord.Embed(
                title=f"Gbot Settings",
                color=discord.Colour.blurple(),
                description="""
                Muterole: None
                Autorole: None
                Welcome Message: None
                """
            )
        )

    
    async def get(self, setting:str):
        """Retrieves a value from the settings window for use by the bot"""
        channel = [c for c in self.guild.channels if c.name == "gbot-config"][0]
        messages = await channel.history(limit=20).flatten()
        settingsMessage = [m for m in messages if m.embeds[0].title == f"Gbot Settings"][0]
        
        settings = settingsMessage.embeds[0].description.split("\n")
        settingsDict = {s.split(":")[0].lstrip():s.split(":")[1].lstrip() for s in settings}

        if setting.lower() == "all":
            return settingsDict
        else:
            return settingsDict[setting]


    async def overwrite(self, settingsDict:dict):
        # get basic dict info and set up variables 
        headers = list(settingsDict.keys())
        details = list(settingsDict.values())
        description_text = ""

        # get the settings message
        channel = [c for c in self.guild.channels if c.name == "gbot-config"][0]
        messages = await channel.history(limit=20).flatten()
        settingsMessage = [m for m in messages if m.embeds[0].title == f"Gbot Settings"][0]

        # convert the dict to a string
        for i in range(len(headers)):
            line = f"{headers[i]}: {details[i]}\n"
            description_text += line

        # change the settings embed's description
        await settingsMessage.edit(
            embed=discord.Embed(
                title=f"Gbot Settings",
                color=discord.Colour.blurple(),
                description=description_text
            )
        )