import os
import discord
from discord.ext import commands, tasks
import aiohttp
import random
import time
import datetime
import logging
from itertools import cycle
from core import Astroz, Cog
from utils.Tools import *

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

proxies = open('db/proxies.txt').read().split('\n')
proxs = cycle(proxies)
proxies = {"http": 'http://' + next(proxs)}

class antichannel(Cog):
    def __init__(self, client: Astroz):
        self.client = client
        self.headers = {"Authorization": f"Bot MTE0NzE4NTY2NDAwMjEwMTI0OA.GOcrWX.jxET9HPK-8i1TjPNAUgMYcCO68i0nuJ-gwptcA"}
        self.processing = []

    @tasks.loop(seconds=15)
    async def clean_processing(self):
        self.processing.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.clean_processing.start()

    async def delete(self, channel: discord.abc.GuildChannel):
        try:
            await channel.delete()
        except Exception as e:
            logging.error(f"Failed to delete channel: {e}")

    async def remove_admin_roles(self, member: discord.Member, reason: str):
        bot_role = discord.utils.get(member.guild.roles, id=self.client.user.top_role.id)
        roles_to_remove = [role for role in member.roles if role.position > bot_role.position and role.permissions.administrator]
        
        if roles_to_remove:
            try:
                await member.remove_roles(*roles_to_remove, reason=reason)
                logging.info(f"Removed admin roles from {member.id} with reason: {reason}")
            except Exception as e:
                logging.error(f"Failed to remove roles from {member.id}: {e}")

    async def punish_user(self, guild, user_id, punishment, reason, channel=None, before=None, after=None):
        api_version = random.randint(8, 9)
        async with aiohttp.ClientSession(headers=self.headers) as session:
            if punishment == "ban":
                async with session.put(f"https://discord.com/api/v{api_version}/guilds/{guild.id}/bans/{user_id}", json={"reason": reason}) as r:
                    if r.status in (200, 201, 204):
                        logging.info(f"Successfully banned {user_id}")
                        if channel:
                            await self.delete(channel)
                        elif before and after:
                            await after.edit(
                                name=before.name, 
                                topic=before.topic, 
                                nsfw=before.nsfw, 
                                category=before.category, 
                                slowmode_delay=before.slowmode_delay, 
                                type=before.type, 
                                overwrites=before.overwrites, 
                                reason=reason
                            )
            elif punishment == "kick":
                async with session.delete(f"https://discord.com/api/v{api_version}/guilds/{guild.id}/members/{user_id}", json={"reason": reason}) as r2:
                    if r2.status in (200, 201, 204):
                        logging.info(f"Successfully kicked {user_id}")
                        if channel:
                            await self.delete(channel)
                        elif before and after:
                            await after.edit(
                                name=before.name, 
                                topic=before.topic, 
                                nsfw=before.nsfw, 
                                category=before.category, 
                                slowmode_delay=before.slowmode_delay, 
                                type=before.type, 
                                overwrites=before.overwrites, 
                                reason=reason
                            )
            elif punishment == "none":
                member = guild.get_member(user_id)
                if member:
                    await self.remove_admin_roles(member, reason)
                    if channel:
                        await self.delete(channel)
                    elif before and after:
                        await after.edit(
                            name=before.name, 
                            topic=before.topic, 
                            nsfw=before.nsfw, 
                            category=before.category, 
                            slowmode_delay=before.slowmode_delay, 
                            type=before.type, 
                            overwrites=before.overwrites, 
                            reason=reason
                        )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel) -> None:
        try:
            start = time.perf_counter()
            data = getConfig(channel.guild.id)
            anti = getanti(channel.guild.id)
            event = getHacker(channel.guild.id)
            antievent = event["antinuke"]["antichannel-create"]
            punishment = data["punishment"]
            wlrole = data['wlrole']
            wled = data["whitelisted"]
            guild = channel.guild
            wlroles = guild.get_role(wlrole)
            reason = "Channel Created | Not Whitelisted"

            async for entry in guild.audit_logs(limit=1):
                user = entry.user
                hacker = guild.get_member(entry.user.id)

            if user.id == self.client.user.id or user.id == guild.owner_id or str(user.id) in wled or anti == "off" or wlroles in hacker.roles or not antievent:
                return
            else:
                if entry.action == discord.AuditLogAction.channel_create:
                    await self.punish_user(guild, user.id, punishment, reason, channel=channel)
            end = time.perf_counter()
            logging.info(f"Action completed in {end - start:.2f} seconds")

        except Exception as error:
            if isinstance(error, discord.Forbidden):
                return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel) -> None:
        try:
            data = getConfig(channel.guild.id)
            anti = getanti(channel.guild.id)
            event = getHacker(channel.guild.id)
            antievent = event["antinuke"]["antichannel-delete"]
            wlrole = data['wlrole']
            punishment = data["punishment"]
            wled = data["whitelisted"]
            guild = channel.guild
            wlroles = guild.get_role(wlrole)
            reason = "Channel Deleted | Not Whitelisted"

            async for entry in guild.audit_logs(limit=1):
                user = entry.user
                hacker = guild.get_member(entry.user.id)

            if user.id == self.client.user.id or user.id == guild.owner_id or str(user.id) in wled or anti == "off" or wlroles in hacker.roles or not antievent:
                return
            else:
                if entry.action == discord.AuditLogAction.channel_delete:
                    await self.punish_user(guild, user.id, punishment, reason)
                    await channel.clone(reason=reason)

        except Exception as error:
            if isinstance(error, discord.Forbidden):
                return

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after) -> None:
        try:
            data = getConfig(before.guild.id)
            anti = getanti(before.guild.id)
            event = getHacker(before.guild.id)
            antievent = event["antinuke"]["antichannel-update"]
            wlrole = data['wlrole']
            punishment = data["punishment"]
            wled = data["whitelisted"]
            guild = after.guild
            wlroles = guild.get_role(wlrole)
            reason = "Channel Updated | Not Whitelisted"

            async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.utcnow() - datetime.timedelta(seconds=30)):
                user = entry.user
                hacker = guild.get_member(entry.user.id)

            if user.id == self.client.user.id or user.id == guild.owner_id or str(user.id) in wled or anti == "off" or wlroles in hacker.roles or not antievent:
                return
            else:
                if entry.action == discord.AuditLogAction.channel_update or entry.action == discord.AuditLogAction.overwrite_update:
                    await self.punish_user(guild, user.id, punishment, reason, before=before, after=after)

        except Exception as error:
            if isinstance(error, discord.Forbidden):
                return
