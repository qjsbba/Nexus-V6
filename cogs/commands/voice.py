import discord
from discord.ext import commands


class hacker1111111111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Voice commands"""
  
    def help_custom(self):
		      emoji = '<:icons_voice:1148115336567205898>'
		      label = "Voice"
		      description = "Shows You Voice Commands."
		      return emoji, label, description

    @commands.group()
    async def __Voice__(self, ctx: commands.Context):
        """`voice` , `voice kick` , `voice kickall` , `voice mute` , `voice muteall` , `voice unmute` , `voice unmuteall` , `voice deafen` , `voice deafenall` , `voice undeafen` , `voice undeafenall` ,` voice moveall` , `vcrole bots add` , `vcrole bots remove` , `vcrole bots` , `vcrole config` , `vcrole humans add` , `vcrole humans remove` , `vcrole humans` , `vcrole rese`t , `vcrole`"""






