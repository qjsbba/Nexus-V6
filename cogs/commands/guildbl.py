import discord
from discord.ext import commands
import json
from utils.Tools import *
from discord import *
from utils.config import OWNER_IDS, No_Prefix
import typing
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from core import Cog, Astroz, Context
from typing import Optional

class bl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blacklisted_guilds = []
        self.load_blacklist()

    def load_blacklist(self):
        try:
            with open('db/guildbl.json', 'r') as file:
                self.blacklisted_guilds = json.load(file)
                if not isinstance(self.blacklisted_guilds, list):
                    self.blacklisted_guilds = []
        except FileNotFoundError:
            self.blacklisted_guilds = []

    def save_blacklist(self):
        with open('db/guildbl.json', 'w') as file:
            json.dump(self.blacklisted_guilds, file, indent=4)

    @commands.group(name="guildbl",
                    help="add guild in blacklist",
                    invoke_without_command=True,
                    usage="add guild in blacklist")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _guildbl(self, ctx: Context):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
  
    @_guildbl.command()
    @commands.is_owner()
    async def add(self, ctx, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        if guild:
            if guild.id in self.blacklisted_guilds:
                await ctx.send("<:hacker_admin_cross:1271209737647558819> | This guild is already blacklisted.")
            else:
                self.blacklisted_guilds.append(guild.id)
                self.save_blacklist()
                await ctx.send(f"<:hacker_tick:1271209580793167925> | Successfully Guild {guild.name} - {guild.id} has been blacklisted.")
                if guild.id in [g.id for g in self.bot.guilds]:
                    await guild.leave()
        else:
            await ctx.send("<:hacker_admin_cross:1271209737647558819> | Invalid guild ID.")

    @_guildbl.command()
    @commands.is_owner()
    async def remove(self, ctx, guild_id: int):
        if guild_id in self.blacklisted_guilds:
            self.blacklisted_guilds.remove(guild_id)
            self.save_blacklist()
            await ctx.send("<:hacker_tick:1271209580793167925> | Successfully Guild has been removed from the blacklist.")
        else:
            await ctx.send("<:hacker_admin_cross:1271209737647558819> | This guild is not blacklisted.")


    @_guildbl.command()
    @commands.is_owner()
    async def show(self, ctx):
        self.load_blacklist()
        if self.blacklisted_guilds:
            guilds = '\n'.join(str(guild_id) for guild_id in self.blacklisted_guilds)

            entries = [
                f"`[{i}]` | `[{guild_id}]`"
                for i, guild_id in enumerate(self.blacklisted_guilds, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                description="",
                title=f"Server Blacklist of Nexus - {len(self.blacklisted_guilds)}",
                color=0x2f3136,
                per_page=10),
                                  ctx=ctx)
            await paginator.paginate()
        else:
            await ctx.send("There are no blacklisted guilds.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild.id in self.blacklisted_guilds:
            await guild.leave()

def setup(bot):
    bot.add_cog(bl(bot))
