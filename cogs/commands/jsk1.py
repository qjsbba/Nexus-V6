import discord
from discord.ext import commands
import json

class jsk1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Jsk commands"""  

    def help_custom(self):
		      emoji = '<:icons_dev2_3:1144991170028638261>'
		      label = "Jsk"
		      description = "Shows you Jsk Commands."
		      return emoji, label, description

    @commands.group()
    async def __Jsk__(self, ctx: commands.Context):
        """`jsk` , `jsk rtt` , `jsk curl` , `jsk debug` , `jsk sync` , `jsk py` , `jsk permtrace` , `jsk retain` , `jsk tasks` , `jsk timeit` , `jsk dis` , `jsk sql` , `jsk py_inspect` , `jsk hide` , `jsk voice` , `jsk git` , `jsk show` , `jsk cancel` , `jsk shell` , `jsk load` , `jsk unload` , `jsk override` , `jsk invite` , `jsk shutdown` , `jsk pip` , `jsk repeat`"""