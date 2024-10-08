import os
from core.Astroz import Astroz
import asyncio, json
import jishaku, cogs
from discord.ext import commands, tasks
import discord
from discord import app_commands
import traceback
from discord.ext.commands import Context
from discord import Spotify
import aiohttp
import base64
import time
from io import BytesIO
#import openai
from discord import Embed
from difflib import get_close_matches
from contextlib import suppress
from core import Context
from core.Cog import Cog
from utils.Tools import getConfig
from itertools import chain
from utils import *
import json
import datetime
import pytz

os.environ["JISHAKU_NO_DM_TRACEBACK"] = "False"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

bot = Astroz()
sniped = {}
client = Astroz()
tree = client.tree
#openai.api_key = ""
clr = 0x2F3136




@client.command()
#@commands.is_owner()
async def reload(ctx):
    await ctx.send("Reloading all modules...")
    # Unload all modules
    for extension in list(bot.extensions):
        bot.unload_extension(extension)

    # Load cogs and core modules again
    load_modules('cogs')
    load_modules('core')

    await ctx.send("Reload complete!")

@commands.cooldown(1, 2, commands.BucketType.user)
@commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
@commands.guild_only()
@client.command()
async def generate(ctx: commands.Context, *, prompt: str):
    ETA=int(time.time()+60)
    await ctx.send(f"**Go grab a coffee , this may take some time... ETA: <t:{ETA}:R>**")
    async with aiohttp.request("POST","https://backend.craiyon.com/generate",json={"prompt": prompt}) as resp:
        r = await resp.json()
        images = r['images']
        image =BytesIO(base64.decodebytes(images[0].encode("utf-8")))
        return await ctx.reply(content="CONTENT GENERATED BY **craiyon.com**",file=discord.File(image,"generatedimage.png"))


