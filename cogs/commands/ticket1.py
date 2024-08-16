import discord
from discord.ext import commands
import json

class cool16(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Ticket commands"""  

    def help_custom(self):
		      emoji = '<:codez_ticket:1147375445499727902>'
		      label = "Ticket"
		      description = "Show You Ticket Commands."
		      return emoji, label, description

    @commands.group()
    async def __Tickets__(self, ctx: commands.Context):
        """`sendpanel`"""
       
    

    
   

