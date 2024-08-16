import discord
from discord.ext import commands


class activityrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Security commands"""
  
    def help_custom(self):
		      emoji = '<:SageActivity:1262521590147715231>'
		      label = "Activity Commands"
		      description = "Show You Activity Commands"
		      return emoji, label, description

    @commands.group(name='Here is Activity Commands', invoke_without_command=True)
    async def __Activity__(self, ctx: commands.Context):
        """`activityrole`, `activityrole setup`, `activityrole reset`, `activityrole status`"""