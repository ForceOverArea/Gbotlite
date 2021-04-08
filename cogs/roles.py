import asyncio, discord
from discord.ext import commands
from discord.utils import get
from internals import *

class roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener() # provides functionality for opt-in roles
    async def on_raw_reaction_add(self, payload):
        member = payload.member

        if member.id == self.bot.user.id:
            return

        channel = discord.utils.get(member.guild.channels, id=payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        id_no = int(message.embeds[0].footer.text)
        role = member.guild.get_role(id_no)
        
        if role not in member.roles:
            await member.add_roles(role)
        else:
            await member.remove_roles(role)
        await message.remove_reaction(payload.emoji, member)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("new member has joined a server")
        try:
            id_no = await discache(member.guild).get("Autorole")
            ar = member.guild.get_role(int(id_no))
            await member.add_roles(ar)
        except:
            print("no autorole given to member")
        
        try:
            welcome = await discache(member.guild).get("Welcome Message")
            welcome = welcome.replace("[member]", member.mention)
            await member.guild.system_channel.send(welcome)
        except:
            print("no welcome message for member")


    @commands.command()
    async def role(self, ctx, user:discord.Member, *roles):
        """Alters a list of given roles for a single specified user"""
        check_admin(ctx)
        history=False

        for role in roles:
            #get the role object
            roleObj = discord.utils.get(ctx.guild.roles, name=role)

            #sends a tidy warning message if the role doesn't exist
            if roleObj == None:
                await ctx.send(
                    delete_after=10,
                    embed=discord.Embed(
                        title=f":warning: could not find role: '{role}' in this server",
                        color=discord.Colour.gold()
                    )
                )
                continue

            if roleObj not in user.roles:
                await user.add_roles(roleObj)
                history=True
            if roleObj in user.roles:
                await user.remove_roles(roleObj)
                history=True

        if history: # send a success message if any roles were modified
            await ctx.send(
                embed=discord.Embed(
                    title=f":white_check_mark: {user}'s roles updated successfully",
                    color=discord.Colour.teal()
                )
            )


    @commands.command()
    async def mute(self, ctx, user:discord.Member, minutes=30.0):

        check_admin(ctx)

        # get the muterole id from the discache object
        mySettings = discache(ctx.guild)
        settingsDict = await mySettings.get("all")
        id_no = await mySettings.get("Muterole")
        
        # get the muterole object if possible or create one
        try:
            muterole = ctx.guild.get_role(int(id_no))       
        except:
            muterole = await ctx.guild.create_role(name="Muted")
            
            # update the discache embed to include new muterole
            settingsDict["Muterole"] = muterole.id
            await mySettings.overwrite(settingsDict)
             
        # update the muterole permissions for any new channels
        for channel in ctx.guild.channels:
            if channel.type == discord.ChannelType.text:
                await channel.set_permissions(
                    target=muterole,
                    overwrite=discord.PermissionOverwrite(send_messages=False)
                )
            if channel.type == discord.ChannelType.voice:
                await channel.set_permissions(
                    target=muterole,
                    overwrite=discord.PermissionOverwrite(speak=False)
                )
        
        # mute the user for a fixed amount of time
        await user.add_roles(muterole)
        await ctx.send(
            embed=discord.Embed(
                title=f":mute: {user} was muted by {ctx.author} for {minutes} minutes",
                colour=discord.Colour.blurple()
            )
        )
        
        await asyncio.sleep(minutes*60)
        
        await user.remove_roles(muterole)
        


    @commands.command()
    async def unmute(self, ctx, user:discord.Member):

        check_admin(ctx)

        mySettings = discache(ctx.guild)
        id_no = await mySettings.get("Muterole")
        muterole = ctx.guild.get_role(int(id_no))
        await user.remove_roles(muterole) 
        await ctx.send(
            embed=discord.Embed(
                title=f":speaker: {user} was unmuted",
                colour=discord.Colour.blurple()
            )
        )

    @commands.command()
    async def optin(self, ctx, role:discord.Role, *text):
        """Creates an embed message that allows users to assign themselves a role"""
        
        check_admin(ctx)

        text = " ".join(text)
        message = ctx.message
        await message.delete()

        if role == None:
            await ctx.send(
                delete_after=5,
                embed=discord.Embed(
                    title=f":warning: could not find the given role in this server",
                    colour=discord.colour.gold()
                )
            )
            return

        optin = await ctx.send(
            embed = discord.Embed(
                title = text,
                description = "Click the :thumbsup: reaction below to toggle",
                colour = discord.Color.blurple()
            ).set_footer(
                text=role.id
            )
        )
        await optin.add_reaction("\U0001F44D")


    @commands.command(aliases=['ar'])
    async def autorole(self, ctx, role:discord.Role):
        check_admin(ctx)

        mySettings = discache(ctx.guild)

        params = await mySettings.get("all")
        params["Autorole"] = role.id
        await mySettings.overwrite(params)


    @commands.command(aliases=['mr'])
    async def muterole(self, ctx, role:discord.Role):

        check_admin(ctx)

        mySettings = discache(ctx.guild)

        params = await mySettings.get("all")
        params["Muterole"] = role.id
        await mySettings.overwrite(params)

    
    @commands.command(aliases=['wm'])
    async def welcome(self, ctx, *message):

        check_admin(ctx)

        message = " ".join(message)
        mySettings = discache(ctx.guild)

        params = await mySettings.get("all")
        params["Welcome Message"] = message
        await mySettings.overwrite(params)


def setup(bot):
    bot.add_cog(roles(bot))
