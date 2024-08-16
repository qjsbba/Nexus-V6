import discord
from discord.ext import commands, tasks
from discord.ui import Select, View
import json
import os


class ActivityRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_activity_data()
        self.check_activity.start()

    def load_activity_data(self):
        if os.path.exists("db/activity_roles.json"):
            with open("db/activity_roles.json", "r") as file:
                self.activity_data = json.load(file)
        else:
            self.activity_data = {}

    def save_activity_data(self):
        with open("activity_roles.json", "w") as file:
            json.dump(self.activity_data, file, indent=4)

    @commands.group(
        name="activityrole",
        invoke_without_command=True,
        description="Shows the activity role's help menu"
    )
    async def activityrole(self, ctx):
        embed = discord.Embed(
            title="Activity Role Commands",
            description="Use the commands below to manage activity role settings.",
            color=0x2f3136
        )
        embed.add_field(name="ActivityRole Setup", value="Setup activity roles.", inline=False)
        embed.add_field(name="ActivityRole Logs", value="Setup a channel to log activity role events.", inline=False)
        embed.add_field(name="ActivityRole Status", value="Show current activity role settings for this guild.", inline=False)
        embed.add_field(name="ActivityRole Reset", value="Reset all activity role configurations for this server.", inline=False)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=embed)

    @activityrole.command(name="setup", description="Setup activity roles")
    @commands.has_permissions(administrator=True)
    async def setup_activityrole(self, ctx):
        view = ActivityRoleSetupView(self.bot)
        embed = discord.Embed(
            title="ActivityRole Setup",
            description="Select the activity role you want to enable:",
            color=0x2f3136
        )
        await ctx.reply(embed=embed, view=view)

    @activityrole.command(name="logs", description="Setup a channel to log activity role events")
    @commands.has_permissions(administrator=True)
    async def setup_logs(self, ctx):
        await ctx.reply(embed=discord.Embed(title="Channel Selection", description=f"Please Mention the channel or provide the Channel ID for Set ActivityRole Logs.", color=0x2f3136), ephemeral=True)


        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60)
            channel_id = int(msg.content.strip('<>#'))
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                self.activity_data[str(ctx.guild.id)]["log_channel"] = channel.id
                self.save_activity_data()
                await ctx.reply(embed=discord.Embed(description=f"<:hacker_tick:1271209580793167925> | Successfully set up the log channel to {channel.mention}."))
            else:
                raise ValueError("Invalid channel")
        except:
            await ctx.reply("Invalid channel. Please try the setup command again.")

    @activityrole.command(name="status", description="Show current activity role settings for this guild")
    @commands.has_permissions(administrator=True)
    async def status(self, ctx):
        guild_id = str(ctx.guild.id)
        embed = discord.Embed(
            description=f"Current Activity Role Settings for **{ctx.guild}**",
            color=0x2f3136
        )
        activities = ["Spotify", "Game", "Streaming"]
        for activity in activities:
            role_id = self.activity_data.get(guild_id, {}).get(activity, None)
            status_text = "Enabled" if role_id else "Disabled"
            status_emoji = "<:nexusenable:1272458135822532679>" if role_id else "<:nexusdisable:1272458087713734717>"
            role_mention = f"<@&{role_id}>" if role_id else "N/A"
            embed.add_field(name=f"{activity} {status_emoji}", value=f"{activity} is Currently **{status_text}** with role {role_mention}.", inline=False)

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_author(name="Activity Role Status", icon_url=self.bot.user.display_avatar.url)
        await ctx.reply(embed=embed)

    @activityrole.command(name="reset", description="Reset all activity role configurations for this server")
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id in self.activity_data:
            del self.activity_data[guild_id]
            self.save_activity_data()
            await ctx.reply(embed=discord.Embed(description=f"All activity role configurations for **{ctx.guild}** have been reset", color=0x2f3136))

        else:
            await ctx.reply(f"No activity role Configurations found for **{ctx.guild.name}**.")

    @tasks.loop(seconds=1)
    async def check_activity(self):
        for guild in self.bot.guilds:
            guild_id = str(guild.id)
            for member in guild.members:
                if not member.bot:
                    await self.update_member_activity_roles(member, guild_id)

    async def update_member_activity_roles(self, member, guild_id):
        activity_roles = self.activity_data.get(guild_id, {})
        current_roles = set(role.id for role in member.roles)
        for activity, role_id in activity_roles.items():
            if activity == "log_channel":
                continue
            role = member.guild.get_role(role_id)
            if role:
                if activity == "Spotify" and any(a.type == discord.ActivityType.listening and a.name == "Spotify" for a in member.activities):
                    if role_id not in current_roles:
                        await member.add_roles(role)
                        await self.log_event(member.guild, f"{activity} activity detected", member, role, "added")
                elif activity == "Game" and any(a.type == discord.ActivityType.playing for a in member.activities):
                    if role_id not in current_roles:
                        await member.add_roles(role)
                        await self.log_event(member.guild, f"{activity} activity detected", member, role, "added")
                elif activity == "Streaming" and any(a.type == discord.ActivityType.streaming for a in member.activities):
                    if role_id not in current_roles:
                        await member.add_roles(role)
                        await self.log_event(member.guild, f"{activity} activity detected", member, role, "added")
                else:
                    if role_id in current_roles:
                        await member.remove_roles(role)
                        await self.log_event(member.guild, f"{activity} activity ended", member, role, "removed")

    async def log_event(self, guild, description, member, role, action):
        log_channel_id = self.activity_data.get(str(guild.id), {}).get("log_channel", None)
        if log_channel_id:
            log_channel = guild.get_channel(log_channel_id)
            if log_channel:
                embed = discord.Embed(
                    title="Activity Role Update",
                    description=f"**{description}**\n\n**Member:** {member.mention}\n**Role:** {role.mention}\n**Action:** {action}",
                    color=discord.Color.green() if action == "added" else discord.Color.red()
                )
                embed.set_author(name="Sage ActivityRole System!", icon_url=self.bot.user.display_avatar.url)
                embed.set_thumbnail(url=member.avatar.url)
                await log_channel.send(embed=embed)

