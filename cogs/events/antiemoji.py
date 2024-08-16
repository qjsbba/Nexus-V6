
import os
import discord
import aiohttp
import asyncio
import logging
from discord.ext import commands
from core import Astroz, Cog
from utils.Tools import *
import random
from itertools import cycle

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class antiemoji(Cog):
    def __init__(self, client: Astroz):
        self.client = client
        self.headers = {"Authorization": f"Bot MTE0NzE4NTY2NDAwMjEwMTI0OA.GOcrWX.jxET9HPK-8i1TjPNAUgMYcCO68i0nuJ-gwptcA"}
        self.proxies = self.load_proxies()
        self.proxy_cycle = cycle(self.proxies)
        self.session = aiohttp.ClientSession()
        self.tracked_emojis = {}  # Track emoji IDs

    def load_proxies(self):
        try:
            with open('db/proxies.txt') as f:
                proxies = [line.strip() for line in f if line.strip()]
                return [{"http": f"http://{proxy}", "https": f"http://{proxy}"} for proxy in proxies]
        except FileNotFoundError:
            logging.error("Proxies file not found.")
            return []

    async def rate_limit_handler(self, request_func, *args, **kwargs):
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = await request_func(*args, **kwargs)
                if response.status == 429:
                    retry_after = int(response.headers.get('Retry-After', 1))
                    logging.info(f"Rate limited. Retrying after {retry_after} seconds.")
                    await asyncio.sleep(retry_after)
                else:
                    return response
            except Exception as e:
                logging.error(f"Error during request: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                else:
                    raise
        return None

    @commands.Cog.listener()
    async def on_emoji_create(self, emoji: discord.Emoji):
        try:
            guild = emoji.guild
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            event = getHacker(guild.id)
            antiemoji_create = event["antinuke"]["antiemoji-create"]
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data['wlrole']
            wlroles = guild.get_role(wlrole)

            if not antiemoji_create:
                return

            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_create):
                user = entry.user

                if user.id == self.client.user.id or user == guild.owner or str(user.id) in wled or wlroles in user.roles:
                    return

                if punishment == "ban":
                    async with self.session.put(f"https://discord.com/api/v10/guilds/{guild.id}/bans/{user.id}", headers=self.headers) as r:
                        if r.status == 429:
                            await self.rate_limit_handler(self.session.put, f"https://discord.com/api/v10/guilds/{guild.id}/bans/{user.id}", headers=self.headers)
                        await emoji.delete()
                        logging.info(f"Successfully banned {user.id} and deleted emoji.")
                
                elif punishment == "kick":
                    async with self.session.delete(f"https://discord.com/api/v10/guilds/{guild.id}/members/{user.id}", headers=self.headers) as r:
                        if r.status == 429:
                            await self.rate_limit_handler(self.session.delete, f"https://discord.com/api/v10/guilds/{guild.id}/members/{user.id}", headers=self.headers)
                        await emoji.delete()
                        logging.info(f"Successfully kicked {user.id} and deleted emoji.")
                
                elif punishment == "none":
                    mem = guild.get_member(user.id)
                    if mem:
                        await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator])
                        await emoji.delete()
                        logging.info(f"Deleted emoji and removed admin roles from {user.id}.")
        
        except discord.Forbidden:
            logging.warning("Forbidden: Unable to perform the action.")
        except Exception as error:
            logging.error(f"Error in on_emoji_create: {error}")

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before, after):
        try:
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            event = getHacker(guild.id)
            antiemoji_delete = event["antinuke"]["antiemoji-delete"]
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data['wlrole']
            wlroles = guild.get_role(wlrole)

            if not antiemoji_delete:
                return

            deleted_emojis = [emoji for emoji in before if emoji not in after]

            for emoji in deleted_emojis:
                async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_delete):
                    user = entry.user

                    if user.id == self.client.user.id or user == guild.owner or str(user.id) in wled or wlroles in user.roles:
                        return

                    if punishment == "ban":
                        async with self.session.put(f"https://discord.com/api/v10/guilds/{guild.id}/bans/{user.id}", headers=self.headers) as r:
                            if r.status == 429:
                                await self.rate_limit_handler(self.session.put, f"https://discord.com/api/v10/guilds/{guild.id}/bans/{user.id}", headers=self.headers)
                            await guild.create_custom_emoji(name=emoji.name, image=await emoji.read())
                            logging.info(f"Successfully banned {user.id} and restored deleted emoji.")
                    
                    elif punishment == "kick":
                        async with self.session.delete(f"https://discord.com/api/v10/guilds/{guild.id}/members/{user.id}", headers=self.headers) as r:
                            if r.status == 429:
                                await self.rate_limit_handler(self.session.delete, f"https://discord.com/api/v10/guilds/{guild.id}/members/{user.id}", headers=self.headers)
                            await guild.create_custom_emoji(name=emoji.name, image=await emoji.read())
                            logging.info(f"Successfully kicked {user.id} and restored deleted emoji.")
                    
                    elif punishment == "none":
                        mem = guild.get_member(user.id)
                        if mem:
                            await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator])
                            await guild.create_custom_emoji(name=emoji.name, image=await emoji.read())
                            logging.info(f"Restored deleted emoji and removed admin roles from {user.id}.")
        
        except discord.Forbidden:
            logging.warning("Forbidden: Unable to perform the action.")
        except Exception as error:
            logging.error(f"Error in on_guild_emojis_update: {error}")

    @commands.Cog.listener()
    async def on_emoji_delete(self, emoji: discord.Emoji):
        try:
            guild = emoji.guild
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            event = getHacker(guild.id)
            antiemoji_delete = event["antinuke"]["antiemoji-delete"]
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data['wlrole']
            wlroles = guild.get_role(wlrole)

            if not antiemoji_delete:
                return

            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_delete):
                user = entry.user

                if user.id == self.client.user.id or user == guild.owner or str(user.id) in wled or wlroles in user.roles:
                    return

                if punishment == "ban":
                    async with self.session.put(f"https://discord.com/api/v10/guilds/{guild.id}/bans/{user.id}", headers=self.headers) as r:
                        if r.status == 429:
                            await self.rate_limit_handler(self.session.put, f"https://discord.com/api/v10/guilds/{guild.id}/bans/{user.id}", headers=self.headers)
                        await guild.create_custom_emoji(name=emoji.name, image=await emoji.read())
                        logging.info(f"Successfully banned {user.id} and restored deleted emoji.")
                
                elif punishment == "kick":
                    async with self.session.delete(f"https://discord.com/api/v10/guilds/{guild.id}/members/{user.id}", headers=self.headers) as r:
                        if r.status == 429:
                            await self.rate_limit_handler(self.session.delete, f"https://discord.com/api/v10/guilds/{guild.id}/members/{user.id}", headers=self.headers)
                        await guild.create_custom_emoji(name=emoji.name, image=await emoji.read())
                        logging.info(f"Successfully kicked {user.id} and restored deleted emoji.")
                
                elif punishment == "none":
                    mem = guild.get_member(user.id)
                    if mem:
                        await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator])
                        await guild.create_custom_emoji(name=emoji.name, image=await emoji.read())
                        logging.info(f"Restored deleted emoji and removed admin roles from {user.id}.")
        
        except discord.Forbidden:
            logging.warning("Forbidden: Unable to perform the action.")
        except Exception as error:
            logging.error(f"Error in on_emoji_delete: {error}")

    async def cog_unload(self):
        await self.session.close()

def setup(client: Astroz):
    client.add_cog(antiemoji(client))
