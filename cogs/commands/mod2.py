import discord
from discord.ext import commands


class hacker111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Moderation commands"""
  
    def help_custom(self):
		      emoji = '<:codez_mod:1147375141924388924>'
		      label = "Moderation"
		      description = "Shows You Moderation Commands."
		      return emoji, label, description

    @commands.group()
    async def __Moderation__(self, ctx: commands.Context):
        """`setprefix` , `mute` , `unmute` , `kick` , `warn` , `ban` , `unban` , `clone` , `nick` , `slowmode` , `unslowmode` , `clear` , `clear all` , `clear bots` , `clear embeds` , `clear files` , `clear mentions` , `clear images` , `clear contains` , `clear reactions` , `clear user` , `clear emoji` , `nuke` , `lock` , `unlock` , `hide` , `unhide` , `hideall` , `unhideall` , `audit` , `role` , `role temp` , `role remove` , `role delete` , `role create` , `role rename` , `enlarge` , `role human` , `role bot` , `role all` , `removerole human` , `removerole bot` , `removerole all` , `admin add` , `admin remove` , `admin show` , `admin role` , `admin reset` , `roleicon`, `steal` , `deleteemoji` , `deletesticker` , `addsticker`,`antialt`"""