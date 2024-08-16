from __future__ import annotations
import discord
from discord.ext import commands, tasks
from core import *
from utils.Tools import *
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from discord.ui import Button, View


class Ignore(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="ignore", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    async def _ignore(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_ignore.group(name="channel",
                   aliases=["chnl"],
                   invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _channel(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_channel.command(name="add")
    @commands.has_permissions(administrator=True)
    async def channel_add(self, ctx: Context, channel: discord.TextChannel):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            with open('db/ignore.json', 'r') as ignore:
                ignores = json.load(ignore)
                if str(channel.id) in ignores["ids"]:
                    embed = discord.Embed(
                        description=
                        f"<:hacker_admin_cross:1271209737647558819> | {channel.mention} is already in ignore channel list .",
                        color=0x2f3136)
                    await ctx.reply(embed=embed, mention_author=False)
                else:
                    add_channel_to_ignore(channel.id)
                    embed = discord.Embed(
                        description=
                        f"<:hacker_tick:1271209580793167925> | Successfully added {channel.mention} to ignore channel list .",
                        color=0x2f3136)
                    await ctx.reply(embed=embed, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5)

    @_channel.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def channel_remove(self, ctx, channel: discord.TextChannel):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            remove_channel_from_ignore(channel.id)
            embed = discord.Embed(
                description=
                f"<:hacker_tick:1271209580793167925> | Successfully removed {channel.mention} from ignore channel list .",
                color=0x2f3136)

            await ctx.reply(embed=embed, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5)


    @_ignore.group(name="user", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    async def _user(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_user.command(name="add",
                        help="add a user to ignored users list for this server .",
                        usage="ignore user add")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def useradd(self, ctx, user: discord.User):
        data = iuser(ctx.guild.id)
        wled = data["iuser"]

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
                if str(user.id) in wled:
                    hacker1 = discord.Embed(
                        description=f"<:hacker_admin_cross:1271209737647558819> | {user.mention} is already in ignore users list .",
                        color=0x2f3136)
                    await ctx.reply(embed=hacker1, mention_author=False)
                else:
                    wled.append(str(user.id))
                    iuser1(ctx.guild.id, data)
                    hacker4 = discord.Embed(
                        description=f"<:hacker_tick:1271209580793167925> | Successfully added {user.mention} to ignore users list .",
                        color=0x2f3136)
                    await ctx.reply(embed=hacker4, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_user.command(name="remove",
                        help="remove a user to ignored users list for this server .",
                        usage="ignore user remove")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def removeuser(self, ctx, user: discord.User):
        data = iuser(ctx.guild.id)
        wled = data["iuser"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if str(user.id) in wled:
                wled.remove(str(user.id))
                iuser1(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=0x2f3136,
                    description=f"<:hacker_tick:1271209580793167925> | Successfully removed {user.mention} from ignore users list ."
                )
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                hacker2 = discord.Embed(
                    color=0x2f3136,
                    description=
                    "<:hacker_admin_cross:1271209737647558819> | This server dont have any ignore users setupped yet ."
                )
                await ctx.reply(embed=hacker2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_user.command(name="show",
                        help="Shows list of ignored users in the server .",
                        usage="ignore user show")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def iusershow(self, ctx):
        data = iuser(ctx.guild.id)
        wled = data["iuser"]
        if len(wled) == 0:
            hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:hacker_admin_cross:1271209737647558819> | This server dont have any ignore users setupped yet ."
            )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            entries = [
                f"`{no}` | <@!{idk}> | ID: [{idk}](https://discord.com/users/{idk})"
                for no, idk in enumerate(wled, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Ignored Users of {ctx.guild.name} - {len(wled)}",
                description="",
                color=0x2F3136),
                                  ctx=ctx)
            await paginator.paginate()
#####
    @_ignore.group(name="bypass", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    async def _bypass(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_bypass.group(name="users", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    async def _users(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_users.command(name="add",
                        help="add a user to ignored bypass users list for this server .",
                        usage="ignore bypass users add")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def hllw(self, ctx, user: discord.User):
        data = iuser2(ctx.guild.id)
        wled1 = data["ibypass"]

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
                if str(user.id) in wled1:
                    hacker1 = discord.Embed(
                        description=f"<:hacker_admin_cross:1271209737647558819> | {user.mention} is already in ignore bypass users list .",
                        color=0x2f3136)
                    await ctx.reply(embed=hacker1, mention_author=False)
                else:
                    wled1.append(str(user.id))
                    iuser3(ctx.guild.id, data)
                    hacker4 = discord.Embed(
                        description=f"<:hacker_tick:1271209580793167925> | Successfully added {user.mention} to ignore bypass users list .",
                        color=0x2f3136)
                    await ctx.reply(embed=hacker4, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_users.command(name="remove",
                        help="remove a user to ignored bypass users list for this server .",
                        usage="ignore bypass users remove")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def removeuser1(self, ctx, user: discord.User):
        data = iuser2(ctx.guild.id)
        wled1 = data["ibypass"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if str(user.id) in wled1:
                wled1.remove(str(user.id))
                iuser3(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=0x2f3136,
                    description=f"<:hacker_tick:1271209580793167925> | Successfully removed {user.mention} from ignore bypass users list ."
                )
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                hacker2 = discord.Embed(
                    color=0x2f3136,
                    description=
                    "<:hacker_admin_cross:1271209737647558819> | This server dont have any ignore bypass users setupped yet ."
                )
                await ctx.reply(embed=hacker2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_users.command(name="show",
                        help="Shows list of ignored bypass users in the server .",
                        usage="ignore bypass users show")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def iusershow1(self, ctx):
        data = iuser2(ctx.guild.id)
        wled1 = data["ibypass"]
        if len(wled1) == 0:
            hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:hacker_admin_cross:1271209737647558819> | This server dont have any ignore bypass users setupped yet ."
            )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            entries = [
                f"`{no}` | <@!{idk}> | ID: [{idk}](https://discord.com/users/{idk})"
                for no, idk in enumerate(wled1, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Ignore Bypass Users of {ctx.guild.name} - {len(wled1)}",
                description="",
                color=0x2F3136),
                                  ctx=ctx)
            await paginator.paginate()