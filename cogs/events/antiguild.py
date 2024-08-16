import discord
import aiohttp
import asyncio
import logging
from discord.ext import commands, tasks
from core import Astroz, Cog
from utils.Tools import getConfig, getanti, getHacker  # Ensure these functions are available
from itertools import cycle

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class antiguild(Cog):
    def __init__(self, client: Astroz):
        self.client = client
        self.headers = {"Authorization": f"Bot MTE0NzE4NTY2NDAwMjEwMTI0OA.GOcrWX.jxET9HPK-8i1TjPNAUgMYcCO68i0nuJ-gwptcA"}  # Replace with actual token
        self.proxies = self.load_proxies()
        self.proxy_cycle = cycle(self.proxies)
        self.session = aiohttp.ClientSession()
        self.processing = []
        self.clean_processing.start()

    def load_proxies(self):
        try:
            with open('db/proxies.txt') as f:
                proxies = [line.strip() for line in f if line.strip()]
                return [{"http": f"http://{proxy}", "https": f"http://{proxy}"} for proxy in proxies]
        except FileNotFoundError:
            logging.error("Proxies file not found.")
            return []

    @tasks.loop(seconds=15)
    async def clean_processing(self):
        self.processing.clear()

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

    async def punish_user(self, guild, user, punishment, reason="Punishment for guild update"):
        punishment_methods = {
            "ban": self.ban_user,
            "kick": self.kick_user,
            "none": self.remove_admin_roles
        }
        method = punishment_methods.get(punishment)
        if method:
            await method(guild, user, reason)

    async def ban_user(self, guild, user, reason):
        url = f"https://discord.com/api/v10/guilds/{guild.id}/bans/{user.id}"
        async with self.session.put(url, headers=self.headers, proxy=next(self.proxy_cycle)) as response:
            if response.status == 429:
                await self.rate_limit_handler(self.session.put, url, headers=self.headers, proxy=next(self.proxy_cycle))
            await guild.ban(user, reason=reason)
            logging.info(f"Successfully banned {user.id}.")

    async def kick_user(self, guild, user, reason):
        url = f"https://discord.com/api/v10/guilds/{guild.id}/members/{user.id}"
        async with self.session.delete(url, headers=self.headers, proxy=next(self.proxy_cycle)) as response:
            if response.status == 429:
                await self.rate_limit_handler(self.session.delete, url, headers=self.headers, proxy=next(self.proxy_cycle))
            await guild.kick(user, reason=reason)
            logging.info(f"Successfully kicked {user.id}.")

    async def remove_admin_roles(self, guild, user, reason):
        member = guild.get_member(user.id)
        if member:
            await member.edit(roles=[role for role in member.roles if not role.permissions.administrator], reason=reason)
            logging.info(f"Removed admin roles from {user.id}.")

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        try:
            data = getConfig(after.id)
            anti = getanti(after.id)
            event = getHacker(after.id)
            anti_update = event["antinuke"]["antiupdate"]
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data['wlrole']
            wlroles = after.get_role(wlrole)

            if not anti_update:
                return

            async for entry in after.audit_logs(limit=1, action=discord.AuditLogAction.guild_update):
                user = entry.user
                if user.id == self.client.user.id or user == after.owner:
                    return
                if str(user.id) in wled or (wlroles and wlroles in user.roles):
                    return

                await self.punish_user(after, user, punishment)

                # Reset guild settings to the before state
                await after.edit(
                    name=before.name,
                    description=before.description,
                    verification_level=before.verification_level,
                    icon=before.icon,
                    rules_channel=before.rules_channel,
                    afk_channel=before.afk_channel,
                    afk_timeout=before.afk_timeout,
                    default_notifications=before.default_notifications,
                    explicit_content_filter=before.explicit_content_filter,
                    system_channel=before.system_channel,
                    system_channel_flags=before.system_channel_flags,
                    public_updates_channel=before.public_updates_channel,
                    reason="Restored to original state due to guild update."
                )

        except discord.Forbidden:
            logging.warning("Forbidden: Unable to perform the action.")
        except Exception as error:
            logging.error(f"Error in on_guild_update: {error}")

    async def cog_unload(self):
        await self.session.close()

def setup(client: Astroz):
    client.add_cog(antiguild(client))
    