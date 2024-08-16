import discord
from discord.ext import commands


class hacker111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """General commands"""
  
    def help_custom(self):
		      emoji = '<a:general:1148115325703946340>'
		      label = "General"
		      description = "Shows You General Commands."
		      return emoji, label, description

    @commands.group()
    async def __General__(self, ctx: commands.Context):
        """`chatgpt` , `avatar` , `servericon` , `membercount` , `poll` , `hack` , `token` , `users` , `italicize` , `strike` , `quote` , `code` , `bold` , `censor` , `underline` , `gender` , `wizz` , `pikachu` , `shorten` , `urban` , `rickroll` , `hash` , `snipe` , `setup` , `setup staff` , `setup girl` , `setup friend` , `setup vip` , `setup guest` , `setup owner` , `setup coowner` , `setup headadmin` , `setup admins` , `setup girladmin` , `setup headmod` , `setup mod` , `setup girlmod` , `setup config` , `staff` , `girl` , `friend` , `vip` , `guest` , `owner` , `coowner` , `headadmin` , `admin` , `girladmin ` , `headmod` , `mod` , `girlmod` , `remove staff` , `remove girl` , `remove friend` , `remove vip` , `remove guest` , `remove owner` , `remove coowner` , `remove headadmin` , `remove admin` , `remove girladmin` , `remove headmod` , `remove mod` , `remove girlmod` , `ar` , `ar create` , `ar delete` , `ar edit` , `ar config`"""