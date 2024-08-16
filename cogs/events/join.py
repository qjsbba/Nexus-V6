import os
import discord
import aiohttp
from discord.ext import commands, tasks
from discord.colour import Color
import json
import random
from discord.ui import Button, View



class Join(commands.Cog):
    def __init__(self, client):
        self.client = client

    

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
          embed = discord.Embed(
            description=f"Thank you for adding me to your server!\n・ My default prefix is `$`\n・ You can use the `$help` command to get list of commands\n・ Our [support server](https://discord.gg/zvU2mGPa6Y) or our team offers detailed information & guides for commands\n・ Feel free to join our [Support Server](https://discord.gg/zvU2mGPa6Y) if you need help/support for anything related to the bot",
            color=0x00FFED
          )
          velocity = Button(label='Support Server', style=discord.ButtonStyle.link, url='https://discord.gg/zvU2mGPa6Y')
          velocity1 = Button(label='Invite Me',style=discord.ButtonStyle.link,url=f'https://discord.com/api/oauth2/authorize?client_id=1096394407823028276&permissions=2199022730751&scope=bot%20applications.commands')

          #velo1 = Button(label='Vote Me',style=discord.ButtonStyle.link,url='https://top.gg/bot/1006557956109779015/vote')
          view = View()
          view.add_item(velocity) 
          view.add_item(velocity1)
          #view.add_item(velo1)
          embed.set_author(name=f"{guild.name}",
                             icon_url=guild.icon.url)
          embed.set_thumbnail(url=guild.owner.avatar.url)
          await guild.owner.send(embed=embed,view=view)


