############MODULES#############
import discord
import requests
import aiohttp
import datetime
import random
from discord.ext import commands
from random import randint
from utils.Tools import *
from core import Cog, Astroz, Context
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import random
from PIL import Image, ImageDraw, ImageOps

#14
#snipe | editsnipe | tickle | kiss | hug | slap | pat | feed | pet | howgay | slots | penis | meme | cat |ship

from pathlib import Path
import json

PICKUP_LINES = json.loads(Path("db/pikup.json").read_text("utf8"))


def RandomColor():
    randcolor = discord.Color(random.randint(0x000000, 0xFFFFFF))
    return randcolor


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def add_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.add_roles(role, reason="Nexus | Role Added ")

    async def remove_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.remove_roles(role, reason="Nexus | Role Removed")

    @blacklist_check()
    @ignore_check()
    @commands.hybrid_command(name="cuddle",
                  help=
                    "Cuddle mentioned user.",
                  usage="Cuddle <member>")
    async def cuddle(self, ctx, user: discord.Member = None):
        if user is None:
          await ctx.send("You need to mention a user to cuddle.")
        elif user == ctx.author:
          await ctx.send("You can't cuddle yourself.")
        elif user.bot:
          await ctx.send("You can't cuddle bots.")
        else:
           r = requests.get("https://nekos.life/api/v2/img/cuddle")
        res = r.json()
        embed = discord.Embed(
            timestamp=datetime.datetime.utcnow(),
            description=f"{ctx.author.mention} cuddle {user.mention}",
            color=0x2f3136)
        embed.set_image(url=res['url'])
        embed.set_footer(text=f"{ctx.guild.name}")
        await ctx.send(embed=embed)

    @blacklist_check()
    @ignore_check()
    @commands.hybrid_command(name="kiss",
                  help=
                    "Kiss mentioned user.",
                  usage="Kiss <member>")
    async def kiss(self, ctx, user: discord.Member = None):
        if user is None:
          await ctx.send("You need to mention a user to kiss.")
        elif user == ctx.author:
          await ctx.send("You can't kiss yourself.")
        elif user.bot:
          await ctx.send("You can't kiss bots.")
        else:
           r = requests.get("https://nekos.life/api/v2/img/kiss")
        res = r.json()
        embed = discord.Embed(
            timestamp=datetime.datetime.utcnow(),
            description=f"{ctx.author.mention} kisses {user.mention}",
            color=0x2f3136)
        embed.set_image(url=res['url'])
        embed.set_footer(text=f"{ctx.guild.name}")
        await ctx.send(embed=embed)
  
    @blacklist_check()
    @ignore_check()
    @commands.command(name="hug",
                  help="Hug mentioned user.",
                  usage="Hug <member>")
    async def hug(self, ctx, user: discord.Member = None):
        if user is None:
          await ctx.send("You need to mention a user to hug.")
        elif user == ctx.author:
          await ctx.send("You can't hug yourself.")
        elif user.bot:
          await ctx.send("You can't hug bots.")
        else:
           r = requests.get("https://nekos.life/api/v2/img/hug")
        res = r.json()
        embed = discord.Embed(
            timestamp=datetime.datetime.utcnow(),
            description=f"{ctx.author.mention} hugged {user.mention}",
            color=0x2f3136)
        embed.set_image(url=res['url'])
        embed.set_footer(text=f"{ctx.guild.name}")
        await ctx.send(embed=embed)
    

    @commands.command(name="slap",
                      help="Slap mentioned user .",
                      usage="Slap <member>")
    @blacklist_check()
    @ignore_check()
    async def slap(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/slap")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                color=0x2f3136,
                description=f"{ctx.author.mention} slapped {user.mention}",
            )
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.command(name="pat",
                      help="Pat mentioned user .",
                      usage="Pat <member>")
    @blacklist_check()
    @ignore_check()
    async def pat(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://some-random-api.ml/animu/pat")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} pats {user.mention}",
                color=0x2f3136)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.command(name="feed",
                      help="Feed mentioned user .",
                      usage="Feed <member>")
    @blacklist_check()
    @ignore_check()
    async def feed(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/feed")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} feeds {user.mention}",
                color=0x2f3136)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.command(name="pet", usage="Pet <member>")
    @blacklist_check()
    @ignore_check()
    async def pet(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/pat")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} pets {user.mention}",
                color=0x2f3136)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)


    @commands.command(name="howgay",
                      aliases=['gay'],
                      help="check someone gay percentage",
                      usage="Howgay <person>")
    @blacklist_check()
    @ignore_check()
    async def howgay(self, ctx, *, person):
        embed = discord.Embed(color=0x2f3136)
        responses = [
            '50', '75', '25', '1', '3', '5', '10', '65', '60', '85', '30',
            '40', '45', '80', '100', '150', '1000'
        ]
        embed.description = f'**{person} is {random.choice(responses)}% Gay** :rainbow:'
        embed.set_footer(text=f'How gay are you? - {ctx.author.name}')
        await ctx.send(embed=embed)
    
    @commands.command(name="slots")
    @blacklist_check()
    @ignore_check()
    async def slots(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)
        slotmachine = f"[ {a} {b} {c} ]\n{ctx.author.mention}"
        if (a == b == c):
            await ctx.send(embed=discord.Embed(
                title="Slot machine",
                description=f"{slotmachine} All Matching! You Won!",
                color=0x2f3136))
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(embed=discord.Embed(
                title="Slot machine",
                description=f"{slotmachine} 2 Matching! You Won!",
                color=0x2f3136))
        else:
            await ctx.send(embed=discord.Embed(
                title="Slot machine",
                description=f"{slotmachine} No Matches! You Lost!",
                color=0x2f3136))

    @commands.command(name="penis",
                      aliases=['dick'],
                      help="Check someone`s dick`s size .",
                      usage="Dick [member]")
    @blacklist_check()
    @ignore_check()
    async def penis(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        size = random.randint(1, 15)
        dong = ""
        for _i in range(0, size):
            dong += "="
        em = discord.Embed(title=f"**{user}'s** Dick size",
                           description=f"8{dong}D",
                           color=0x2f3136)
        em.set_footer(text=f'whats {user} dick size?')
        await ctx.send(embed=em)

    @commands.command(name="meme", help="give you a meme", usage="meme")
    @blacklist_check()
    @ignore_check()
    async def meme(self, ctx):
        embed = discord.Embed(title="""Take some memes""", color=0x2f3136)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    'https://www.reddit.com/r/dankmemes/new.json?sort=hot'
            ) as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(
                    0, 25)]['data']['url'])
                embed.set_footer(text=f'Random Meme:')
                #embed.set_footer(text=f'Random Meme:')
                await ctx.send(embed=embed)


    @commands.hybrid_command(name="iplookup",
                             aliases=['ip', 'ipl'],
                             help="shows info about an ip",
                             usage="Iplookup [ip]")
    @blacklist_check()
    @ignore_check()
    async def iplookup(self, ctx, *, ip):
        async with aiohttp.ClientSession() as a:
            async with a.get(f"http://ipwhois.app/json/{ip}") as b:
                c = await b.json()
                try:
                    coordj = ''.join(f"{c['latitude']}" + ", " +
                                     f"{c['longitude']}")
                    embed = discord.Embed(
                        title="IP: {}".format(ip),
                        description=
                        f"```txt\n\nLocation Info:\nIP: {ip}\nIP Type: {c['type']}\nCountry, Country code: {c['country']} ({c['country_code']})\nPhone Number Prefix: {c['country_phone']}\nRegion: {c['region']}\nCity: {c['city']}\nCapital: {c['country_capital']}\nLatitude: {c['latitude']}\nLongitude: {c['longitude']}\nLat/Long: {coordj} \n\nTimezone Info:\nTimezone: {c['timezone']}\nTimezone Name: {c['timezone_name']}\nTimezone (GMT): {c['timezone_gmt']}\nTimezone (GMT) offset: {c['timezone_gmtOffset']}\n\nContractor/Hosting Info:\nASN: {c['asn']}\nISP: {c['isp']}\nORG: {c['org']}\n\nCurrency:\nCurrency type: {c['currency']}\nCurrency Code: {c['currency_code']}\nCurrency Symbol: {c['currency_symbol']}\nCurrency rates: {c['currency_rates']}\nCurrency type (plural): {c['currency_plural']}```",
                        color=0x2f3136)
                    embed.set_footer(
                        text='Thanks For Using Nexus',
                        icon_url=
                        "https://cdn.discordapp.com/avatars/1096394407823028276/706ed7412d2f615b61c084ae5c6524e1.webp?size=2048"
                    )
                    await ctx.send(embed=embed)
                except KeyError:
                    embed = discord.Embed(
                        description=
                        "KeyError has occured, perhaps this is a bogon IP address, or invalid IP address?",
                        color=0x2f3136)
                    await ctx.send(embed=embed)


