import discord
import aiohttp
import asyncio
from discord.ext import commands
from core import Astroz, Cog
from utils.Tools import *
import logging
import random
from itertools import cycle

logging.basicConfig(level=logging.INFO)

class antibot(Cog):
    def __init__(self, client: Astroz):
        self.client = client
        self.headers = {"Authorization": f"Bot YOUR_BOT_TOKEN_HERE"}  # Replace with your bot token
        self.proxies = self.load_proxies()
        self.proxy_cycle = cycle(self.proxies)
        self.session = aiohttp.ClientSession()

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
    async def on_member_join(self, member: discord.Member) -> None:
        try:
            data = getConfig(member.guild.id)
            anti = getanti(member.guild.id)
            event = getHacker(member.guild.id)
            antibot = event["antinuke"]["antibot"]
            wlrole = data['wlrole']
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlroles = member.guild.get_role(wlrole)
            guild = member.guild

            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
                hacker = guild.get_member(entry.user.id)

                if entry.user.id == guild.owner_id:
                    return

                if str(entry.user.id) in wled or anti == "off" or wlroles in hacker.roles or not antibot:
                    return

                # Ban or kick the bot
                if punishment == "ban":
                    if member.bot:
                        await member.ban()
                elif punishment == "kick":
                    if member.bot:
                        await member.kick()
                
                # Ban or kick the user who added the bot
                if punishment == "ban" and hacker:
                    async with self.session.put(f"https://discord.com/api/v10/guilds/{guild.id}/bans/{hacker.id}", headers=self.headers) as r:
                        if r.status == 429:
                            await self.rate_limit_handler(self.session.put, f"https://discord.com/api/v10/guilds/{guild.id}/bans/{hacker.id}", headers=self.headers)
                elif punishment == "kick" and hacker:
                    async with self.session.delete(f"https://discord.com/api/v10/guilds/{guild.id}/members/{hacker.id}", headers=self.headers) as r:
                        if r.status == 429:
                            await self.rate_limit_handler(self.session.delete, f"https://discord.com/api/v10/guilds/{guild.id}/members/{hacker.id}", headers=self.headers)
                
                # Handle 'none' punishment by removing admin roles if applicable
                if punishment == "none" and member.bot:
                    mem = guild.get_member(member.id)
                    if mem:
                        await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator])

        except discord.Forbidden:
            logging.warning("Forbidden: Unable to perform the action.")
        except Exception as error:
            logging.error(f"Error in on_member_join: {error}")

    async def cog_unload(self):
        await self.session.close()

def setup(client: Astroz):
    client.add_cog(antibot(client))
