import discord
from discord.ext import commands


class ver1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Verification commands"""
  
    def help_custom(self):
		      emoji = '<:icons_verify:1145005541123436716>'
		      label = "Verification"
		      description = "Show You Verification Commands"
		      return emoji, label, description

    @commands.group()
    async def __Verification__(self, ctx: commands.Context):
        """`verification enable` `verification disable` `verification config`"""






