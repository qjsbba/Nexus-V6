import discord
from discord.ext import commands


class reactionrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Starboard commands"""
  
    def help_custom(self):
		      emoji = '<:nexus_ColouredStar:1149251932779712563>'
		      label = "ReactionRole"
		      description = "Shows You ReactionRole Commands."
		      return emoji, label, description

    @commands.group()
    async def __Starboard__(self, ctx: commands.Context):
        """`starboard info` , `starboard limit` , `starboard lock` , `starboard setup` , `starboard unlock` , `starboard`"""