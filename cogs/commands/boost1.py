import discord
from discord.ext import commands


class velo1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """BoostMessage commands"""
  #sobn done help ar i think so
    def help_custom(self):
		      emoji = '<:Booster:1149252341896331295>'
		      label = "BoostMessage"
		      description = "Shows You BoostMessage Commands."
		      return emoji, label, description

    @commands.group()
    async def __BoostMessage__(self, ctx: commands.Context):
        """`boostrole add` , `boostrole remove` , `boostrole config` , `boostrole reset` , `boost channel add` , `boost channel remove` , `boost channel` , `boost embed` , `boost image` , `boost message` , `boost ping` , `boost test` , `boost thumbnail` , `boost autodel` , `boost`"""