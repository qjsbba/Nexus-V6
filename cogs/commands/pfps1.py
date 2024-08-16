import discord
from discord.ext import commands


class cool191(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Pfp Commands"""
  
    def help_custom(self):
		      emoji = '<a:awful_pfp:1147375011859009587>'
		      label = "Pfp"
		      description = "Show You Pfp Commands."
		      return emoji, label, description

    @commands.group()
    async def __Pfp__(self, ctx: commands.Context):
        """`pic`, `boys` , `girls`, `couples`, `anime`"""