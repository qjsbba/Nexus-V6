import discord
from discord.ext import commands


class hacker1111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Music commands"""
  
    def help_custom(self):
		      emoji = '<a:music_orbit:1147375359315152916>'
		      label = "Music"
		      description = "Shows You Music Commands."
		      return emoji, label, description

    @commands.group()
    async def __Music__(self, ctx: commands.Context):
        """`connect` , `play` , `queue` , `nowplaying` , `stop`, `pause` , `move` , `shuffle` , `resume` , `skip` , `clear` , `disconnect` , `seek` , `pull` , `volume` , `bassboost enable` , `bassboost disable` , `filter` , `filter daycore enable` , `filter daycore disable` , `filter speed enable` , `filter speed disable` , `filter slowmode enable` , `filter slowmode disable` , `filter lofi enable` , `filter lofi disable` , `filter nightcore enable` , `filter nightcore disable` , `filter drunk enable` , `filter drunk disable` , `filter quick enable` , `filter quick disable` , `filter slowmode enable` , `filter slowmode disable` , `filter reset`"""