class ActivityRoleSetupView(View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.bot = bot
        self.add_item(ActivityRoleSelect(bot))

class ActivityRoleSelect(Select):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2f3136
        self.greencolor = 0x00FF00
        options = [
            discord.SelectOption(label="Spotify", emoji="<:spotify:1272459249288482836>", description="Assign role when user is listening to Spotify."),
            discord.SelectOption(label="Game", emoji="<:games:1272459732761968734>", description="Assign role when user is playing a game."),
            discord.SelectOption(label="Streaming", emoji="<:Streaming:1272459922054971475>", description="Assign role when user is streaming.")
        ]
        super().__init__(placeholder="Choose an activity role...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        activity = self.values[0]
        await self.setup_activity_role(interaction, activity)

    async def setup_activity_role(self, interaction: discord.Interaction, activity: str):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.bot.cogs['ActivityRole'].activity_data:
            self.bot.cogs['ActivityRole'].activity_data[guild_id] = {}

        if activity in self.bot.cogs['ActivityRole'].activity_data[guild_id]:
            await interaction.response.send_message(embed=discord.Embed(title="Error Found", description=f"**{activity}** is already enabled for this server.", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Role Selection", description=f"Please mention the role or provide the role ID for **{activity}**.", color=self.color), ephemeral=True)

            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
                role_id = int(msg.content.strip('<@&>'))
                role = interaction.guild.get_role(role_id)
                if role:
                    self.bot.cogs['ActivityRole'].activity_data[guild_id][activity] = role.id
                    self.bot.cogs['ActivityRole'].save_activity_data()
                    await interaction.followup.send(embed=discord.Embed(title="Role Assigned", description=f"Successfully assigned **{role.mention}** for **{activity}** activity.", color=self.greencolor))
                else:
                    await interaction.followup.send(embed=discord.Embed(title="Error Found", description="Invalid role. Please try the setup command again.", color=discord.Color.red()), ephemeral=True)
            except:
                await interaction.followup.send(embed=discord.Embed(title="Error Found", description="Invalid input or timeout. Please try the setup command again.", color=discord.Color.red()), ephemeral=True)

async def setup(bot):
    await bot.add_cog(ActivityRole(bot))


