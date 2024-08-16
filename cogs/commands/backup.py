import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import psutil
import time
from typing import Optional, Union
import sqlite3
from datetime import datetime, timedelta

# Replace this import with the correct path to your utility functions
from utils.Tools import blacklist_check, iuser_check, ignore_check

start_time = time.time()

class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.hybrid_command(name="statistics",
                             aliases=["st", "stats"],
                             usage="stats",
                             with_app_command=True)
    @blacklist_check()
    @iuser_check()
    @ignore_check()
    async def stats(self, ctx):
        """Shows some useful information about Nexus"""

        # Start with sending the loading message
        loading_message = await ctx.send(embed=discord.Embed(
            color=0x2f3136,
            description="<a:pain_run:1149272995840401428> Fetching Info From Database..."
        ))

        try:
            # Gathering statistics
            await asyncio.sleep(1)  # Simulating delay, adjust as needed

            serverCount = len(self.bot.guilds)
            textchannel = sum(len(guild.text_channels) for guild in self.bot.guilds)
            totalcommands = len(self.bot.commands)
            voicechannel = sum(len(guild.voice_channels) for guild in self.bot.guilds)
            categorichannel = sum(len(guild.categories) for guild in self.bot.guilds)
            total_channels = textchannel + voicechannel + categorichannel
            cached_users = len(self.bot.users)

            # Attempt to gather system usage stats
            try:
                used_memory = psutil.virtual_memory().percent
                cpu_used = psutil.cpu_percent()
            except PermissionError:
                used_memory = "N/A"
                cpu_used = "N/A"
                await ctx.send(embed=discord.Embed(
                    color=0xFF0000,
                    description="⚠️ Unable to fetch system stats due to permission restrictions."
                ))

            shard_count = self.bot.shard_count
            total_members = sum(guild.member_count for guild in self.bot.guilds if guild.member_count is not None)

            pain = await self.bot.fetch_user(1078333867175465162)
            vivek = await self.bot.fetch_user(881087574553264138)

            # Create buttons for interaction
            button_general_info = Button(label="General Info", style=discord.ButtonStyle.primary)
            button_team_info = Button(label="Team Info", style=discord.ButtonStyle.primary)
            button_other_info = Button(label="Other Info", style=discord.ButtonStyle.primary)

            # Create the view to hold the buttons
            view = View()
            view.add_item(button_general_info)
            view.add_item(button_team_info)
            view.add_item(button_other_info)

            # Create the initial embed with general information
            initial_embed = discord.Embed(
                color=0x2f3136,
                description="**Hey, it's me Nexus! A feature-rich, advanced multipurpose bot. Build the community of your dreams with me. Try Nexus now!**"
            )
            initial_embed.set_author(
                name=f"About {self.bot.user.name}",
                icon_url=self.bot.user.display_avatar.url
            )
            initial_embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            initial_embed.add_field(name="**Click a button for more information!**", value="")

            # Send the initial message with buttons
            message = await loading_message.edit(embed=initial_embed, view=view)

            # Button interactions
            async def show_general_info(interaction: discord.Interaction):
                general_info_embed = discord.Embed(
                    title="General Information",
                    color=0x2f3136,
                    description="Here you can find general information about the bot and its functionalities."
                )               
                general_info_embed.add_field(name="**Total Guilds**", value=serverCount)
                general_info_embed.add_field(name="**Total Users**", value=total_members)
                general_info_embed.add_field(name="**Total Commands**", value=totalcommands)
                general_info_embed.add_field(name="**Voice Channels**", value=voicechannel)
                general_info_embed.add_field(name="**Category Channels**", value=categorichannel)
                general_info_embed.add_field(name="**Total Channels**", value=total_channels)
                general_info_embed.add_field(name="**Cached Users**", value=cached_users)
                general_info_embed.add_field(name="**Used Memory (%)**", value=used_memory)
                general_info_embed.add_field(name="**CPU Usage (%)**", value=cpu_used)
                general_info_embed.add_field(name="**Shard Count**", value=shard_count)
                await interaction.response.edit_message(embed=general_info_embed, view=view)

            async def show_team_info(interaction: discord.Interaction):
                team_embed = discord.Embed(
                    title="Nexus Team",
                    color=0x2f3136,
                    description="Meet the amazing team behind Nexus!"
                )
                team_embed.add_field(
                    name="Developer",
                    value=f"[{pain}](https://discord.com/users/1078333867175465162)",
                    inline=False
                )
                team_embed.add_field(
                    name="Team Member",
                    value=f"[{vivek}](https://discord.com/users/881087574553264138)",
                    inline=False
                )
                await interaction.response.edit_message(embed=team_embed, view=view)

            async def show_other_info(interaction: discord.Interaction):
                other_info_embed = discord.Embed(
                    title="Other Information",
                    color=0x2f3136,
                    description="Additional information about the bot's features and functionalities."
                )
                # Add more fields if needed
                await interaction.response.edit_message(embed=other_info_embed, view=view)

            button_general_info.callback = show_general_info
            button_team_info.callback = show_team_info
            button_other_info.callback = show_other_info

        except Exception as e:
            # If something goes wrong, display an error message
            await loading_message.delete()
            await ctx.send(embed=discord.Embed(
                color=0xFF0000,
                description=f"⚠️ An error occurred while fetching the stats: {str(e)}"
            ))


# To add this cog to your bot
async def setup(bot):
    await bot.add_cog(Stats(bot))
