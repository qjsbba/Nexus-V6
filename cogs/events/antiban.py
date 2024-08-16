import os
import discord
from discord.ext import commands, tasks
import aiohttp
import logging
import random
from itertools import cycle
from core import Astroz, Cog
from utils.Tools import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

# Read proxies
proxies = open('db/proxies.txt').read().split('\n')
proxs = cycle(proxies)
proxies = {"http": 'http://' + next(proxs)}

class antiban(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.headers = {"Authorization": f"Bot MTE0NzE4NTY2NDAwMjEwMTI0OA.GOcrWX.jxET9HPK-8i1TjPNAUgMYcCO68i0nuJ-gwptcA"}
        self.processing = []

    @tasks.loop(seconds=15)
    async def clean_processing(self):
        self.processing.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.clean_processing.start()

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        try:
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            event = getHacker(guild.id)
            antiban = event["antinuke"]["antiban"]
            wlrole = data['wlrole']  
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlroles = guild.get_role(wlrole)
            reason = "Banning Members | Not Whitelisted"
            api = random.randint(8, 9)

            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                user_id = entry.user.id
                hacker = guild.get_member(entry.user.id)
                
                if entry.user.id == self.client.user.id or entry.user.id == guild.owner_id or str(entry.user.id) in wled or anti == "off" or wlroles in hacker.roles or not antiban:
                    return
                
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    if punishment == "ban":
                        async with session.put(f"https://discord.com/api/v{api}/guilds/{guild.id}/bans/{user_id}", json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info(f"Successfully banned {user_id}")
                            await guild.unban(user=user)
                    elif punishment == "kick":
                        async with session.delete(f"https://discord.com/api/v{api}/guilds/{guild.id}/members/{user_id}", json={"reason": reason}) as r2:
                            if r2.status in (200, 201, 204):
                                logging.info(f"Successfully kicked {user_id}")
                            await guild.unban(user=user)
                    elif punishment == "none":
                        mem = guild.get_member(user_id)
                        if mem:
                            await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator], reason=reason)
                            logging.info(f"Removed admin roles from {user_id}")
                            await guild.unban(user=user)
        except discord.Forbidden:
            logging.warning("Forbidden: Unable to perform the action.")
        except Exception as e:
            logging.error(f"Error in on_member_ban: {e}")

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        try:
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            event = getHacker(guild.id)
            antiban = event["antinuke"]["antiban"]
            wled = data["whitelisted"]
            punishment = data["punishment"]
            wlrole = data['wlrole']
            wlroles = guild.get_role(wlrole)
            reason = "Unbanning Members | Not Whitelisted"
            api = random.randint(8, 9)

            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
                user_id = entry.user.id
                hacker = guild.get_member(entry.user.id)

                if entry.user.id == self.client.user.id or entry.user.id == guild.owner_id or str(entry.user.id) in wled or anti == "off" or wlroles in hacker.roles or not antiban:
                    return
                
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    if punishment == "ban":
                        async with session.put(f"https://discord.com/api/v{api}/guilds/{guild.id}/bans/{user_id}", json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info(f"Successfully banned {user_id}")
                            await guild.ban(discord.Object(id=user.id), reason="Unauthorized Unban - Victim Re-Banned")
                    elif punishment == "kick":
                        async with session.delete(f"https://discord.com/api/v{api}/guilds/{guild.id}/members/{user_id}", json={"reason": reason}) as r2:
                            if r2.status in (200, 201, 204):
                                logging.info(f"Successfully kicked {user_id}")
                            await guild.ban(discord.Object(id=user.id), reason="Unauthorized Unban - Victim Re-Banned")
                    elif punishment == "none":
                        mem = guild.get_member(user_id)
                        if mem:
                            await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator], reason=reason)
                            logging.info(f"Removed admin roles from {user_id}")
                            await guild.ban(discord.Object(id=user.id), reason="Unauthorized Unban - Victim Re-Banned")
        except discord.Forbidden:
            logging.warning("Forbidden: Unable to perform the action.")
        except Exception as e:
            logging.error(f"Error in on_member_unban: {e}")

def setup(client):
    client.add_cog(antiban(client))
