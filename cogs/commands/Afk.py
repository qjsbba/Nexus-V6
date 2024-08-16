import discord
from discord.ext import commands
import json
import time
from typing import Optional

afk_path = "db/afk.json"

class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: Optional[int] = None):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.value = None
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                embed=discord.Embed(description=f"Only **{self.ctx.author}** can use this command.", color=0xFF0000),
                ephemeral=True
            )
            return False
        return True

class OnOrOff(BasicView):
    @discord.ui.button(label="Global AFK", style=discord.ButtonStyle.secondary)
    async def global_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 'Global'
        self.stop()

    @discord.ui.button(label="Server AFK", style=discord.ButtonStyle.secondary)
    async def server_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 'Server'
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 'Cancel'
        self.stop()

class AFK(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def time_formatter(self, seconds: float):
        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return ((str(days) + " days, ") if days else "") + \
               ((str(hours) + " hours, ") if hours else "") + \
               ((str(minutes) + " minutes, ") if minutes else "") + \
               ((str(seconds) + " seconds, ") if seconds else "")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        try:
            with open(afk_path, 'r') as f:
                afk_data = json.load(f)

            user_id = str(message.author.id)

            # Remove AFK status if the user sends a message
            if user_id in afk_data:
                afk_info = afk_data[user_id]
                if afk_info['AFK'] == 'True':
                    if afk_info['scope'] == 'Global' or (afk_info['scope'] == 'Server' and message.guild.id in afk_info['servers']):
                        afk_info['AFK'] = 'False'
                        afk_info['time'] = None
                        afk_info['reason'] = None
                        pings = afk_info.get('pings', [])
                        ping_count = len(pings)

                        with open(afk_path, 'w') as f:
                            json.dump(afk_data, f)

                        elapsed_time = await self.time_formatter(time.time() - afk_info['start_time'])
                        ping_messages = '\n'.join(pings)
                        await message.channel.send(
                            embed=discord.Embed(description=f"**Welcome back {message.author.mention}!**\n**I Have Removed Your AFK Status**\n**You were AFK for {elapsed_time}.**\n**You were pinged {ping_count} times:**\n{ping_messages}", color=0x2F3136)
                        )

            # Track pings if the user is AFK
            if message.mentions:
                afk_users = [user for user in message.mentions if str(user.id) in afk_data]
                if afk_users:
                    for user in afk_users:
                        afk_info = afk_data[str(user.id)]
                        if afk_info['AFK'] == 'True':
                            if afk_info['scope'] == 'Global' or (afk_info['scope'] == 'Server' and message.guild.id in afk_info['servers']):
                                ping_number = len(afk_info.setdefault('pings', [])) + 1
                                ping_entry = f"[Ping {ping_number}]({message.jump_url})"
                                afk_info['pings'].append(ping_entry)

                                with open(afk_path, 'w') as f:
                                    json.dump(afk_data, f)

                                afk_reason = afk_info['reason']
                                start_time = afk_info['start_time']
                                elapsed_time = await self.time_formatter(time.time() - start_time)

                                await message.channel.send(
                                    embed=discord.Embed(description=f"{user.mention} is AFK: {afk_reason} (AFK for {elapsed_time})", color=0x2F3136)
                                )
        except KeyError:
            pass

    @commands.hybrid_command(description="Set your AFK status.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def afk(self, ctx: commands.Context, *, reason: str = "I'm AFK"):
        view = OnOrOff(ctx)
        embed = discord.Embed(description="**<:ask:1271200784230387785> Would You Like Nexus To Set Your AFK Globally Or For This Server Only**", color=0x2F3136)
        message = await ctx.send(embed=embed, view=view)
        
        await view.wait()

        if view.value is None or view.value == 'Cancel':
            return await message.edit(content="AFK setup canceled.", embed=None, view=None)
        
        afk_scope = view.value
        
        with open(afk_path, 'r') as f:
            afk_data = json.load(f)

        afk_data[str(ctx.author.id)] = {
            'AFK': 'True',
            'reason': reason,
            'start_time': time.time(),
            'scope': afk_scope,
            'servers': [ctx.guild.id] if afk_scope == 'Server' else [],
            'pings': []
        }

        with open(afk_path, 'w') as f:
            json.dump(afk_data, f)

        await message.delete()
        await ctx.send(embed=discord.Embed(description=f"**<:ok_manoo:1271201165656461404> {ctx.author.mention} I Have Successfully Set Your AFK With The Reason Of **__{reason}__** [ {afk_scope} AFK ]**", color=0x2F3136))

async def setup(client):
    await client.add_cog(AFK(client))
