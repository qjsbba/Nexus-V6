import discord
from discord.ext import commands


class gw1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Giveaway commands"""
  
    def help_custom(self):
		      emoji = '<a:nexus_giveaway:1147374841108910143>'
		      label = "Giveaway"
		      description = "Shows You Giveaway Commands."
		      return emoji, label, description

    @commands.group()
    async def __Giveaway__(self, ctx: commands.Context):
        """`giveaway` , `gstart` , `gend` , `greroll`"""