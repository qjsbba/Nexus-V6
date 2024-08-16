import os
import discord
from discord.ext import commands
import aiohttp
import logging
import time
import asyncio
import random
from utils.Tools import getConfig, getanti, getHacker

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class antirole(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.headers = {"Authorization": f"Bot MTE0NzE4NTY2NDAwMjEwMTI0OA.GOcrWX.jxET9HPK-8i1TjPNAUgMYcCO68i0nuJ-gwptcA"}
        self.lock = asyncio.Lock()
        self.role_queue = asyncio.Queue()
        self.retry_queue = asyncio.Queue()
        self.session = None
        self.rate_limit_buckets = {}
        self.process_task = self.client.loop.create_task(self.process_roles())
        self.retry_task = self.client.loop.create_task(self.retry_failed_tasks())

    async def start_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(headers=self.headers, timeout=timeout)

    async def close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def rate_limit_handler(self, method, url, retries=5, **kwargs):
        bucket_key = self.get_bucket_key(url)
        backoff = 1
        while retries > 0:
            async with self.lock:
                await self.start_session()
                if bucket_key in self.rate_limit_buckets:
                    retry_after = self.rate_limit_buckets[bucket_key] - time.time()
                    if retry_after > 0:
                        logging.warning(f"Rate limit bucket hit for {bucket_key}. Retrying in {retry_after:.2f} seconds...")
                        await asyncio.sleep(retry_after)
                async with self.session.request(method, url, **kwargs) as response:
                    if response.status in {200, 201, 204}:
                        if response.status == 429:  # Update bucket info on rate limit
                            self.update_rate_limit_bucket(bucket_key, response)
                        return response
                    elif response.status == 429:  # Rate limit hit
                        self.update_rate_limit_bucket(bucket_key, response)
                        retry_after = int(response.headers.get("Retry-After", 5))
                        logging.warning(f"Rate limit hit. Retrying in {retry_after} seconds...")
                        await asyncio.sleep(retry_after + backoff)
                        retries -= 1
                        backoff *= 2
                    else:
                        logging.error(f"Failed to {method} {url}: {response.status} {response.reason}")
                        response.raise_for_status()
        logging.error(f"Failed to {method} {url} after retries")
        return None

    def get_bucket_key(self, url):
        # Generate a bucket key based on the URL to handle rate limits per endpoint
        return url.split("/")[4]

    def update_rate_limit_bucket(self, bucket_key, response):
        retry_after = int(response.headers.get("Retry-After", 5))
        self.rate_limit_buckets[bucket_key] = time.time() + retry_after

    async def delete_role(self, role):
        try:
            await role.delete()
            logging.info(f"Deleted role {role.id}")
        except discord.Forbidden:
            logging.error(f"Permission denied to delete role {role.id}")
        except Exception as e:
            logging.error(f"Failed to delete role {role.id}: {e}")

    async def create_role(self, guild, **kwargs):
        try:
            await guild.create_role(**kwargs)
            logging.info(f"Created role with kwargs: {kwargs}")
        except discord.Forbidden:
            logging.error(f"Permission denied to create role with kwargs: {kwargs}")
        except Exception as e:
            logging.error(f"Failed to create role with kwargs: {e}")

    async def edit_role(self, role, **kwargs):
        try:
            await role.edit(**kwargs)
            logging.info(f"Edited role {role.id}")
        except discord.Forbidden:
            logging.error(f"Permission denied to edit role {role.id}")
        except Exception as e:
            logging.error(f"Failed to edit role {role.id}: {e}")

    async def handle_punishment(self, guild, user_id, punishment, reason):
        api_version = 9  # Set a consistent API version
        try:
            if punishment == "ban":
                await self.rate_limit_handler(
                    'PUT', f"https://discord.com/api/v{api_version}/guilds/{guild.id}/bans/{user_id}",
                    json={"reason": reason}
                )
                logging.info(f"Successfully banned {user_id}")
            elif punishment == "kick":
                await self.rate_limit_handler(
                    'DELETE', f"https://discord.com/api/v{api_version}/guilds/{guild.id}/members/{user_id}",
                    json={"reason": reason}
                )
                logging.info(f"Successfully kicked {user_id}")
            elif punishment == "none":
                member = guild.get_member(user_id)
                if member:
                    await member.edit(roles=[role for role in member.roles if not role.permissions.administrator], reason=reason)
                logging.info(f"Successfully removed admin roles from {user_id}")
        except discord.Forbidden:
            logging.error(f"Insufficient permissions to punish user {user_id}")
        except Exception as e:
            logging.error(f"Failed to handle punishment for user {user_id}: {e}")

    async def process_roles(self):
        while True:
            roles = []
            while len(roles) < 50:  # Batch size of 50
                try:
                    role, action, kwargs = await asyncio.wait_for(self.role_queue.get(), timeout=1.0)
                    roles.append((role, action, kwargs))
                except asyncio.TimeoutError:
                    break
            if roles:
                await self.handle_roles_batch(roles)

    async def handle_roles_batch(self, roles):
        tasks = []
        for role, action, kwargs in roles:
            if action == 'delete':
                tasks.append(self.delete_role(role))
            elif action == 'create':
                tasks.append(self.create_role(role.guild, **kwargs))
            elif action == 'edit':
                tasks.append(self.edit_role(role, **kwargs))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                await self.retry_queue.put(roles[idx])

    async def retry_failed_tasks(self):
        while True:
            role, action, kwargs = await self.retry_queue.get()
            try:
                if action == 'delete':
                    await self.delete_role(role)
                elif action == 'create':
                    await self.create_role(role.guild, **kwargs)
                elif action == 'edit':
                    await self.edit_role(role, **kwargs)
                logging.info(f"Retried and processed role {role.id} for action {action}")
            except Exception as e:
                logging.error(f"Failed again to process role {role.id}: {e}")
            finally:
                self.retry_queue.task_done()

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("antirole cog is ready.")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        await self.handle_role_event(role, 'create')

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await self.handle_role_event(role, 'delete')

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        await self.handle_role_event(before, 'update', after)

    async def handle_role_event(self, role, event_type, updated_role=None):
        try:
            start = time.perf_counter()
            data = getConfig(role.guild.id)
            anti = getanti(role.guild.id)
            event = getHacker(role.guild.id)
            antievent = event["antinuke"][f"antirole-{event_type}"]
            punishment = data["punishment"]
            wled = data["whitelisted"]
            guild = role.guild
            reason = f"Role {event_type.capitalize()}d | Not Whitelisted"

            async for entry in guild.audit_logs(limit=5):
                user_id = entry.user.id
                if entry.action == getattr(discord.AuditLogAction, f"role_{event_type}"):
                    break

            if entry.user.id == self.client.user.id or entry.user.id == guild.owner_id or str(entry.user.id) in wled or anti == "off" or not antievent:
                return

            await self.handle_punishment(guild, user_id, punishment, reason)

            actions = []
            if event_type == 'create':
                actions.append((role, 'delete', {}))
            elif event_type == 'delete':
                actions.append((role, 'create', {
                    'name': role.name, 'permissions': role.permissions, 'hoist': role.hoist, 'mentionable': role.mentionable, 'colour': role.colour, 'reason': reason
                }))
            elif event_type == 'update' and updated_role:
                actions.append((updated_role, 'edit', {
                    'name': role.name, 'permissions': role.permissions, 'colour': role.colour, 'hoist': role.hoist, 'mentionable': role.mentionable, 'reason': reason
                }))

            for action in actions:
                await self.role_queue.put(action)

            logging.info(f"{event_type.capitalize()}d role event handled for role {role.id} by user {user_id}")
            logging.info(f"Time taken: {time.perf_counter() - start:.2f} seconds")

        except Exception as e:
            logging.error(f"Failed to handle role {event_type}: {e}")

    def cog_unload(self):
        self.client.loop.create_task(self.close_session())
        self.process_task.cancel()
        self.retry_task.cancel()

async def setup(client):
    await client.add_cog(antirole(client))