############################

    @commands.command(name="owner",
                      description="Gives the owner role to the user .",
                      aliases=['own'],
                      help="Gives the owner role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _owner(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['owner'] 
            req = context.guild.get_role(lol)
            owner =context.guild.get_role(own)
            if data["owner"] == None:
                hacker1 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Owner role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                await context.send(embed=hacker1)
            if data["reqrole"] == None:
                hacker4 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                await context.send(embed=hacker4)
            else:
                if context.author == context.guild.owner or req in context.author.roles:
                    await self.add_role(role=own, member=member)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    await context.send(embed=hacker3)




    @commands.command(name="coowner",
                      description="Gives the owner role to the user .",
                      aliases=['coown'],
                      help="Gives the owner role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _coowner(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['coown']  
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["coown"] != None:
                        await self.add_role(role=own, member=member)
                        hacker = discord.Embed(
                description=
                f"<:hacker_tick:1271209580793167925> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                        hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                        hacker.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker)
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Co Owner role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    hacker3.set_thumbnail(url=f"{context.author.avatar}")
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                hacker4.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker4)


    @commands.command(name="headadmin",
                      description="Gives the head admin role to the user .",
                      aliases=['hadmin'],
                      help="Gives the head admin role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _headadmin(self, context: Context,
                         member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['headadmin']  
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["headadmin"] != None:
                        await self.add_role(role=own, member=member)
                        hacker = discord.Embed(
                description=
                f"<:hacker_tick:1271209580793167925> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                        hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                        hacker.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker)
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Head Admins role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    hacker3.set_thumbnail(url=f"{context.author.avatar}")
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                hacker4.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker4)    

    @commands.command(name="admins",
                      description="Gives the admins role to the user .",
                      help="Gives the admins role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _admins(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['admin']  
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["admin"] != None:
                        await self.add_role(role=own, member=member)
                        hacker = discord.Embed(
                description=
                f"<:hacker_tick:1271209580793167925> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                        hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                        hacker.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker)
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Admins role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    hacker3.set_thumbnail(url=f"{context.author.avatar}")
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                hacker4.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker4)  

    @commands.command(name="girladmin",
                      description="Gives the admin role to the user .",
                      aliases=['gadmin'],
                      help="Gives the admin role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _girladmin(self, context: Context,
                         member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['gadmin']  
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["gadmin"] != None:
                        await self.add_role(role=own, member=member)
                        hacker = discord.Embed(
                description=
                f"<:hacker_tick:1271209580793167925> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                        hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                        hacker.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker)
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Girl Admins role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    hacker3.set_thumbnail(url=f"{context.author.avatar}")
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                hacker4.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker4)  


    @commands.command(name="headmod",
                      description="Gives the head mod role to the user .",
                      aliases=['hmod'],
                      help="Gives the head mod role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _headmod(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['headmod']  
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["headmod"] != None:
                        await self.add_role(role=own, member=member)
                        hacker = discord.Embed(
                description=
                f"<:hacker_tick:1271209580793167925> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                        hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                        hacker.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker)
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Head Mod role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    hacker3.set_thumbnail(url=f"{context.author.avatar}")
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                hacker4.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker4) 
    
    @commands.command(name="mod",
                      description="Gives the mod role to the user .",
                      help="Gives the mod role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _mod(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['mod']  
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["mod"] != None:
                        await self.add_role(role=own, member=member)
                        hacker = discord.Embed(
                description=
                f"<:hacker_tick:1271209580793167925> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                        hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                        hacker.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker)
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Mod role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    hacker3.set_thumbnail(url=f"{context.author.avatar}")
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                hacker4.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker4) 

    @commands.command(name="girlmod",
                      description="Gives the girl mod role to the user .",
                      aliases=['gmod'],
                      help="Gives the girl mod role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _girlmod(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['gmod']  
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["gmod"] != None:
                        await self.add_role(role=own, member=member)
                        hacker = discord.Embed(
                description=
                f"<:hacker_tick:1271209580793167925> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                        hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                        hacker.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker)
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Girl Mod role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    hacker3.set_thumbnail(url=f"{context.author.avatar}")
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:hacker_admin_cross:1271209737647558819> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                hacker4.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker4)    



    @commands.command()
    async def pickupline(self, ctx: Context) -> None:
        """
        Gives you a random pickup line.
        Note that most of them are very cheesy.
        """
        random_line = random.choice(PICKUP_LINES["lines"])
        embed = discord.Embed(
            title=":cheese: Your pickup line :cheese:",
            description=random_line["line"],
            color=ctx.author.color,
        )
        embed.set_thumbnail(
            url=random_line.get("image", PICKUP_LINES["placeholder"]))
        await ctx.send(embed=embed)