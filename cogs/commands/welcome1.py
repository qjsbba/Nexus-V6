import discord
from discord.ext import commands


class hacker11111111111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Welcome commands"""
  
    def help_custom(self):
		      emoji = '<a:_welcome_:1148115579211890688>'
		      label = "Welcomer"
		      description = "Shows You Welcomer Commands."
		      return emoji, label, description

    @commands.group()
    async def __Welcomer__(self, ctx: commands.Context):
        """`greet channel add` , `greet channel remove` , `greet channel` , `greet embed` , `greet image` , `greet message` , `greet ping` , `greet test` , `greet thumbnail` , `greet autodel` , `greet`"""