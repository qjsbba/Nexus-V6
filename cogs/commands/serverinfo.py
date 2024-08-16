from discord.ext import commands
import discord
import os
import humanize
from discord.ext.commands import Cog, Context
from utils.Tools import *

class util:
  def checkrol(role):
    perms = ""
    for p in role.permissions:
      xd = p[0]
      checkofperm = p[1]
      wp = xd.replace("_", " ")
      if checkofperm:
        perms+=f"{xd.replace('_', ' ')}, "
    if perms == "":
      perms+="None"
    else:
      perms.replace("_", " ")
      perms.strip(", ")
    return perms

class Info(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.client = bot
    self.color = discord.Color (0x00FFED)

  @commands.command(name="serverinfo",aliases=["sinfo","si"], description="Show's information of the server")
  @blacklist_check()
  @ignore_check()
  @iuser_check()
  async def serverinfo(self, ctx: commands.Context):
        bammed = 0
        async for bans in ctx.guild.bans(limit=None):
          bammed += 1
        animated_emojis = len([emoji for emoji in ctx.guild.emojis if emoji.animated])
        static = len([emoji for emoji in ctx.guild.emojis if not emoji.animated])
        om = ctx.guild.afk_timeout /60
        default = None
        if ctx.guild.default_notifications == discord.NotificationLevel.all_messages:
          default = "All Messages"
        elif ctx.guild.default_notifications == discord.NotificationLevel.only_mentions:
          default = "Only @mentions"
        al = ctx.guild.emoji_limit
        al1 = ctx.guild.sticker_limit
        uf = ctx.guild.emoji_limit * 2
        nsfw_level = ''
        if ctx.guild.nsfw_level.name == 'default':
          nsfw_level = 'Default'
        if ctx.guild.nsfw_level.name == 'explicit':
          nsfw_level = 'Explicit'
        if ctx.guild.nsfw_level.name == 'safe':
          nsfw_level = 'Safe'
        if ctx.guild.nsfw_level.name == 'age_restricted':
          nsfw_level = 'Age Restricted'
        guild: discord.Guild = ctx.guild 
        for r in ctx.guild.roles:
            if len(ctx.guild.roles) < 1:
                roless = "None"
            else:
                if len(ctx.guild.roles) < 50:
                    roless = ", ".join(
                        [role.mention for role in ctx.guild.roles[1:][::-1]])
                else:
                    if len(ctx.guild.roles) > 50:
                        roless = "Too many roles to show here." 
        embed = discord.Embed(color=0x00FFED,
            title=f" **{guild.name}'s Information**",
          description=f"**__About__**\n**Name:** {ctx.guild.name}\n**ID:** {ctx.guild.id}\n**Owner <:nexus_crown:1144991527681138739>:** {ctx.guild.owner} ({guild.owner.mention})\n**Created At:** <t:{round(guild.created_at.timestamp())}:R>\n**Members:** {len(guild.members)}\n**Banned:** {bammed}")
             
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar)
        if guild.icon is not None:
            embed.set_thumbnail(url=guild.icon.url)
        if guild.system_channel_flags.join_notifications:
          haa = "**System Welcome Messages**: <:tick_icons:1124596979813580801>"
        else:
          haa = "**System Welcome Messages**: <:icons_cross:1124690918893690920>"
        afkk = ctx.guild.afk_channel
        if ctx.guild.system_channel_flags.premium_subscriptions:
          skib = "**System Boost Messages**: <:tick_icons:1124596979813580801>"
        else:
          skib = "**System Boost Messages**: <:icons_cross:1124690918893690920>"  
        if guild.system_channel:
              ha = f"**System Messages Channel**: {guild.system_channel.mention}"
        else:
              ha = "**System Messages Channel**: None"
        mfa = ""
        if ctx.guild.mfa_level == discord.MFALevel.disabled:
          mfa = "Enabled <:tick_icons:1124596979813580801>"
        else:
          mfa = "Disabled <:icons_cross:1124690918893690920>"
        embed.add_field(
            name="**__Extras__**",
            value=f"""
**Verification Level:** {str(guild.verification_level).title()}
**Upload Limit:** {humanize.naturalsize(guild.filesize_limit)}
**Inactive Channel**: {afkk}
**Inactive Timeout:** {om} Mins
{ha}
{haa} 
{skib} 
**Default Notifications:** {default}
**Explicit Media Content Filter:** {guild.explicit_content_filter.name} 
**2FA Requirement:** {mfa}
**Boost Bar Enabled:** {'<:icons_cross:1124690918893690920>' if not ctx.guild.premium_progress_bar_enabled else '<:tick_icons:1124596979813580801>'}
            """,
            inline=False
        )
        embed.add_field(
            name="**__Description__**",
            value=f"""
{guild.description}
            """,
            inline=False
        )       
        if guild.features:
            dk = []
            for feat in guild.features:
              dk.append(feat.replace('_', ' ').title())
            embed.add_field(
                name="**__Features__**",
                value='\n'.join([f"<:tick_icons:1124596979813580801>: {feature}" for feature in dk]),
                inline=False
            )
            if guild.rules_channel:
              bye = f"Rules Channel: {guild.rules_channel.mention}"
            else:
              bye = ""
            embed.add_field(
            name="**__Channels__**",
            value=f"""
Total: {len(guild.channels)}
Channels: <:Channels:1145003473272844448> {len(guild.text_channels)} | <:icons_voice:1145003566180872273> {len(guild.voice_channels)} | <:icons_podcast:1145003473876811856> {len(guild.stage_channels)} 
{bye}
            """,
            inline=False
        )
        embed.add_field(
            name="**__Emoji Info__**",
            value=f"""
Regular: {static}/{al}
Animated: {animated_emojis}/{al}
Stickers: {len(guild.stickers)}/{al1}
Total Emoji: {len(guild.emojis)}/{uf}
            """, 
            inline=False
        )
        if guild.premium_subscriber_role:
          byecom = f"Booster Role: {guild.premium_subscriber_role.mention}"
        else:
          byecom = ""
        embed.add_field(
            name="**__Boost Status__**",
            value=f"""
Level: {guild.premium_tier} [<:Boosters:1144632869940121731> {guild.premium_subscription_count} boosts] 
{byecom}
            """,
            inline=False
        )
        embed.add_field(name=f"**__Server Roles [ {len(guild.roles)} ]__**",
                        value=f"{roless}",
                        inline=False)
        if guild.banner is not None:
            embed.set_image(url=guild.banner.url)
        embed.timestamp = discord.utils.utcnow()
        return await ctx.send(embed=embed)