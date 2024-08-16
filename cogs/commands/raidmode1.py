import discord
from discord.ext import commands


class hacker1111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Raidmode commands"""
  
    def help_custom(self):
		      emoji = '<:automod:1148959459121582231> '
		      label = "Raidmode"
		      description = "Shows You Raidmode Commands."
		      return emoji, label, description

    @commands.group()
    async def __Raidmode__(self, ctx: commands.Context):
        """`automod` , `antispam on` , `antispam off` , `antilink off` ,  `antilink on` , `verification enable` , `verification disable` , `verification config`"""