@client.command()
async def chatgpt(ctx, *, question):

    loading_message = await ctx.send("<a:pain_run:1149272995840401428> | Loading, Please Wait...")
    

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        max_tokens=3000,
        temperature=0.7
    )
    output = response["choices"][0]["text"]
    

    await asyncio.sleep(5)
    

    embed = Embed(description=f"```python{output}```", color=0x00FFED)
    embed.set_author(
        name=f"Nexus Chat Gpt`s Response:",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    )
    embed.set_footer(
        text=f"Requested By {ctx.author}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    )
    

    await loading_message.delete()
    await ctx.send(embed=embed)

@client.command()
async def createinvite(ctx, guildid: int):
  if ctx.author.id == 1078333867175465162 or 1078333867175465162:

    guild = client.get_guild(guildid)
    invitelink = ""
    i = 0
    while invitelink == "":
      channel = guild.text_channels[i]
      link = await channel.create_invite(max_age=300,max_uses=1)
      invitelink = str(link)
      i += 1
    await ctx.send(invitelink)
  else:

    await ctx.send("Iam not in this server")


@client.event
async def on_message_delete(message):

    if message.content or message.attachments:

        sniped[str(message.guild.id)] = sniped.get(str(message.guild.id), {})
        sniped[str(message.guild.id)][str(message.channel.id)] = {
            "author": message.author.id,
            "channel": message.channel.id,
            "content": message.content,
            "attachment_url": message.attachments[0].url if message.attachments else None,
            "timestamp": message.created_at.replace(tzinfo=pytz.UTC)
        }


@client.command()
async def snipe(ctx, channel: discord.TextChannel=None):
    if channel is None:
        channel = ctx.channel

    try:
        snipe_info = sniped[str(channel.guild.id)][str(channel.id)]
        if snipe_info["content"] == "" and not snipe_info["attachment_url"]:
            return await ctx.send(f"<:nexus_cross_none:1148906686162141256> | There is nothing to snipe in {channel.mention}")
    except KeyError:
        return await ctx.send(f"<:nexus_cross_none:1148906686162141256> | There is nothing to snipe in {channel.mention}")

    timestamp = snipe_info["timestamp"]
    time_diff = datetime.datetime.now(pytz.UTC) - timestamp
    hours, remainder = divmod(int(time_diff.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)

    embed = discord.Embed(
        title="", 
        description=f"🚮 Message sent by <@{snipe_info['author']}> deleted in <#{snipe_info['channel']}>\n__**Content**__:\n{snipe_info['content'] or '[***Content Unavailable***]'}",
        color=0x00FFED, 
        timestamp=ctx.message.created_at
    )

    attachment_url = snipe_info["attachment_url"]
    if attachment_url and attachment_url.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
        embed.set_image(url=attachment_url)

    embed.set_footer(text=f"Deleted {hours}h {minutes}m {seconds}s ago")
    await ctx.send(embed=embed)


import qrcode

@client.command()
async def qr(ctx, link):
    if link == "":
      await ctx.sent("You did not add a link.")
    else:
      embedd = discord.Embed(title="This is the generated qr code.")
      embedd.set_image(url=f"https://api.qrserver.com/v1/create-qr-code/?size=450x450&data={link}")
    await ctx.send(embed=embedd)

@client.command()
async def say(ctx, *, text):
    await ctx.send(text)


@client.command()
async def tools(ctx):
    embed = discord.Embed(title="Top 10 Ethical Hacking Tools", description="", color=discord.Color.blue())
    
    embed.add_field(name="**Nmap**", value="""```yaml
A powerful port scanner and network exploration tool
```[Download Link](https://nmap.org/download.html)""", inline=False)
    embed.add_field(name="**Metasploit**", value="""```yaml
An advanced framework for exploit development and testing.
```[Download Link](https://www.metasploit.com/)""", inline=False)
    embed.add_field(name="**Wireshark**", value="""```yaml
A popular network protocol analyzer.
```[Download Link](https://www.wireshark.org/download.html)""", inline=False)
    embed.add_field(name="**John the Ripper**", value="""```yaml
A password cracking tool.
```[Download Link](https://www.openwall.com/john/)""", inline=False)
    embed.add_field(name="**Aircrack-ng**", value="""```yaml
A popular wireless network cracking tool.
```[Download Link](https://www.aircrack-ng.org/)""", inline=False)
    embed.add_field(name="**Burp Suite**", value="""```yaml
A web application security testing tool
```[Download Link](https://portswigger.net/burp)""", inline=False)
    embed.add_field(name="**SQLMap**", value="""```yaml
An automatic SQL injection and database takeover tool.
```[Download Link](https://sqlmap.org/)""", inline=False)
    embed.add_field(name="**Hydra**", value="""```yaml
A popular brute-force attack tool.
```[Download Link](https://github.com/vanhauser-thc/thc-hydra)""", inline=False)
    embed.add_field(name="**Dirbuster**", value="""```yaml
A web application directory bruteforcer.
```[Download Link](https://sourceforge.net/projects/dirbuster/)""", inline=False)
    embed.add_field(name="**Nikto**", value="""```yaml
A web server vulnerability scanner.
```[Download Link](https://cirt.net/Nikto2)""", inline=False)
    
    await ctx.send(embed=embed)

import wikipedia

@client.command()
async def wiki(ctx, *, query):
    try:
        results = wikipedia.search(query)
        if not results:
            raise wikipedia.exceptions.PageError(query)


        page = wikipedia.page(results[0])
        summary = page.summary


        embed = discord.Embed(title=page.title, description=summary, color=discord.Color.blue())
        embed.set_footer(text="Provided by Wikipedia")

        await ctx.send(embed=embed)

    except wikipedia.exceptions.PageError:
        await ctx.send(f"Sorry, there are no Wikipedia results found for '{query}'.")

import random
import string

@client.command()
async def passgen(ctx):
    password_length = 12


    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for _ in range(password_length))


    await ctx.author.send(f"**Your Generated Password is:** ```{password}```")


    await ctx.send(f"**{ctx.author.mention},Check your DM for the generated password!**")

#bal hoy na

class Hacker(discord.ui.Modal, title='Embed Configuration'):
    tit = discord.ui.TextInput(
        label='Embed Title',
        placeholder='Embed title here',
    )

    description = discord.ui.TextInput(
        label='Embed Description',
        style=discord.TextStyle.long,
        placeholder='Embed description optional',
        required=False,
        max_length=400,
    )

    thumbnail = discord.ui.TextInput(
        label='Embed Thumbnail',
        placeholder='Embed thumbnail here optional',
        required=False,
    )

    img = discord.ui.TextInput(
        label='Embed Image',
        placeholder='Embed image here optional',
        required=False,
    )

    footer = discord.ui.TextInput(
        label='Embed footer',
        placeholder='Embed footer here optional',
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.tit.value,
                              description=self.description.value,
                              color=0x00FFE4)
        if not self.thumbnail.value is None:
            embed.set_thumbnail(url=self.thumbnail.value)
        if not self.img.value is None:
            embed.set_image(url=self.img.value)
        if not self.footer.value is None:
            embed.set_footer(text=self.footer.value)
        await interaction.response.send_message(embed=embed)

    async def on_error(self, interaction: discord.Interaction,
                       error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.',
                                                ephemeral=True)

        traceback.print_tb(error.__traceback__)


@tree.command(name="embed", description="Create A Embed Using Nexus")
async def _embed(interaction: discord.Interaction) -> None:
    await interaction.response.send_modal(Hacker())


########################################


@client.event
async def on_presence_update(before, after):
    with open("db/vanityroles.json", "r") as f:
        jnl = json.load(f)
    if str(before.guild.id) not in jnl:
        return
    elif str(before.guild.id) in jnl:
        vanity = jnl[str(before.guild.id)]["vanity"]
        role = jnl[str(before.guild.id)]["role"]
        channel = jnl[str(before.guild.id)]["channel"]
        if str(before.raw_status) == "offline":
            return
        else:
            if len(after.activities) != 0:
                aft = after.activities[0].name
            else:
                aft = ""
            if len(before.activities) != 0:
                bef = before.activities[0].name
            else:
                bef = ""
            if aft == bef:
                return None
            elif vanity in aft and vanity in bef:
                return None
            if vanity in aft:
                try:
                    if vanity not in bef:
                        gchannel = client.get_channel(channel)
                        grole = after.guild.get_role(role)
                        if after.avatar is None:
                            pass
                        else:
                            await after.add_roles(
                                grole,
                                reason=f"Nexus | Added {vanity} In Status")
                            hacker5 = discord.Embed(
                                description=
                                f"{after.name}, *Thanks For Repping [{after.guild.name}](https://discord.gg{vanity}) Vanity {vanity} In Your Status <3 .*",
                                color=0x2f3136)
                            hacker5.set_author(
                                name=f"{after.name}",
                                icon_url=after.avatar.url
                                if after.avatar else after.default_avatar.url)
                            hacker5.timestamp = discord.utils.utcnow()
                            if after.guild.icon is not None:
                                hacker5.set_footer(
                                    text=after.guild.name,
                                    icon_url=after.guild.icon.url)
                            await gchannel.send(embed=hacker5,
                                                mention_author=False)
                    elif vanity in bef:
                        return None
                except:
                    pass
            elif vanity not in aft:
                if vanity in bef:
                    try:
                        gchannel = client.get_channel(channel)
                        grole = after.guild.get_role(role)
                        if after.avatar is None:
                            pass
                        else:
                            hacker = discord.Embed(
                                description=
                                f"{after.name}, *Removed [{after.guild.name}](https://discord.gg{vanity}) Vanity {vanity} From Her/His Status .*",
                                color=0x2f3136)
                            hacker.set_author(
                                name=f"{after.name}",
                                icon_url=after.avatar.url
                                if after.avatar else after.default_avatar.url)
                            hacker.timestamp = discord.utils.utcnow()
                            if after.guild.icon is not None:
                                hacker.set_footer(
                                    text=after.guild.name,
                                    icon_url=after.guild.icon.url)
                            await after.remove_roles(
                                grole,
                                reason=f"Nexus | Removed {vanity} From Status"
                            )
                            await gchannel.send(embed=hacker,
                                                mention_author=False)
                    except:
                        pass


@client.event
async def on_ready():
    print("Loaded & Online!")
    print(f"Logged in as: {client.user}")
    print(f"Nexus Connected to: {len(client.guilds)} guilds")
    print(f"Nexus Connected to: {len(client.users)} users")
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(e)

web= "https://discord.com/api/webhooks/1270788267536810035/yu1R6LJHhJiMz-mLzEY4i_l80yqHmy1TbuSylzicUoqG3XItgtXGBoQjw4Jb7OEV39yA"
@client.event
async def on_command_completion(context: Context) -> None:

    full_command_name = context.command.qualified_name
    split = full_command_name.split("\n")
    executed_command = str(split[0])
    hacker = discord.SyncWebhook.from_url(web)
   # hacker = client.get_channel(1157962854952091818)
    if not context.message.content.startswith("$"):
        pcmd = f"`${context.message.content}`"
    else:
        pcmd = f"`{context.message.content}`"
    if context.guild is not None:
        try:

            embed = discord.Embed(color=0x2f3136)
            embed.set_author(
                name=
                f"Executed {executed_command} Command By : {context.author}",
                icon_url=f"{context.author.avatar}")
            embed.set_thumbnail(url=f"{context.author.avatar}")
            embed.add_field(
                name="Command Name :",
                value=f"{executed_command}",
                inline=False)
            embed.add_field(
                name="Command Content :",
                value="{}".format(pcmd),
                inline=False)
            embed.add_field(
                name="Command Executed By :",
                value=
                f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name="Command Executed In :",
                value=
                f"{context.guild.name}  | ID: [{context.guild.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name=
                "Command Executed In Channel :",
                value=
                f"{context.channel.name}  | ID: [{context.channel.id}](https://discord.com/channel/{context.channel.id})",
                inline=False)
            embed.set_footer(text=f"Thank you for choosing  {client.user.name}",
                             icon_url=client.user.display_avatar.url)
            hacker.send(embed=embed)
        except:
            print('hehe')
    else:
        try:

            embed1 = discord.Embed(color=0x2f3136)
            embed1.set_author(
                name=
                f"Executed {executed_command} Command By : {context.author}",
                icon_url=f"{context.author.avatar}")
            embed1.set_thumbnail(url=f"{context.author.avatar}")
            embed1.add_field(
                name="Command Name :",
                value=f"{executed_command}",
                inline=False)
            embed1.add_field(
                name="Command Executed By :",
                value=
                f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed1.set_footer(text=f"Thank you for choosing  {client.user.name}",
                              icon_url=client.user.display_avatar.url)
            hacker.send(embed=embed1)
        except:
            print("xD")
            await client.loop.create_task(VisionX_stats())
async def VisionX_stats():
  while True:
    servers = len(client.guilds)
    users = sum(g.member_count for g in client.guilds
                if g.member_count != None)
    sv_ch = client.get_channel(1177231523984973865)
    users_ch = client.get_channel(1177231541764636883)
    await asyncio.sleep(600)
    await sv_ch.edit(name="『Servers : {} 』".format(servers))
    await users_ch.edit(name="『Users : {} 』".format(users))


from flask import Flask
from threading import Thread

app = Flask(__name__) 
@app.route('/')
def home():
    return "Nexus is online"
def run():
  app.run(host='0.0.0.0',port=8080)
def keep_alive():  
  server=Thread(target=run)
  server.start()
keep_alive()




@client.command(aliases=['wh'])
@commands.has_permissions(administrator=True)
async def create_hook(ctx, name=None):
  if not name:
    await ctx.send("Please specify a name for the webhook.")
    return
  webhook = await ctx.channel.create_webhook(name=name)
  embed = discord.Embed(
    title=
    f"**<:nexus_tick_none:1148905989127557120> | Webhook __{webhook.name}__ created successfully **",
    color=discord.Color.blue())
  try:
    await ctx.author.send(f"||{webhook.url}||")
    await ctx.author.send(embed=embed)
    await ctx.send(
      f"**<:nexus_tick_none:1148905989127557120> | Webhook :- __{webhook.name}__ created successfully.**\n** Check your DMs for the URL.\n {ctx.author.mention} **"
    )
  except discord.Forbidden:
    await ctx.send(
      f"**<:nexus_cross_none:1148906686162141256> | Webhook:- __{webhook.name}__ ||{webhook.url}|| (Unable to DM user) ** \n {ctx.author.mention}"
    )


@client.command()
@commands.has_permissions(administrator=True)
async def delete_hook(ctx, webhook_id):
  try:
    webhook = await discord.Webhook.from_url(
      webhook_id, adapter=discord.RequestsWebhookAdapter())
    await webhook.delete()
    await ctx.send("Webhook deleted successfully.")
  except discord.NotFound:
    await ctx.send("Webhook not found.")


@client.command(aliases=['all_hooks'])
async def list_hooks(ctx):
  webhooks = await ctx.channel.webhooks()
  if not webhooks:
    await ctx.send("No webhooks found in this channel.")
    return
  embed = discord.Embed(title="List of Webhooks", color=discord.Color.blue())
  for webhook in webhooks:
    embed.add_field(
      name="__Name__",
      value=f"**<:nexus_tick_none:1148905989127557120> | {webhook.name} **")
    embed.add_field(name="__ID__", value=webhook.id)
    embed.add_field(name="\u200b", value="\u200b")
  await ctx.send(
    f"{ctx.author.mention}, Here are the webhooks in this channel",
    embed=embed)



@client.command()
async def makeembed(ctx, *, description):
    if not description:
        await ctx.channel.send(
            "One or more values are missing. Command should look like 'makeEmbed (description)'"
        )

    embed = discord.Embed(description=description, color=0x2f3136)
    if ctx.guild.icon is not None:
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)

    await ctx.send(embed=embed)


@client.command()
async def spotify(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
        pass
    if user.activities:
        for activity in user.activities:
            if isinstance(activity, Spotify):
                nexuss = discord.Embed(title=f"{user.name}'s Spotify",
                                     description="Listening to {}".format(
                                         activity.title),
                                     color=0x2f3136)
                nexuss.set_thumbnail(url=activity.album_cover_url)
                nexuss.add_field(name="Artist", value=activity.artist)
                nexuss.add_field(name="Album", value=activity.album)
                nexuss.set_footer(text="Song started at {}".format(
                    activity.created_at.strftime("%H:%M")))
                await ctx.send(embed=nexuss)





            
async def main():
    async with client:
        os.system("clear")
        await client.load_extension("cogs")
        await client.load_extension("jishaku")
        await client.start("")

if __name__ == "__main__":
    asyncio.run(main())
