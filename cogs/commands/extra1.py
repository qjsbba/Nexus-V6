import discord
from discord.ext import commands


class hacker11(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Extra commands"""
  
    def help_custom(self):
		      emoji = '<:extra:1148117650401153056>'
		      label = "Extra"
		      description = "Shows You Extra Commands."
		      return emoji, label, description

    @commands.group()
    async def __Extra__(self, ctx: commands.Context):
        """`stats` , `invite` , `vote` , `serverinfo` , `userinfo` , `roleinfo` , `botinfo` , `status` , `firstmessage` , `passgen` , `say` , `boostlevel` , `emoji` , `user` , `badges` , `role` , `channel` , `boosts` , `unbanall` ,  `joined-at` , `ping` , `uptime` , `github` , `vcinfo` , `channelinfo` , `note` , `notes` , `trashnotes` , `badges` , `reminder start` , `reminder delete` , `reminder list` , `list boosters` , `list inrole` , `list emojis` , `list bots` , `list admins` , `list invoice` , `list mods` , `list early` , `list activedeveloper` , `list createpos` , `list roles` , `ignore` , `ignore channel` , `ignore channel add` , `ignore channel remove` , `ignore user add` , `ignore user remove` , `ignore user show` , `banner user` , `banner server` , `logall enable` , `logall disable` , `pic`, `boys` , `girls`, `couples`, `anime` , `media`, `media setup`, `media remove`, `media config`, `media reset`"""