import discord
from discord.ext import commands
from difflib import get_close_matches
from contextlib import suppress
from core import Context
from core.Astroz import Astroz
from core.Cog import Cog
from utils.Tools import getConfig
from itertools import chain
from utils import *
import json
from utils import help as vhelp
from discord.ext import commands
from discord.ui import Select, View
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator

class HelpCommand(commands.HelpCommand):
    # ... (other methods)

    async def send_bot_help(self, mapping):
        await self.context.typing()

        # Load necessary data for blacklist and ignore checks
        with open('db/ignore.json', 'r') as heck:
            randi = json.load(heck)
        with open('db/blacklist.json', 'r') as f:
            bled = json.load(f)

        if str(self.context.author.id) in bled["ids"]:
            embed = discord.Embed(
                title="<:ayden_cross:1136704636259160194> Blacklisted", 
                description="You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/dwarika)", 
                color=0x2f3136
            )
            return await self.context.reply(embed=embed, mention_author=False)
        elif str(self.context.channel.id) in randi["ids"]:
            return None

        categories = {
            "Activity Role": ['activityrole' , 'activityrole setup' , 'activityrole reset' , 'activityrole status'],
            "Antinuke": ['antinuke' , 'antinuke enable' , 'antinuke disable' , 'antinuke antirole-create' , 'antinuke antirole-delete' , 'antinuke antirole-update' , 'antinuke antichannel-create' , 'antinuke antichannel-delete' , 'antinuke antichannel-update' , 'antinuke antiban' , 'antinuke antikick' , 'antinuke antiwebhook' , 'antinuke antibot' , 'antinuke antiserver' , 'antinuke antiping' , 'antinuke antiprune' , 'antiemoji-delete' , 'antinuke antiemoji-create' , 'antinuke antiemoji-update' , 'antinuke show' , 'antinuke punishment set' , 'antinuke whitelist add' , 'antinuke whitelist remove' , 'antinuke whitelist show' , 'antinuke whitelist reset' , 'antinuke channelclean' , 'antinuke roleclean' , 'antinuke wl role' , 'antinuke owner add' , 'antinuke owner remove' , 'antinuke owner show' , 'antinuke owner reset'],
            "Antialt": ['Antialt'],
            "Autorole": ['Autorolesetup'],
            "Boost": ['boostrole add' , 'boostrole remove' , 'boostrole config' , 'boostrole reset' , 'boost channel add' , 'boost channel remove' , 'boost channel' , 'boost embed' , 'boost image' , 'boost message' , 'boost ping' , 'boost test' , 'boost thumbnail' , 'boost autodel' , 'boost'],
            "Extra": ['stats' , 'invite' , 'vote' , 'serverinfo' , 'userinfo' , 'roleinfo' , 'botinfo' , 'status' , 'firstmessage' , 'passgen' , 'say' , 'boostlevel' , 'emoji' , 'user' , 'badges' , 'role' , 'channel' , 'boosts' , 'unbanall' ,  'joined-at' , 'ping' , 'uptime' , 'github' , 'vcinfo' , 'channelinfo' , 'note' , 'notes' , 'trashnotes' , 'badges' , 'reminder start' , 'reminder delete' , 'reminder list' , 'list boosters' , 'list inrole' , 'list emojis' , 'list bots' , 'list admins' , 'list invoice' , 'list mods' , 'list early' , 'list activedeveloper' , 'list createpos' , 'list roles' , 'ignore' , 'ignore channel' , 'ignore channel add' , 'ignore channel remove' , 'ignore user add' , 'ignore user remove' , 'ignore user show' , 'banner user' , 'banner server' , 'logall enable' , 'logall disable' , 'pic', 'boys' , 'girls', 'couples', 'anime' , 'media', 'media setup', 'media remove', 'media config', 'media reset'],
            "Fun": ['tickle' , 'kiss' , 'hug' , 'slap' , 'pat' , 'feed' , 'pet' , 'howgay' , 'slots' , ' penis' , 'meme' , 'cat' , 'iplookup'],
            "Games": ['akinator' , 'chess' , 'hangman' , 'typerace' , 'rps' , 'reaction' , 'tick-tack-toe' , 'wordle' , '2048' , 'memory-game' , 'number-slider' , 'battleship' , 'country-guesser'],
            "General": ['chatgpt' , 'avatar' , 'servericon' , 'membercount' , 'poll' , 'hack' , 'token' , 'users' , 'italicize' , 'strike' , 'quote' , 'code' , 'bold' , 'censor' , 'underline' , 'gender' , 'wizz' , 'pikachu' , 'shorten' , 'urban' , 'rickroll' , 'hash' , 'snipe' , 'setup' , 'setup staff' , 'setup girl' , 'setup friend' , 'setup vip' , 'setup guest' , 'setup owner' , 'setup coowner' , 'setup headadmin' , 'setup admins' , 'setup girladmin' , 'setup headmod' , 'setup mod' , 'setup girlmod' , 'setup config' , 'staff' , 'girl' , 'friend' , 'vip' , 'guest' , 'owner' , 'coowner' , 'headadmin' , 'admin' , 'girladmin ' , 'headmod' , 'mod' , 'girlmod' , 'remove staff' , 'remove girl' , 'remove friend' , 'remove vip' , 'remove guest' , 'remove owner' , 'remove coowner' , 'remove headadmin' , 'remove admin' , 'remove girladmin' , 'remove headmod' , 'remove mod' , 'remove girlmod' , 'ar' , 'ar create' , 'ar delete' , 'ar edit' , 'ar config'],
            "Giveaway": ['giveaway' , 'gstart' , 'gend' , 'greroll'],
            "Raidmode": ['automod' , 'antispam on' , 'antispam off' , 'antilink off' ,  'antilink on' , 'verification enable' , 'verification disable' , 'verification config'],
            "Moderation": ['setprefix' , 'mute' , 'unmute' , 'kick' , 'warn' , 'ban' , 'unban' , 'clone' , 'nick' , 'slowmode' , 'unslowmode' , 'clear' , 'clear all' , 'clear bots' , 'clear embeds' , 'clear files' , 'clear mentions' , 'clear images' , 'clear contains' , 'clear reactions' , 'clear user' , 'clear emoji' , 'nuke' , 'lock' , 'unlock' , 'hide' , 'unhide' , 'hideall' , 'unhideall' , 'audit' , 'role' , 'role temp' , 'role remove' , 'role delete' , 'role create' , 'role rename' , 'enlarge' , 'role human' , 'role bot' , 'role all' , 'removerole human' , 'removerole bot' , 'removerole all' , 'admin add' , 'admin remove' , 'admin show' , 'admin role' , 'admin reset' , 'roleicon', 'steal' , 'deleteemoji' , 'deletesticker' , 'addsticker'],
            "Starboard": ['starboard info' , 'starboard limit' , 'starboard lock' , 'starboard setup' , 'starboard unlock' , 'starboard'],
            "Music": ['connect' , 'play' , 'queue' , 'nowplaying' , 'stop', 'pause' , 'move' , 'shuffle' , 'resume' , 'skip' , 'clear' , 'disconnect' , 'seek' , 'pull' , 'volume' , 'bassboost enable' , 'bassboost disable' , 'filter' , 'filter daycore enable' , 'filter daycore disable' , 'filter speed enable' , 'filter speed disable' , 'filter slowmode enable' , 'filter slowmode disable' , 'filter lofi enable' , 'filter lofi disable' , 'filter nightcore enable' , 'filter nightcore disable' , 'filter drunk enable' , 'filter drunk disable' , 'filter quick enable' , 'filter quick disable' , 'filter slowmode enable' , 'filter slowmode disable' , 'filter reset'],
            "Waifu": ['setupwaifu'],
      #      "ReactionRole": ['
            "Voice": ['vcrole bots add' , 'vcrole bots remove' , 'vcrole bots' , 'vcrole config' , 'vcrole humans add' , 'vcrole humans remove' , 'vcrole humans' , 'vcrole reset' , 'vcrole'],
            "Welcomer": ['greet channel add' , 'greet channel remove' , 'greet channel' , 'greet embed' , 'greet image' , 'greet message' , 'greet ping' , 'greet test' , 'greet thumbnail' , 'greet autodel' , 'greet'],
            "Ticket": ['sendpanel'],
            "Pfps": ['pic', 'boys' , 'girls', 'couples, anime'],
            "Jsk": ['jsk' , 'jsk rtt' , 'jsk curl' , 'jsk debug' , 'jsk sync' , 'jsk py' , 'jsk permtrace' , 'jsk retain' , 'jsk tasks' , 'jsk timeit' , 'jsk dis' , 'jsk sql' , 'jsk py_inspect' , 'jsk hide' , 'jsk voice' , 'jsk git' , 'jsk show' , 'jsk cancel' , 'jsk shell' , 'jsk load' , 'jsk unload' , 'jsk override' , 'jsk invite' , 'jsk shutdown' , 'jsk pip' , 'jsk repeat']
        }

        options = [discord.SelectOption(label=cat, value=cat.lower()) for cat in categories.keys()]
        select = Select(placeholder="Choose a category...", options=options)

        async def select_callback(interaction: discord.Interaction):
            if interaction.user != self.context.author:
                return await interaction.response.send_message("You cannot interact with this menu.", ephemeral=True)

            selected_category = interaction.data['values'][0]
            commands_list = categories.get(selected_category.title(), [])
            embed = discord.Embed(
                title=f"{selected_category.title()} Commands", 
                description=" , ".join([f"`{cmd}`" for cmd in commands_list]), 
                color=0x2f3136
            )
            await interaction.response.edit_message(embed=embed, view=view)

        select.callback = select_callback
        view = View()
        view.add_item(select)

        embed = discord.Embed(description="**<:Nexus_Dot:1272554692689268813> Elevate Your Discord Experience with Best Quality Security and Versatility!**", color=0x2f3136)
        embed.add_field(name="<:Category:1272554950622445601> Use the dropdown menu to select a category.",
                       value=""" """,
                    inline=True)
                            
        embed.set_thumbnail(url=self.context.bot.user.display_avatar.url)
        embed.set_footer(text=f"Made with 💖 by Cosmic Owners", icon_url="https://cdn.discordapp.com/avatars/1096394407823028276/706ed7412d2f615b61c084ae5c6524e1.webp?size=2048")

        await self.context.reply(embed=embed, view=view, mention_author=False)


    async def send_command_help(self, command):
        with open('db/ignore.json', 'r') as heck:
            randi = json.load(heck)
        with open('db/blacklist.json', 'r') as f:
            data = json.load(f)
        if str(self.context.author.id) in data["ids"]:
            embed = discord.Embed(title="<a:Haveli_blackmagic:1147189435109224558> Blacklisted", description="You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/dwarika)", color=0x2f3136)
            return await self.context.reply(embed=embed, mention_author=False)
        elif str(self.context.channel.id) in randi["ids"]:
            return None
        else:
            if command.cog_name in ("security", "anti", "antinuke"):
                cog = self.context.bot.get_cog("Antinuke")
                with suppress(discord.HTTPException):
                    return await self.send_cog_help(cog)
            elif not command.hidden:
                await self.context.typing()
                paginator = FieldPagePaginator(self.context)
                paginator.add_command_fields([command])
                await paginator.start()
            else:
                await self.context.send(f"Command `{command.qualified_name}` not found.")
        cmds = (str(cmd) for cmd in self.context.bot.walk_commands())
        mtchs = get_close_matches(string, cmds)
        if mtchs:
          for okaay, okay in enumerate(mtchs, start=1):
            msg += f"Did You Mean: \n`[{okaay}]`. `{okay}`\n"
        return msg
        
    async def send_cog_help(self, cog):
        with open('db/ignore.json', 'r') as heck:
            randi = json.load(heck)
        with open('db/blacklist.json', 'r') as f:
            data = json.load(f)
        if str(self.context.author.id) in data["ids"]:
            embed = discord.Embed(title="<a:Haveli_blackmagic:1147189435109224558> Blacklisted", description="You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/dwarika)", color=0x2f3136)
            return await self.context.reply(embed=embed, mention_author=False)
        elif str(self.context.channel.id) in randi["ids"]:
            return None
        else:
            await self.context.typing()
            paginator = FieldPagePaginator(self.context)
            paginator.add_cog_fields(cog)
            await paginator.start()

    async def send_group_help(self, group):
        with open('db/ignore.json', 'r') as heck:
            randi = json.load(heck)
        with open('db/blacklist.json', 'r') as f:
            data = json.load(f)
        if str(self.context.author.id) in data["ids"]:
            embed = discord.Embed(title="<a:Haveli_blackmagic:1147189435109224558> Blacklisted", description="You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/dwarika)", color=0x2f3136)
            return await self.context.reply(embed=embed, mention_author=False)
        elif str(self.context.channel.id) in randi["ids"]:
            return None
        else:
            await self.context.typing()
            paginator = FieldPagePaginator(self.context)
            paginator.add_command_fields(group.commands)
            await paginator.start()

    async def send_error_message(self, error):
        raise error




class Help(Cog, name="help"):
    def __init__(self, client: Astroz):
        self._original_help_command = client.help_command
        attributes = {
            'name': "help",
            'aliases': ['h'],
            'cooldown': commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user),
            'help': 'Shows help about bot, a command or a category'
        }
        client.help_command = HelpCommand(command_attrs=attributes)
        client.help_command.cog = self

    async def cog_unload(self):
        self.help_command = self._original_help_command
