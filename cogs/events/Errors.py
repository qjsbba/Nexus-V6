import discord
import json
from discord.ext import commands
from core import Astroz, Cog, Context
from utils.Tools import *


class Errors(Cog):
    def __init__(self, client: Astroz):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        with open('db/ignore.json', 'r') as file:
            randi = json.load(file)
        with open('db/iuser.json', 'r') as file:
            randi2 = json.load(file)
        with open('db/ibypass.json', 'r') as file:
            randi1 = json.load(file)
        with open('db/blacklist.json', 'r') as file:
            data = json.load(file)

        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
        elif isinstance(error, commands.CheckFailure):
            if str(ctx.author.id) in data["ids"]:
                embed = discord.Embed(
                    title="<:Nexus_cross:1144687282176147629> Blacklisted",
                    description="You are blacklisted from using my commands.\nIf you think that it is a mistake, you can appeal in our support server by clicking [here](https://discord.gg/zvU2mGPa6Y)",
                    color=0x2f3136
                )
                await ctx.reply(embed=embed, mention_author=False)
            if str(ctx.channel.id) in randi["ids"]:
                hacker44 = discord.Embed(
                    color=0x2f3136,
                    description="This channel is in the ignored channel list. Try my commands in another channel.",
                )
                await ctx.reply(embed=hacker44, delete_after=10)
            guild_id = str(ctx.guild.id)
            if guild_id in randi2["guilds"] and str(ctx.author.id) in randi2["guilds"][guild_id]["iuser"]:

                hacker41 = discord.Embed(
                    color=0x2f3136,
                    description=f"You are set as an ignored user for {ctx.guild.name}.\nTry my commands or modules in another guild."
                )
                await ctx.reply(embed=hacker41, delete_after=10)

        elif isinstance(error, commands.NoPrivateMessage):
            hacker = discord.Embed(
                color=0x2f3136,
                description="You can't use my commands in DMs",
                timestamp=ctx.message.created_at
            )
       #     hacker.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=hacker, delete_after=20)
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send_help(ctx.command)
        elif isinstance(error, commands.CommandOnCooldown):
            hacker = discord.Embed(
                color=0x2f3136,
                description=f"<:Nexus_cross:1144687282176147629> | {ctx.author.name} is on cooldown. Retry after {error.retry_after:.2f} second(s).",
                timestamp=ctx.message.created_at
            )
   #         hacker.set_author(name=str(ctx.author), icon_url=str(ctx.author.avatar_url))
            await ctx.reply(embed=hacker, delete_after=10)
        elif isinstance(error, commands.MaxConcurrencyReached):
            hacker = discord.Embed(
                color=0x2f3136,
                description="<:Nexus_cross:1144687282176147629> | This command is already running. Please wait for it to finish and retry later.",
                timestamp=ctx.message.created_at
            )
            hacker.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=hacker, delete_after=10)
        elif isinstance(error, commands.MissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            if len(missing) > 2:
                fmt = "{}, and {}".format(", ".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)
            hacker = discord.Embed(
                color=0x2f3136,
                description=f"<:Nexus_cross:1144687282176147629> | You lack `{fmt}` permission(s) to run the `{ctx.command.name}` command!",
                timestamp=ctx.message.created_at
            )
       #     hacker.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=hacker, delete_after=6)
        elif isinstance(error, commands.BadArgument):
            await ctx.send_help(ctx.command)
        elif isinstance(error, commands.BotMissingPermissions):
            missing = ", ".join(error.missing_perms)
            await ctx.send(f'I need the **{missing}** permission(s) to run the **{ctx.command.name}** command!', delete_after=10)
        elif isinstance(error, discord.HTTPException):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            pass
          