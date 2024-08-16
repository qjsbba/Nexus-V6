from __future__ import annotations
from discord.ext import commands
from utils.Tools import *
from discord import *
from utils.config import OWNER_IDS, No_Prefix
import json, discord
import typing
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from core import Cog, Astroz, Context
from typing import Optional

        

class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

        
    @commands.command(name="slist")
    @commands.is_owner()
    async def _slist(self, ctx):
        hasanop = ([hasan for hasan in self.client.guilds])
        hasanop = sorted(hasanop,
                         key=lambda hasan: hasan.member_count,
                         reverse=True)
        entries = [
            f"`[{i}]` | [{g.name}](https://discord.com/channels/{g.id}) - {g.member_count}"
            for i, g in enumerate(hasanop, start=1)
        ]
        paginator = Paginator(source=DescriptionEmbedPaginator(
            entries=entries,
            description="",
            title=f"Server List of Nexus - {len(self.client.guilds)}",
            color=0x2f3136,
            per_page=10),
                              ctx=ctx)
        await paginator.paginate()



    @commands.command(name="restart", help="Restarts the client.")
    @commands.is_owner()
    async def _restart(self, ctx: Context):
        await ctx.reply("**<:Nexus_tick:1144687280540369018> Restarting.. <a:loadhearts:1144989282977710240>**")
        restart_program()

    @commands.command(name="sync", help="Syncs all database.")
    @commands.is_owner()
    async def _sync(self, ctx):
        await ctx.reply("<a:loadhearts:1144989282977710240> Syncing...", mention_author=False)
        with open('db/events.json', 'r') as f:
            data = json.load(f)
        for guild in self.client.guilds:
            if str(guild.id) not in data['guild']:
                data['guilds'][str(guild.id)] = 'on'
                with open('db/events.json', 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                pass
        with open('db/config.json', 'r') as f:
            data = json.load(f)
        for op in data["guilds"]:
            g = self.client.get_guild(int(op))
            if not g:
                data["guilds"].pop(str(op))
                with open('db/config.json', 'w') as f:
                    json.dump(data, f, indent=4)

    @commands.group(name="blacklist",
                    help="let's you add someone in blacklist",
                    aliases=["bl"])
    @commands.is_owner()
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            with open("db/blacklist.json") as file:
                blacklist = json.load(file)
                entries = [
                    f"`[{no}]` | <@!{mem}> (ID: {mem})"
                    for no, mem in enumerate(blacklist['ids'], start=1)
                ]
                paginator = Paginator(source=DescriptionEmbedPaginator(
                    entries=entries,
                    title=
                    f"List of Blacklisted users of Nexus - {len(blacklist['ids'])}",
                    description="",
                    per_page=10,
                    color=0x2f3136),
                                      ctx=ctx)
                await paginator.paginate()

    @blacklist.command(name="add")
    @commands.is_owner()
    async def blacklist_add(self, ctx: Context, member: discord.Member):
        try:
            with open('db/blacklist.json', 'r') as bl:
                blacklist = json.load(bl)
                if str(member.id) in blacklist["ids"]:
                    embed = discord.Embed(
                        title="Error!",
                        description=f"{member.name} is already blacklisted",
                        color=discord.Colour(0x2f3136))
                    await ctx.reply(embed=embed, mention_author=False)
                else:
                    add_user_to_blacklist(member.id)
                    embed = discord.Embed(
                        title="Blacklisted",
                        description=f"Successfully Blacklisted {member.name}",
                        color=discord.Colour(0x2f3136))
                    with open("db/blacklist.json") as file:
                        blacklist = json.load(file)
                        embed.set_footer(
                            text=
                            f"There are now {len(blacklist['ids'])} users in the blacklist"
                        )
                        await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(title="Error!",
                                  description=f"An Error Occurred",
                                  color=discord.Colour(0x2f3136))
            await ctx.reply(embed=embed, mention_author=False)

    @blacklist.command(name="remove")
    @commands.is_owner()
    async def blacklist_remove(self, ctx, member: discord.Member = None):
        try:
            remove_user_from_blacklist(member.id)
            embed = discord.Embed(
                title="User removed from blacklist",
                description=
                f"<:Nexus_tick:1144687280540369018> | **{member.name}** has been successfully removed from the blacklist",
                color=0x2f3136)
            with open("db/blacklist.json") as file:
                blacklist = json.load(file)
                embed.set_footer(
                    text=
                    f"There are now {len(blacklist['ids'])} users in the blacklist"
                )
                await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(
                title="Error!",
                description=f"**{member.name}** is not in the blacklist.",
                color=0x2f3136)
            embed.set_thumbnail(url=f"{self.client.user.display_avatar.url}")
            await ctx.reply(embed=embed, mention_author=False)

    @commands.group(
        name="np",
        help="Allows you to add someone in no prefix list (owner only command)"
    )
    @commands.is_owner()
    async def _np(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_np.command(name="list")
    @commands.is_owner()
    async def np_list(self, ctx):
        with open("db/info.json") as f:
            np = json.load(f)
            nplist = np["np"]
            npl = ([await self.client.fetch_user(nplu) for nplu in nplist])
            npl = sorted(npl, key=lambda nop: nop.created_at)
            entries = [
                f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) (ID: {mem.id})"
                for no, mem in enumerate(npl, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"No Prefix of Nexus - {len(nplist)}",
                description="",
                per_page=10,
                color=0x2f3136),
                                  ctx=ctx)
            await paginator.paginate()


    @commands.command(name="owners")
    @commands.is_owner()
    async def own_list(self, ctx):
        with open("db/info.json") as f:
            np = json.load(f)
            nplist = np["OWNER_IDS"]
            npl = ([await self.client.fetch_user(nplu) for nplu in nplist])
            npl = sorted(npl, key=lambda nop: nop.created_at)
            entries = [
                f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) (ID: {mem.id})"
                for no, mem in enumerate(npl, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Owner list of Nexus - {len(nplist)}",
                description="",
                per_page=10,
                color=0x2f3136),
                                  ctx=ctx)
            await paginator.paginate()


    
    @_np.command(name="add", help="Add user to no prefix")
    @commands.is_owner()
    async def np_add(self, ctx, user: discord.User):
        with open('db/info.json', 'r') as idk:
            data = json.load(idk)
        np = data["np"]
        if user.id in np:
            embed = discord.Embed(
                description=
                f"**The User You Provided Already In My No Prefix**",
                color=0x2f3136)
            await ctx.reply(embed=embed)
            return
        else:
            data["np"].append(user.id)
        with open('db/info.json', 'w') as idk:
            json.dump(data, idk, indent=4)
            embed1 = discord.Embed(
                description=
                f"<:Nexus_tick:1144687280540369018> | Added no prefix from {user} for all",
                color=0x2f3136)

            await ctx.reply(embed=embed1)
    
    @_np.command(name="remove", aliases=["rmv"], description="Remove user from no prefix")
    async def np_remove(self, ctx: Context, user: discord.User):
     with open('db/info.json', 'r') as idk:
       data = json.load(idk)
     np = data["np"]
     if user.id not in np:
       await ctx.send(embed=discord.Embed(description=f"**The User You Provided He Dosen't In My No Prefix**",color=0x2f3136))
     else:
       data["np"].remove(user.id)
     with open('db/info.json', 'w') as idk:
       json.dump(data, idk, indent=4)
       await ctx.send(embed=discord.Embed(description=f"<:Nexus_tick:1144687280540369018> | Removed no prefix from {user.name} for all",color=0x2f3136))
       
    #@commands.command()
    #async def dm(self, ctx, user: discord.User, *, message: str):
        #""" DM the user of your choice """
        #try:
            #await user.send(message)
            #await ctx.send(f"<:Nexus_tick:1144687280540369018> | Successfully Sent a DM to **{user}**")
        #except discord.Forbidden:
            #await ctx.reply("<:icons_exclamation:1144986614804787310> This user might be having DMs blocked or it's a bot account...")           



    @commands.group()
    @commands.is_owner()
    async def change(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))
            
            
    @change.command(name="nickname")
    @commands.is_owner()
    async def change_nickname(self, ctx, *, name: str = None):
        """ Change nickname. """
        try:
            await ctx.guild.me.edit(nick=name)
            if name:
                await ctx.send(f"<:Nexus_tick:1144687280540369018> | Successfully changed nickname to **{name}**")
            else:
                await ctx.send("<:Nexus_tick:1144687280540369018> | Successfully removed nickname")
        except Exception as err:
            await ctx.send(err)



    @commands.command()
    @commands.is_owner()
    async def globalban(self, ctx, *, user: discord.User = None):
        if user is None:
            return await ctx.send(
                "You need to define the user"
            )
        for guild in self.client.guilds:
            for member in guild.members:
                if member == user:
                    await user.ban(reason="...")
               
        
    @commands.is_owner()
    @commands.command()
    async def leaveguild(self, ctx, guild: discord.Guild = None):
        if ctx.author.id not in [1078333867175465162, 1139570279748739093,1181256087081603116]:
            await ctx.send(embed=discord.Embed(color=0x2f3136, description="<:Nexus_cross:1144687282176147629> | This command can only be executed by my developer"))
            return

        if guild is None:
            await ctx.send(embed=discord.Embed(description="<:Nexus_cross:1144687282176147629> | Please provide me a server id", color=0x2f3136))
        else:
            await ctx.send(embed=discord.Embed(description="<:Nexus_tick:1144687280540369018> | Successfully Left The Guild.", color=0x2f3136))
            await guild.leave()


    @commands.is_owner()
    @commands.command(help="Change the bot's status")
    async def changestatus(self, ctx: commands.Context, *, status: str):
        await self.client.change_presence(
            activity=discord.Game(name=status),
            status=discord.Status.online
        )
        await ctx.message.add_reaction('<:icons_dev2_3:1144991170028638261>') 


    @commands.is_owner()
    @commands.command(help="Change the bot's status to listening")
    async def listening(self, ctx: commands.Context, *, status: str):
        await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
        await ctx.message.add_reaction('<:icons_dev2_3:1144991170028638261>') 
            
            
        
        await ctx.send(embed=discord.Embed(description="<:Nexus_tick:1144687280540369018> | Successfully Changed the bot's presence to Listening", color=0x2f3136))


    @commands.is_owner()
    @commands.command(help="Change the bot's status to streaming")
    async def streaming(self, ctx: commands.Context, *, status: str):
        await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=status, url = "https://dsc.gg/cosmic-codez"))
        await ctx.message.add_reaction('<:icons_dev2_3:1144991170028638261>') 
            
            
        
        await ctx.send(embed=discord.Embed(description="<:Nexus_tick:1144687280540369018> | Successfully Changed the bot's presence to Streaming.", color=0x2f3136))

    @commands.is_owner()
    @commands.command(help="Change the bot's status to watching")
    async def watching(self, ctx: commands.Context, *, status: str):
        await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        await ctx.message.add_reaction('<:icons_dev2_3:1144991170028638261>') 
      
            
        
        await ctx.send(embed=discord.Embed(description="<:Nexus_tick:1144687280540369018> | Successfully Changed the bot's presence to Watching.", color=0x2f3136))


    @commands.is_owner()
    @commands.command(help="Change the bot's status to playing")
    async def playing(self, ctx: commands.Context, *, status: str):
        await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status))
        await ctx.message.add_reaction('<:icons_dev2_3:1144991170028638261>')             
            
        
        await ctx.send(embed=discord.Embed(description="<:Nexus_tick:1144687280540369018> | Successfully Changed the bot's presence to Playing.", color=0x2f3136))


    @commands.is_owner()
    @commands.command(help="Change the bot's status to competing")
    async def competing(self, ctx: commands.Context, *, status: str):
        await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=status))
        await ctx.message.add_reaction('<:icons_dev2_3:1144991170028638261>')             
            
        
        await ctx.send(embed=discord.Embed(description="<:Nexus_tick:1144687280540369018> | Successfully Changed the bot's presence to Competing.", color=0x2f3136))         

    @commands.is_owner()
    @commands.command(help="Change the bot's status to idle")
    async def idle(self, ctx):
        await ctx.bot.change_presence(status=discord.Status.idle)
        await ctx.message.add_reaction('<:icons_dev2_3:1144991170028638261>') 
      
        await ctx.send(embed=discord.Embed(description="<:Nexus_tick:1144687280540369018> | Successfully changed the bot's status to Idle.", color=0x2f3136))

    @commands.is_owner()
    @commands.command(help="Change the bot's status to dnd")
    async def dnd(self, ctx):
        await ctx.bot.change_presence(status=discord.Status.dnd)
        await ctx.message.add_reaction('<:icons_dev2_3:1144991170028638261>') 
      
        await ctx.send(embed=discord.Embed(description="<:Nexus_tick:1144687280540369018> | Successfully changed the bot's status to Dnd.", color=0x2f3136))

    @commands.is_owner()
    @commands.command(help="Change the bot's status to online")
    async def online(self, ctx):
        await ctx.bot.change_presence(status=discord.Status.online)
        await ctx.message.add_reaction('<:icons_dev2_3:1144991170028638261>') 
      
        await ctx.send(embed=discord.Embed(description="<:Nexus_tick:1144687280540369018> | Successfully changed the bot's status to Online.", color=0x2f3136))
