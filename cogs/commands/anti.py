from core import Cog, Astroz, Context
import discord
from utils.Tools import *
from discord.ui import Button, View
import datetime
from typing import Optional
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator


class Security(Cog):
    """Shows a list of commands regarding antinuke"""

    def __init__(self, client: Astroz):
        self.client = client
        self.color = 0x2f3136



    @commands.hybrid_group(name="antinuke",
                    aliases=["anti", "Security"],
                    help="Enables/Disables antinuke in your server .",
                    invoke_without_command=True,
                    usage="Antinuke Enable/Disable")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _antinuke(self, ctx: Context):
        embed = discord.Embed(
            title="Antinuke Command List",
            description="Use the following commands to manage antinuke settings for your server:",
            color=self.color
        )
        embed.add_field(name="Antinuke Enable", value="Enable antinuke in your server.", inline=False)
        embed.add_field(name="Antinuke Disable", value="Disable antinuke in your server.", inline=False)
        embed.add_field(name="Antinuke Show", value="Show the current status of antinuke settings.", inline=False)
        embed.add_field(name="Antinuke Punishment", value="Shows all Antinuke Punishment Commands", inline=False)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text=f"Request By {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=embed, mention_author=False)            

    @_antinuke.command(name="enable")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antinuke_enable(self, ctx: Context):
        
        
        data = getanti(ctx.guild.id)
        d2 = getConfig(ctx.guild.id)
        event = getHacker(ctx.guild.id)
        wled = d2["whitelisted"]
        punish = d2["punishment"]
        antibot = event["antinuke"]["antibot"]
        antiban = event["antinuke"]["antiban"]
        antikick = event["antinuke"]["antikick"]
        antichannelcreate = event["antinuke"]["antichannel-create"]
        antichanneldelete = event["antinuke"]["antichannel-delete"]
        antichannelupdate = event["antinuke"]["antichannel-update"]
        antirolecreate = event["antinuke"]["antirole-create"]
        antiroledelete = event["antinuke"]["antirole-delete"]
        antiroleupdate = event["antinuke"]["antirole-update"]
        antiwebhook = event["antinuke"]["antiwebhook"]
        antiguild = event["antinuke"]["antiserver"]
        antiemojicreate = event["antinuke"]["antiemoji-create"]
        antiemojidelete = event["antinuke"]["antiemoji-delete"]
        antiemojiupdate = event["antinuke"]["antiemoji-update"]    
        antiping = event["antinuke"]["antiping"] 
        antiprune = event["antinuke"]["antiprune"] 
        if antibot == True:
            bot = "**Anti Bot:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antibot == False:
            bot = "**Anti Bot:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiban == True:
            ban = "**Anti Ban:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antibot == False:
            ban = "**Anti Ban:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antikick == True:
            kick = "**Anti Kick:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antikick == False:
            kick = "**Anti Kick:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antichannelcreate == True:
            channelcreate = "**Anti Channel Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antichannelcreate == False:
            channelcreate = "**Anti Channel Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antichanneldelete == True:
            channeldelete = "**Anti Channel Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antichanneldelete == False:
            channeldelete = "**Anti Channel Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antichannelupdate == True:
            channelupdate = "**Anti Channel Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antichannelupdate == False:
            channelupdate = "**Anti Channel Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antirolecreate == True:
            rolecreate = "**Anti Role Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antirolecreate == False:
            rolecreate = "**Anti Role Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiroledelete == True:
            roledelete = "**Anti Role Delete:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiroledelete == False:
            roledelete = "**Anti Role Delete:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiroleupdate == True:
            roleupdate = "**Anti Role Update:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiroleupdate == False:
            roleupdate = "**Anti Role Update:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiwebhook == True:
            webhook = "**Anti Webhook Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiwebhook == False:
            webhook = "**Anti Webhook Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiguild == True:
            antiserver = "**Anti Guild Update:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiguild == False:
            antiserver = "**Anti Guild Update:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"

        if antiemojicreate == True:
            emojicreate = "**Anti Emoji Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antirolecreate == False:
            emojicreate = "**Anti Emoji Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiroledelete == True:
            emojidelete = "**Anti Emoji Delete:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiemojidelete == False:
            emojidelete = "**Anti Emoji Delete:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiemojiupdate == True:
            emojiupdate = "**Anti Emoji Update:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiemojiupdate == False:
            emojiupdate = "**Anti Emoji Update:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"

        if antiping == True:
            ping = "**Anti Everyone/Here Mention:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiping == False:
            ping = "**Anti Everyone/Here Mention:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"

        if antiprune == True:
            prune = "**Anti Prune:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiprune == False:
            prune = "**Anti Prune:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"  

        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:   
            if data == "on":
                embed = discord.Embed(

                    description=
                    f"Looks Like **{ctx.guild}** has already Enabled Sage Security\n\nUse `antinuke disable` to Disable Security in **{ctx.guild}**\nUse `antinuke` to check all Security Command.\n\n**Security Status :** <:Sageenable:1257270292875575338>",
                    color=self.color)
                embed.set_author(name=f"{ctx.guild.name}'s Security Settings", icon_url=ctx.guild.icon.url if ctx.guild.icon else self.client.user.avatar.url)
                embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else self.client.user.avatar.url)

                await ctx.reply(embed=embed, mention_author=False)
            else:
                data = "on"
                updateanti(ctx.guild.id, data)
                embed2 = discord.Embed(

                    description=
                    f"""
### <:SageRules:1257300322204778568> Instructions ###
Move My Role to Top of Roles for me to work Properly.
Use `antinuke` to Check all Antinuke Commands.
Also You Can Whitelist Your Trusted Member by using `antinuke whitelist add <user>`.


### <:SageModeration:1257299062777184337> Security Punishments: ###
{bot}
{ban}
{kick}
{channelcreate}
{channeldelete}
{channelupdate}
{rolecreate}
{roledelete}
{roleupdate}
{webhook}
{antiserver}
{emojicreate}
{emojidelete}
{emojiupdate}
{ping}
**Whitelisted Users:** {len(wled)}


**Auto Recovery:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>
{prune}                                     
                    """,
                    color=self.color)
                embed2.set_author(name=f"{ctx.guild.name}'s Security Settings", icon_url=ctx.guild.icon.url if ctx.guild.icon else self.client.user.avatar.url)
                embed2.add_field(
                    name="<:Sageutility:1244686286522945586> More Security Settings",
                    value=
                f"You Can Change the Punishment by Using `antinuke punishment set <type>`\n**Punishment Types:** `kick`, `ban` and `None`."
                )
                embed2.set_footer(text=f"Current punishment type is {punish}")
                await ctx.reply(embed=embed2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)


    @_antinuke.command(
        name="disable",
        help="You can disable antinuke for your server using this command",
        aliases=["off"],
        usage="Antinuke disable")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antinuke_disable(self, ctx: Context):
        
        
        data = getanti(ctx.guild.id)
        d2 = getConfig(ctx.guild.id)
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:   
            if data == "off":
                emb = discord.Embed(

                    description=
                    f"Looks Like **{ctx.guild}** has already Disabled Sage Security\n\nUse `antinuke enable` to Enable Security in **{ctx.guild}**\nUse `antinuke` to check all Security Command.\n\n**Security Status :** <:Sagedisable:1257270290107596943>",
                    color=self.color)
                emb.set_author(name=f"{ctx.guild.name}'s Security Settings", icon_url=ctx.guild.icon.url if ctx.guild.icon else self.client.user.avatar.url)
                emb.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else self.client.user.avatar.url)
                await ctx.reply(embed=emb, mention_author=False)
            else:
                data = "off"
                updateanti(ctx.guild.id, data)
                final = discord.Embed(

                    description=
                    f"Successfully Disabled security settings.\nUse `antinuke enable`to Enable Security again in **{ctx.guild}**.\n\n**Security Status:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>",
                    color=self.color)
                final.set_author(name=f"{ctx.guild.name}'s Security Settings", icon_url=ctx.guild.icon.url if ctx.guild.icon else self.client.user.avatar.url)
                final.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else self.client.user.avatar.url)
                await ctx.reply(embed=final, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)


    @_antinuke.command(
        name="antirole-create",
        help="Toggles antirole-create",
        usage="antinuke antirole-create")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antirolecreate(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:   
            if data["antinuke"]["antirole-create"] == True:
                data["antinuke"]["antirole-create"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antirole-create** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
            elif data["antinuke"]["antirole-create"] == False:
                data["antinuke"]["antirole-create"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antirole-create** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)


    @_antinuke.command(
        name="antirole-delete",
        help="Toggles antirole-delete",
        usage="antinuke antirole-delete")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiroledelete(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:   
            if data["antinuke"]["antirole-delete"] == True:
                data["antinuke"]["antirole-delete"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antirole-delete** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
            elif data["antinuke"]["antirole-delete"] == False:
                data["antinuke"]["antirole-delete"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **antirole-delete** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)



    @_antinuke.command(
        name="antirole-update",
        help="Toggles antirole-update",
        usage="antinuke antirole-update")
    @blacklist_check()

    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiroleupdate(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:   
            if data["antinuke"]["antirole-update"] == True:
                data["antinuke"]["antirole-update"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antirole-update** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
            elif data["antinuke"]["antirole-update"] == False:
                data["antinuke"]["antirole-update"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antirole-update** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)

    @_antinuke.command(
        name="antichannel-create",
        help="Toggles antichannel-create",
        usage="antinuke antichannel-create")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antichannelcreate(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:   
            if data["antinuke"]["antichannel-create"] == True:
                data["antinuke"]["antichannel-create"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antichannel-create** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
            elif data["antinuke"]["antichannel-create"] == False:
                data["antinuke"]["antichannel-create"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antichannel-create** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10) 

    @_antinuke.command(
        name="antichannel-delete",
        help="Toggles antichannel-delete",
        usage="antinuke antichannel-delete")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antichanneldelete(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:   
            if data["antinuke"]["antichannel-delete"] == True:
                data["antinuke"]["antichannel-delete"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antichannel-delete** is now Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)

            elif data["antinuke"]["antichannel-delete"] == False:
                data["antinuke"]["antichannel-delete"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antichannel-delete** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)

    @_antinuke.command(
        name="antichannel-update",
        help="Toggles antichannel-update",
        usage="antinuke antichannel-update")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antichannelupdate(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:   
            if data["antinuke"]["antichannel-update"] == True:
                data["antinuke"]["antichannel-update"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antichannel-update** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
            elif data["antinuke"]["antichannel-update"] == False:
                data["antinuke"]["antichannel-update"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antichannel-update** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)



    @_antinuke.command(
        name="antiban",
        help="Toggles antiban",
        usage="antinuke antiban")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiban(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:   
            if data["antinuke"]["antiban"] == True:
                data["antinuke"]["antiban"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiban** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)

            elif data["antinuke"]["antiban"] == False:
                data["antinuke"]["antiban"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiban** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)



    @_antinuke.command(
        name="antikick",
        help="Toggles antikick",
        usage="antinuke antikick")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antikick(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:   
            if data["antinuke"]["antikick"] == True:
                data["antinuke"]["antikick"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antikick** is **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)

            elif data["antinuke"]["antikick"] == False:
                data["antinuke"]["antikick"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antikick is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)

    @_antinuke.command(
        name="antiwebhook",
        help="Toggles antiwebhook",
        usage="antinuke antiwebhook")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiwebhook(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:   
            if data["antinuke"]["antiwebhook"] == True:
                data["antinuke"]["antiwebhook"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiwebhook** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)

            elif data["antinuke"]["antiwebhook"] == False:
                data["antinuke"]["antiwebhook"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiwebhook** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)


    @_antinuke.command(
        name="antibot",
        help="Toggles antibot",
        usage="antinuke antibot")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antibot(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  
            if data["antinuke"]["antibot"] == True:
                data["antinuke"]["antibot"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antibot** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)

            elif data["antinuke"]["antibot"] == False:
                data["antinuke"]["antibot"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antibot** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)

    @_antinuke.command(
        name="antiserver",
        help="Toggles antiserver",
        usage="antinuke antiserver")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiserver(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner: 
            if data["antinuke"]["antiserver"] == True:
                data["antinuke"]["antiserver"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiserver** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)

            elif data["antinuke"]["antiserver"] == False:
                data["antinuke"]["antiserver"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiserver** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)




    @_antinuke.command(
        name="antiping",
        help="Toggles antiping",
        usage="antinuke antiping")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiping(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  
            if data["antinuke"]["antiping"] == True:
                data["antinuke"]["antiping"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiping** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)

            elif data["antinuke"]["antiping"] == False:
                data["antinuke"]["antiping"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiping** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)



    @_antinuke.command(
        name="antiemoji-delete",
        help="Toggles antiemoji-delete",
        usage="antinuke antiemoji-delete")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiemojidelete(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  
            if data["antinuke"]["antiemoji-delete"] == True:
                data["antinuke"]["antiemoji-delete"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiemoji-delete** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)

            elif data["antinuke"]["antiemoji-delete"] == False:
                data["antinuke"]["antiemoji-delete"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiemoji-delete** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)




    @_antinuke.command(
        name="antiemoji-create",
        help="Toggles antiemoji-create",
        usage="antinuke antiemoji-create")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiemojicreate(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  
            if data["antinuke"]["antiemoji-create"] == True:
                data["antinuke"]["antiemoji-create"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiemoji-create** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)

            elif data["antinuke"]["antiemoji-create"] == False:
                data["antinuke"]["antiemoji-create"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiemoji-create** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)


    @_antinuke.command(
        name="antiemoji-update",
        help="Toggles antiemoji-update",
        usage="antinuke antiemoji-update")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiemojiupdate(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  
            if data["antinuke"]["antiemoji-update"] == True:
                data["antinuke"]["antiemoji-update"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiemoji-update** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)

            elif data["antinuke"]["antiemoji-update"] == False:
                data["antinuke"]["antiemoji-update"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antiemoji-update** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)

    @_antinuke.command(
        name="antimemberrole-update",
        help="Toggles antimemberrole-update",
        usage="antinuke antimemberrole-update")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antimemberroleupdate(self, ctx):
        data = getHacker(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  
            if data["antinuke"]["antimemberrole-update"] == True:
                data["antinuke"]["antimemberrole-update"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antimemberrole-update** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)

            elif data["antinuke"]["antimemberrole-update"] == False:
                data["antinuke"]["antimemberrole-update"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=self.color,
                description=
                f"<a:SageCheck:1250852491768369172> | **Antimemberrole-update** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)

    @_antinuke.command(
        name="show",
        help="Shows currently antinuke config settings of your server",
        aliases=["config"],
        usage="Antinuke show")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antinuke_show(self, ctx: Context):
        
        
        data = getanti(ctx.guild.id)
        event = getHacker(ctx.guild.id)
        d2 = getConfig(ctx.guild.id)
        wled = d2["whitelisted"]
        punish = d2["punishment"]
        wlrole = d2['wlrole']
        antibot = event["antinuke"]["antibot"]
        antiban = event["antinuke"]["antiban"]
        antikick = event["antinuke"]["antikick"]
        antichannelcreate = event["antinuke"]["antichannel-create"]
        antichanneldelete = event["antinuke"]["antichannel-delete"]
        antichannelupdate = event["antinuke"]["antichannel-update"]
        antirolecreate = event["antinuke"]["antirole-create"]
        antiroledelete = event["antinuke"]["antirole-delete"]
        antiroleupdate = event["antinuke"]["antirole-update"]
        antiwebhook = event["antinuke"]["antiwebhook"]
        antiguild = event["antinuke"]["antiserver"]
        antiemojicreate = event["antinuke"]["antiemoji-create"]
        antiemojidelete = event["antinuke"]["antiemoji-delete"]
        antiemojiupdate = event["antinuke"]["antiemoji-update"]    
        antiping = event["antinuke"]["antiping"] 
        antiprune = event["antinuke"]["antiprune"]        
        emojicreate =""
        if antibot == True:
            bot = "**Anti Bot:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antibot == False:
            bot = "**Anti Bot:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiban == True:
            ban = "**Anti Ban:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antibot == False:
            ban = "**Anti Ban:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antikick == True:
            kick = "**Anti Kick:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antikick == False:
            kick = "**Anti Kick:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antichannelcreate == True:
            channelcreate = "**Anti Channel Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antichannelcreate == False:
            channelcreate = "**Anti Channel Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antichanneldelete == True:
            channeldelete = "**Anti Channel Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antichanneldelete == False:
            channeldelete = "**Anti Channel Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antichannelupdate == True:
            channelupdate = "**Anti Channel Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antichannelupdate == False:
            channelupdate = "**Anti Channel Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antirolecreate == True:
            rolecreate = "**Anti Role Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antirolecreate == False:
            rolecreate = "**Anti Role Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiroledelete == True:
            roledelete = "**Anti Role Delete:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiroledelete == False:
            roledelete = "**Anti Role Delete:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiroleupdate == True:
            roleupdate = "**Anti Role Update:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiroleupdate == False:
            roleupdate = "**Anti Role Update:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiwebhook == True:
            webhook = "**Anti Webhook Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiwebhook == False:
            webhook = "**Anti Webhook Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiguild == True:
            antiserver = "**Anti Guild Update:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiguild == False:
            antiserver = "**Anti Guild Update:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"

        if antiemojicreate == True:
            emojicreate = "**Anti Emoji Create:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antirolecreate == False:
            emojicreate = "**Anti Emoji Create:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiroledelete == True:
            emojidelete = "**Anti Emoji Delete:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiemojidelete == False:
            emojidelete = "**Anti Emoji Delete:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"
        if antiemojiupdate == True:
            emojiupdate = "**Anti Emoji Update:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiemojiupdate == False:
            emojiupdate = "**Anti Emoji Update:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"

        if antiping == True:
            ping = "**Anti Everyone/Here Mention:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiping == False:
            ping = "**Anti Everyone/Here Mention:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"

        if antiprune == True:
            prune = "**Anti Prune:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>"
        elif antiprune == False:
            prune = "**Anti Prune:** <:SageDisable:1250899245238587441><:SageEnable:1250899295381749864>"           

        if data == "off":
            emb = discord.Embed(

                description=
                f"Looks Like **{ctx.guild}** has Disabled Sage Security\n\nUse `antinuke enable` to Disable Security in **{ctx.guild}**\nUse `antinuke` to check all Security Command.\n\n**Security Status :** <:Sagedisable:1257270290107596943>",
                color=self.color)
            emb.set_author(name=f"{ctx.guild.name}'s Security Settings", icon_url=ctx.guild.icon.url if ctx.guild.icon else self.client.user.avatar.url)
            emb.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else self.client.user.avatar.url)
            await ctx.reply(embed=emb, mention_author=False)
        elif data == "on":
            embed2 = discord.Embed(

                description=
                f"""
### <:SageRules:1257300322204778568> Instructions ###
Move My Role to Top of Roles for me to work Properly.
Use `antinuke` to Check all Antinuke Commands.
Also You Can Whitelist Your Trusted Member by using `antinuke whitelist add <user>`.

### <:SageModeration:1257299062777184337> Security Punishments: ###
{bot}
{ban}
{kick}
{channelcreate}
{channeldelete}
{channelupdate}
{rolecreate}
{roledelete}
{roleupdate}
{webhook}
{antiserver}
{emojicreate}
{emojidelete}
{emojiupdate}
{ping}
**Whitelisted Role:** <@&{wlrole}>
**Whitelisted Users:** {len(wled)}


**Auto Recovery:** <:Sageno:1247285105756737566><:Sageyes:1247285177403838484>
{prune}
""",
                color=self.color)
            embed2.set_author(name=f"{ctx.guild.name}'s Security Settings", icon_url=ctx.guild.icon.url if ctx.guild.icon else self.client.user.avatar.url)
            embed2.add_field(
                name="<:Sageutility:1244686286522945586> More Security Settings",
                value=
            f"You Can Change the Punishment by Using `antinuke punishment set <type>`\n**Punishment Types:** `kick`, `ban` and `None`."
            )
            embed2.set_footer(text=f"Current Punishment Type Is {punish}")
            await ctx.reply(embed=embed2, mention_author=False)

    @_antinuke.command(
        name="recover",
        help="Deletes all channels with name of rules and moderator-only",
        usage="Antinuke recover")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _recover(self, ctx: Context):
        for channel in ctx.guild.channels:
            if channel.name in ('rules', 'moderator-only'):
                try:
                    await channel.delete()
                except:
                    pass
        hacker5 = discord.Embed(

            description=
            "<:Sageyes:1247285177403838484> | Successfully Deleted All Channels With Name Of `rules` and `moderator-only`",
            color=self.color)
        hacker5.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.reply(embed=hacker5, mention_author=False)

    @_antinuke.group(
        name="punishment",
        help="Changes Punishment of antinuke and antiraid for this server.",
        invoke_without_command=True,
        usage="Antinuke punishment set/show")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _punishment(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_punishment.command(
        name="set",
        help="Changes Punishment of antinuke and automod for this server.",
        aliases=["change"],
        usage="Antinuke punishment set <none>")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def punishment_set(self, ctx, punishment: str):
        
        
        data = getConfig(ctx.guild.id)

        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  

            kickOrBan = punishment.lower()

            if kickOrBan == "kick":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "kick"
                hacker = discord.Embed(

                    description=
                    f"<a:SageCheck:1250852491768369172> | Successfully Changed Punishment To: **{kickOrBan}** For {ctx.guild.name}",
                    color=self.color)
                await ctx.reply(embed=hacker, mention_author=False)

                updateConfig(ctx.guild.id, data)

            elif kickOrBan == "ban":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "ban"
                hacker1 = discord.Embed(

                    description=
                    f"<a:SageCheck:1250852491768369172> | Successfully Changed Punishment To: **{kickOrBan}** For {ctx.guild.name}",
                    color=self.color)
                await ctx.reply(embed=hacker1, mention_author=False)

                updateConfig(ctx.guild.id, data)

            elif kickOrBan == "none":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "none"
                hacker3 = discord.Embed(

                    description=
                    f"<a:SageCheck:1250852491768369172> | Successfully Changed Punishment To: **{kickOrBan}** For {ctx.guild.name}",
                    color=self.color)
                await ctx.reply(embed=hacker3, mention_author=False)

                updateConfig(ctx.guild.id, data)
            else:
                hacker6 = discord.Embed(

                    description=
                    "Invalid Punishment Type\nValid Punishment Type(s) Are: Kick, Ban, None",
                    color=self.color)
                await ctx.reply(embed=hacker6, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)

    @_punishment.command(name="show",
                         help="Shows custom punishment type for this server",
                         usage="Antinuke punishment show")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def punishment_show(self, ctx: Context):
        data = getConfig(ctx.guild.id)
        punish = data["punishment"]
        hacker5 = discord.Embed(
            color=self.color,

            description=
            "Custom punishment of anti-nuke in this server is: **{}**"
            .format(punish.title()))
        await ctx.reply(embed=hacker5, mention_author=False)

    @_antinuke.command(name="channelclean",
                       aliases=['cc'],
                       help="deletes channel with similar name provided.",
                       usage="Antinuke channelclean <none>")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def _channelclean(self, ctx: Context, channeltodelete: str):
        
        
        data = getConfig(ctx.guild.id)

        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  
            for channel in ctx.message.guild.channels:
                if channel.name == channeltodelete:
                    try:
                        await channel.delete()
                    except:
                        pass
            hacker1 = discord.Embed(

                description=
                f"<:Sageyes:1247285177403838484> | Successfully Deleted All Channels With The Name Of {channeltodelete}",
                color=self.color)
            await ctx.reply(embed=hacker1, mention_author=False)
        elif ctx.author.id == 246469891761111051:
            for channel in ctx.message.guild.channels:
                if channel.name == channeltodelete:
                    try:
                        await channel.delete()
                    except:
                        pass
            hacker2 = discord.Embed(

                description=
                f"<:Sageyes:1247285177403838484> | Successfully Deleted All Channels With The Name Of {channeltodelete}",
                color=self.color)
            await ctx.reply(embed=hacker2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)

    @_antinuke.command(name="roleclean",
                       aliases=['cr'],
                       help="deletes role with similar name provided",
                       usage="Antinuke roleclean <none>")
    @blacklist_check()
    @ignore_check()

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def _roleclean(self, ctx: Context, roletodelete: str):
        data = getConfig(ctx.guild.id)
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  
            for role in ctx.message.guild.roles:
                if role.name == roletodelete:
                    try:
                        await role.delete()
                    except:
                        pass
            hacker = discord.Embed(

                description=
                f"<:Sageyes:1247285177403838484> | Successfully Deleted All Roles With The Name Of {roletodelete}",
                color=self.color)
            await ctx.reply(embed=hacker, mention_author=False)
        elif ctx.author.id == 143853929531179008:
            for role in ctx.message.guild.roles:
                if role.name == roletodelete:
                    try:
                        await role.delete()
                    except:
                        pass
            hacker3 = discord.Embed(

                description=
                f"<:Sageyes:1247285177403838484> | Successfully Deleted All Roles With The Name Of {roletodelete}",
                color=self.color)
            await ctx.reply(embed=hacker3, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)

    @_antinuke.group(name="whitelist",
                  aliases=["wl"],
                     help="Whitelist your TRUSTED users for anti-nuke",
                     invoke_without_command=True,
                     usage="Antinuke whitelist add/remove")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _whitelist(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_whitelist.command(name="add",
                        help="Add a user to whitelisted users",
                        usage="Antinuke whitelist add <user>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_add(self, ctx, user: discord.User):
        data = getConfig(ctx.guild.id)
        wled = data["whitelisted"]
        
        

        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  
            if len(wled) == 100:
                hacker = discord.Embed(

                    description=
                    f"<:Sageexclamation:1250851224886968470> This server have already maximum number of whitelisted users (100)\nRemove one to add another :)",
                    color=self.color)
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                if str(user.id) in wled:
                    hacker1 = discord.Embed(

                        description=
                        f"<:Sageexclamation:1250851224886968470> That user is already in my whitelist.",
                        color=self.color)
                    await ctx.reply(embed=hacker1, mention_author=False)
                else:
                    wled.append(str(user.id))
                    updateConfig(ctx.guild.id, data)
                    hacker4 = discord.Embed(
                        color=self.color,

                        description=
                        f"<a:SageCheck:1250852491768369172> | Successfully Whitelisted {user.mention} For {ctx.guild.name}"
                    )
                    await ctx.reply(embed=hacker4, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)


    @_whitelist.command(name="remove",
                        help="Remove a user from whitelisted users",
                        usage="Antinuke whitelist remove <user>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_remove(self, ctx, user: discord.User):
        data = getConfig(ctx.guild.id)
        wled = data["whitelisted"]
        
        
        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  
            if str(user.id) in wled:
                wled.remove(str(user.id))
                updateConfig(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=self.color,

                    description=
                    f"<a:SageCheck:1250852491768369172> | Successfully Unwhitelisted {user.mention} For {ctx.guild.name}"
                )
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                hacker2 = discord.Embed(
                    color=self.color,

                    description=
                    "<:Sageexclamation:1250851224886968470> | That user is not in my whitelist."
                )
                await ctx.reply(embed=hacker2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)



    @_whitelist.command(name="show",
                        help="Shows list of whitelisted users in the server.",
                        usage="Antinuke whitelist show")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_show(self, ctx):
        data = getConfig(ctx.guild.id)
        wled = data["whitelisted"]
        
        
        if len(wled) == 0:
            hacker = discord.Embed(
                color=self.color,

                description=
                f"<:Sageexclamation:1250851224886968470> | There aren\'t any whitelised users for this server"
            )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            entries = [
                f"`{no}` | <@!{idk}> | ID: [{idk}](https://discord.com/users/{idk})"
                for no, idk in enumerate(wled, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Whitelisted Users of {ctx.guild.name} - {len(wled)}",
                description="",
                color=self.color),
                                  ctx=ctx)
            await paginator.paginate()

    @_whitelist.command(name="reset",
                        help="removes every user from whitelist database",
                        aliases=["clear"],
                        usage="Antinuke whitelist reset")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def wl_reset(self, ctx: Context):
        data = getConfig(ctx.guild.id)
        
        

        if ctx.author == ctx.guild.owner or str(ctx.author.id) in owner:  
            data = getConfig(ctx.guild.id)
            data["whitelisted"] = []
            updateConfig(ctx.guild.id, data)
            hacker = discord.Embed(
                color=self.color,

                description=
                f"<a:SageCheck:1250852491768369172> | Successfully Cleared Whitelist Database For **{ctx.guild.name}**"
            )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner or extra owners can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)


################################            ROLE WHITELISTING            ################################          




#########################3####33###3            

    @_antinuke.group(name="owner",
                     aliases=["own"],
                     help="Add/Remove a user to/from extra owner list for antinuke .",
                     invoke_without_command=True,
                     usage="Antinuke owner add/remove")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _owner(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_owner.command(name="add",
                        help="Add a user to extra owner list .",
                        usage="Antinuke owner add <user>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def owner_add(self, ctx, user: discord.User):
        data = getExtra(ctx.guild.id)
        wled = data["owners"]

        if ctx.author == ctx.guild.owner:
            if len(wled) == 15:
                hacker = discord.Embed(

                    description=
                    f"<:Sageexclamation:1250851224886968470> This server have already maximum number of extra owners(15)\nRemove one to add another :)",
                    color=self.color)
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                if str(user.id) in wled:
                    hacker1 = discord.Embed(

                        description=
                        f"<:Sageexclamation:1250851224886968470> That user is already in my extra owner list .",
                        color=self.color)
                    await ctx.reply(embed=hacker1, mention_author=False)
                else:
                    wled.append(str(user.id))
                    updateExtra(ctx.guild.id, data)
                    hacker4 = discord.Embed(
                        color=self.color,

                        description=
                        f"<a:SageCheck:1250852491768369172> | Successfully added {user.mention} as extra owner for {ctx.guild.name}"
                    )
                    await ctx.reply(embed=hacker4, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)

    @_owner.command(name="remove",
                        help="Remove a user from extra owner list .",
                        usage="Antinuke owner remove <user>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def owner_remove(self, ctx, user: discord.User):
        data = getExtra(ctx.guild.id)
        wled = data["owners"]
        if ctx.author == ctx.guild.owner:
            if str(user.id) in wled:
                wled.remove(str(user.id))
                updateExtra(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=self.color,

                    description=
                    f"<a:SageCheck:1250852491768369172> | Successfully removed {user.mention} from extra owner list of {ctx.guild.name}"
                )
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                hacker2 = discord.Embed(
                    color=self.color,

                    description=
                    f"<:Sageexclamation:1250851224886968470> | That user is not in {ctx.guild.name} extra owner list ."
                )
                await ctx.reply(embed=hacker2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)




    @_owner.command(name="show",
                        help="Shows list of extra owners in the server.",
                        usage="Antinuke owner show")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def owner_show(self, ctx):
        data = getExtra(ctx.guild.id)
        wled = data["owners"]
        if len(wled) == 0:
            hacker = discord.Embed(
                color=self.color,

                description=
                f"<:Sageexclamation:1250851224886968470> | There aren\'t any extra owner users for this server ."
            )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            entries = [
                f"`{no}` | <@!{idk}> | ID: [{idk}](https://discord.com/users/{idk})"
                for no, idk in enumerate(wled, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Extra Owners of {ctx.guild.name} - 15/{len(wled)}",
                description="",
                color=self.color),
                                  ctx=ctx)
            await paginator.paginate()

    @_owner.command(name="reset",
                        help="removes every user from extra owner list .",
                        aliases=["clear"],
                        usage="Antinuke owner reset")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def owner_reset(self, ctx: Context):
        data = getExtra(ctx.guild.id)

        if ctx.author == ctx.guild.owner:
            data = getExtra(ctx.guild.id)
            data["owners"] = []
            updateExtra(ctx.guild.id, data)
            hacker = discord.Embed(
                color=self.color,

                description=
                f"<a:SageCheck:1250852491768369172> | Successfully Cleared Extra Owners Database For **{ctx.guild.name}**"
            )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """<:Sageexclamation:1250851224886968470> | Only the server owner can run this command .""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker5, mention_author=False,delete_after=10)