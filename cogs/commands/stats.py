import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import psutil
import platform
import time

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
        loading_message = await ctx.send("<a:pain_run:1149272995840401428> Fetching Info From Database...")
        await asyncio.sleep(1)  # Simulate a delay

        # Delete the loading message
        await loading_message.delete()

        try:
            # Gathering statistics
            server_count = len(self.bot.guilds)
            text_channels = sum(len(guild.text_channels) for guild in self.bot.guilds)
            total_commands = len(self.bot.commands)
            voice_channels = sum(len(guild.voice_channels) for guild in self.bot.guilds)
            category_channels = sum(len(guild.categories) for guild in self.bot.guilds)
            total_channels = text_channels + voice_channels + category_channels
            total_users = sum(guild.member_count for guild in self.bot.guilds if guild.member_count is not None)

            # Attempt to gather system usage stats
            try:
                cpu_model = platform.processor()
                cpu_speed = psutil.cpu_freq().current
                cpu_core = psutil.cpu_count(logical=False)
                cpu_usage = psutil.cpu_percent(interval=1)
                cpu_free = 100 - cpu_usage
                used_memory = psutil.virtual_memory().percent
            except PermissionError:
                cpu_model = "N/A"
                cpu_speed = "N/A"
                cpu_core = "N/A"
                cpu_usage = "N/A"
                cpu_free = "N/A"
                used_memory = "N/A"
                await ctx.send(embed=discord.Embed(
                    color=0xFF0000,
                    description="⚠️ Unable to fetch system stats due to permission restrictions."
                ))

            shard_count = self.bot.shard_count

            # Create buttons for interaction
            button_general_info = Button(label="General Info", style=discord.ButtonStyle.secondary)
            button_system_info = Button(label="System Info", style=discord.ButtonStyle.secondary)
            button_module_info = Button(label="Module Info", style=discord.ButtonStyle.secondary)
            button_team_info = Button(label="Team Info", style=discord.ButtonStyle.secondary)

            # Create the view to hold the buttons
            view = View()
            view.add_item(button_general_info)
            view.add_item(button_system_info)
            view.add_item(button_module_info)
            view.add_item(button_team_info)

            # Create the initial embed with general information
            initial_embed = discord.Embed(
                color=0x2f3136,
                description="**[• Nexus Statistics](https://discord.gg/dwarika)**"
            )
            initial_embed.set_thumbnail(url=ctx.author.display_avatar.url)
            initial_embed.add_field(name="**About Nexus**", value="Hey, it's me Nexus! A feature-rich, advanced multipurpose bot. Build the community of your dreams with me. Try Nexus now!")                     

            # Send the initial message with buttons
            message = await ctx.send(embed=initial_embed, view=view)

            # Store the original user's ID
            original_user_id = ctx.author.id

            # Button interactions
            async def disable_buttons(selected_button: Button):
                for item in view.children:
                    if isinstance(item, Button):
                        item.disabled = item == selected_button

                await message.edit(view=view)

            async def show_general_info(interaction: discord.Interaction):
                if interaction.user.id != original_user_id:
                    return await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)
                
                general_info_embed = discord.Embed(
                    color=0x2f3136,
                    description="**[• Nexus Statistics](https://discord.gg/dwarika)**"
                )
                general_info_embed.set_thumbnail(url=ctx.author.display_avatar.url)
                general_info_embed.add_field(
                    name="__General Info__", 
                    value=(
                        f"**Total Guilds:** {server_count}\n"
                        f"**Total Users:** {total_users}\n"
                        f"**Total Commands:** {total_commands}\n"
                        f"**WebSocket Latency:** {round(self.bot.latency * 1000, 2)}ms"
                    ),
                    inline=False
                )
                general_info_embed.add_field(
                    name="__Channels__", 
                    value=(
                        f"**Total Channels:** {total_channels}\n"
                        f"**Text Channels:** {text_channels}\n"
                        f"**Voice Channels:** {voice_channels}\n"
                        f"**Categories:** {category_channels}"
                    ),
                    inline=False
                )
                
                await interaction.response.edit_message(embed=general_info_embed)
                await disable_buttons(button_general_info)

            async def show_system_info(interaction: discord.Interaction):
                if interaction.user.id != original_user_id:
                    return await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)
                
                system_info_embed = discord.Embed(
                    color=0x2f3136,
                    description="**[• Nexus Statistics](https://discord.gg/dwarika)**"
                )
                system_info_embed.set_thumbnail(url=ctx.author.display_avatar.url)         
                system_info_embed.add_field(
                    name="__System Info__", 
                    value=(
                        f"**CPU Model:** {cpu_model}\n"
                        f"**CPU Speed:** {f'{cpu_speed:.2f} MHz' if isinstance(cpu_speed, float) else cpu_speed}\n"
                        f"**CPU Cores:** {cpu_core}\n"
                        f"**CPU Usage:** {cpu_usage}%\n"
                        f"**CPU Free:** {cpu_free}%\n"
                        f"**Memory Usage:** {used_memory}%"
                    ),
                    inline=False
                )
                
                await interaction.response.edit_message(embed=system_info_embed)
                await disable_buttons(button_system_info)

            async def show_module_info(interaction: discord.Interaction):
                if interaction.user.id != original_user_id:
                    return await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)
                
                module_info_embed = discord.Embed(
                    color=0x2f3136,
                    description="**[• Nexus Statistics](https://discord.gg/dwarika)**"
                )
                module_info_embed.set_thumbnail(url=ctx.author.display_avatar.url)          
                module_info_embed.add_field(
                    name="__Module Info__", 
                    value=(
                        f"**Python Version:** **[3.12.3](https://www.python.org/downloads/release/python-3123/)**\n"
                        f"**discord.py Version:** **[2.4.0](https://pypi.org/project/discord.py/)**\n"
                        f"**Database:** **[SQLite](https://www.sqlite.org/)\n"
                        f"**Platform:** **__{platform.system()}__**\n"
                        f"**Architecture:** **__{platform.architecture()[0]}__"
                    ),
                    inline=False
                )
                
                await interaction.response.edit_message(embed=module_info_embed)
                await disable_buttons(button_module_info)

            async def show_team_info(interaction: discord.Interaction):
                if interaction.user.id != original_user_id:
                    return await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)

                # Define the team members, owners, and sponsors (user IDs)
                developers = {
                    "Ravan": 683768585071493157,
                    "Itzhervoid": 1207080455225213061,
                }
                owners = {
                    "Aditya": 1198144799937675347,
                }
                early_sup = {
                    "Peris.exe": 975111454653038664,
                    "Zombie": 1231241822081126411,
                }

                team_info_embed = discord.Embed(
                    color=0x2f3136,
                    description="**                                                  [• Nexus Statistics](https://discord.gg/dwarika)                                                  **"
                )
                team_info_embed.set_thumbnail(url=ctx.author.display_avatar.url)

                guild = ctx.guild
                if guild is not None:
                    # Add Developer field
                    developer_field_value = " | ".join(
                        f"**{get_status(guild, user_id)} [{name}](https://discord.com/users/{user_id})**"
                        for name, user_id in developers.items()
                    )
                    team_info_embed.add_field(name="__Developers__\n", value=developer_field_value, inline=False)

                    # Add Owner field
                    owner_field_value = " | ".join(
                        f"**{get_status(guild, user_id)} [{name}](https://discord.com/users/{user_id})**"
                        for name, user_id in owners.items()
                    )
                    team_info_embed.add_field(name="__Owners__\n", value=owner_field_value, inline=False)

                    # Add Early Supporters field
                    early_sup_field_value = " | ".join(
                        f"**{get_status(guild, user_id)} [{name}](https://discord.com/users/{user_id})**"
                        for name, user_id in early_sup.items()
                    )
                    team_info_embed.add_field(name="__Early Supporters__\n", value=early_sup_field_value, inline=False)
                
                team_info_embed.set_thumbnail(url=ctx.author.display_avatar.url)
                
                await interaction.response.edit_message(embed=team_info_embed)
                await disable_buttons(button_team_info)

            button_general_info.callback = show_general_info
            button_system_info.callback = show_system_info
            button_module_info.callback = show_module_info
            button_team_info.callback = show_team_info

        except Exception as e:
            # If something goes wrong, display an error message
            await ctx.send(embed=discord.Embed(
                color=0xFF0000,
                description=f"⚠️ An error occurred while fetching the stats: {str(e)}"
            ))

# Utility function to get the status of a member
def get_status(guild, user_id):
    member = guild.get_member(user_id)
    if not member:
        return "Not in server"
    status = {
        discord.Status.online: "<:icons_online:1271851797975400492>",
        discord.Status.idle: "<:LM_Icons_Idle:1271851793223254107>",
        discord.Status.dnd: "<:icons_dnd:1271851720573452369>",
        discord.Status.offline: "<:Icon_invisible:1271851726730956840>"
    }
    return status.get(member.status, "Unknown")

# To add this cog to your bot
async def setup(bot):
    await bot.add_cog(Stats(bot))
