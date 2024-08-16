import discord
from discord.ext import commands
from discord.ui import Select, View
from difflib import get_close_matches
from contextlib import suppress
import json
from utils import help as vhelp, Paginator, FieldPagePaginator
from core import Context, Astroz, Cog  # Ensure `Astroz` is imported from `core`

client = Astroz()  # Make sure Astroz is properly imported



class HelpCommand(commands.HelpCommand):
    async def on_help_command_error(self, ctx, error):
        if not isinstance(error, (commands.CommandOnCooldown, commands.CommandNotFound, discord.HTTPException, commands.CommandInvokeError)):
            await self.context.reply(f"Unknown Error Occurred\n{error}", mention_author=False)
        else:
            if isinstance(error, commands.CommandOnCooldown):
                return
            await super().on_help_command_error(ctx, error)

    async def command_not_found(self, string: str) -> None:
        with open('db/blacklist.json', 'r') as f:
            data = json.load(f)
        if str(self.context.author.id) in data["ids"]:
            embed = discord.Embed(
                title="<a:Haveli_blackmagic:1147189435109224558> Blacklisted",
                description="You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/dwarika)",
                color=0x2f3136
            )
            return None
        else:
            if string in ("security", "anti", "antinuke"):
                cog = self.context.bot.get_cog("Antinuke")
                with suppress(discord.HTTPException):
                    await self.send_cog_help(cog)
            else:
                msg = f"Command `{string}` is not found...\n"
                cmds = (str(cmd) for cmd in self.context.bot.walk_commands())
                mtchs = get_close_matches(string, cmds)
                if mtchs:
                    for okaay, okay in enumerate(mtchs, start=1):
                        msg += f"Did You Mean: \n`[{okaay}]`. `{okay}`\n"
                embed1 = discord.Embed(
                    color=0x2f3136,
                    title=f"Command `{string}` is not found...\n",
                    description=msg
                )
                embed1.set_footer(text=f"Made with 💖 by Cosmic Owners",
                                  icon_url="https://cdn.discordapp.com/avatars/1096394407823028276/706ed7412d2f615b61c084ae5c6524e1.webp?size=2048")
                return None

    async def send_bot_help(self, mapping):
        await self.context.typing()
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

        # Define command categories
        categories = {
            "Antinuke": ['`antinuke` , `antinuke enable` , `antinuke disable` , `antinuke antirole-create` , `antinuke antirole-delete` , `antinuke antirole-update` , `antinuke antichannel-create` , `antinuke antichannel-delete` , `antinuke antichannel-update` , `antinuke antiban` , `antinuke antikick` , `antinuke antiwebhook` , `antinuke antibot` , `antinuke antiserver` , `antinuke antiping` , `antinuke antiprune` , `antiemoji-delete` , `antinuke antiemoji-create` , `antinuke antiemoji-update` , `antinuke show` , `antinuke punishment set` , `antinuke whitelist add` , `antinuke whitelist remove` , `antinuke whitelist show` , `antinuke whitelist reset` , `antinuke channelclean` , `antinuke roleclean` , `antinuke wl role` , `antinuke owner add` , `antinuke owner remove` , `antinuke owner show` , `antinuke owner reset`'],
            "Antialt": ['Antialt'],
            "Autorole": ['Autorolesetup'],
            "Boost": ['boostrole add` , `boostrole remove` , `boostrole config` , `boostrole reset` , `boost channel add` , `boost channel remove` , `boost channel` , `boost embed` , `boost image` , `boost message` , `boost ping` , `boost test` , `boost thumbnail` , `boost autodel` , `boost'],
            "Extra": ['stats` , `invite` , `vote` , `serverinfo` , `userinfo` , `roleinfo` , `botinfo` , `status` , `firstmessage` , `passgen` , `say` , `boostlevel` , `emoji` , `user` , `badges` , `role` , `channel` , `boosts` , `unbanall` ,  `joined-at` , `ping` , `uptime` , `github` , `vcinfo` , `channelinfo` , `note` , `notes` , `trashnotes` , `badges` , `reminder start` , `reminder delete` , `reminder list` , `list boosters` , `list inrole` , `list emojis` , `list bots` , `list admins` , `list invoice` , `list mods` , `list early` , `list activedeveloper` , `list createpos` , `list roles` , `ignore` , `ignore channel` , `ignore channel add` , `ignore channel remove` , `ignore user add` , `ignore user remove` , `ignore user show` , `banner user` , `banner server` , `logall enable` , `logall disable` , `pic`, `boys` , `girls`, `couples`, `anime` , `media`, `media setup`, `media remove`, `media config`, `media reset'],
            "Fun": ['tickle` , `kiss` , `hug` , `slap` , `pat` , `feed` , `pet` , `howgay` , `slots` , ` penis` , `meme` , `cat` , `iplookup'],
            "Games": ['akinator` , `chess` , `hangman` , `typerace` , `rps` , `reaction` , `tick-tack-toe` , `wordle` , `2048` , `memory-game` , `number-slider` , `battleship` , `country-guesser'],
            "General": ['chatgpt` , `avatar` , `servericon` , `membercount` , `poll` , `hack` , `token` , `users` , `italicize` , `strike` , `quote` , `code` , `bold` , `censor` , `underline` , `gender` , `wizz` , `pikachu` , `shorten` , `urban` , `rickroll` , `hash` , `snipe` , `setup` , `setup staff` , `setup girl` , `setup friend` , `setup vip` , `setup guest` , `setup owner` , `setup coowner` , `setup headadmin` , `setup admins` , `setup girladmin` , `setup headmod` , `setup mod` , `setup girlmod` , `setup config` , `staff` , `girl` , `friend` , `vip` , `guest` , `owner` , `coowner` , `headadmin` , `admin` , `girladmin ` , `headmod` , `mod` , `girlmod` , `remove staff` , `remove girl` , `remove friend` , `remove vip` , `remove guest` , `remove owner` , `remove coowner` , `remove headadmin` , `remove admin` , `remove girladmin` , `remove headmod` , `remove mod` , `remove girlmod` , `ar` , `ar create` , `ar delete` , `ar edit` , `ar config'],
            "Giveaway": ['giveaway` , `gstart` , `gend` , `greroll'],
            "Raidmode": ["raidmode1", "raidmode2"],
            "Moderation": ["moderation1", "moderation2"],
            "Starboard": ["starboard1", "starboard2"],
            "BoostMessage": ["boostmessage1", "boostmessage2"],
            "Music": ["music1", "music2"],
            "Waifu": ["waifu1", "waifu2"],
            "Voice": ["voice1", "voice2"],
            "Welcomer": ["welcomer1", "welcomer2"],
            "VanityRoles": ["vanityroles1", "vanityroles2"],
            "Ticket": ["ticket1", "ticket2"],
            "Pfps": ["pfps1", "pfps2"],
            "Jsk": ["jsk1", "jsk2"]
        }

        # Create Select options for categories
        options = [discord.SelectOption(label=cat, value=cat.lower()) for cat in categories.keys()]
        select = Select(placeholder="Choose a category...", options=options)

        async def select_callback(interaction: discord.Interaction):
            category = interaction.data['values'][0]
            commands_list = categories.get(category.title(), [])
            embed = discord.Embed(
                title=f"{category.title()} Commands",
                description="\n".join([f"`{cmd}`" for cmd in commands_list]),
                color=0x2f3136
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        select.callback = select_callback
        view = View()
        view.add_item(select)

        embed = discord.Embed(
            description="Use the dropdown menu to select a category.",
            color=0x2f3136
        )
        embed.set_thumbnail(url=self.context.bot.user.display_avatar.url)
        embed.set_footer(text=f"Made with 💖 by Cosmic Owners", icon_url="https://cdn.discordapp.com/avatars/1096394407823028276/706ed7412d2f615b61c084ae5c6524e1.webp?size=2048")

        await self.context.reply(embed=embed, view=view, mention_author=False)

    async def send_command_help(self, command):
        with open('db/ignore.json', 'r') as heck:
            randi = json.load(heck)
        with open('db/blacklist.json', 'r') as f:
            data = json.load(f)
        if str(self.context.author.id) in data["ids"]:
            embed = discord.Embed(
                title="<a:Haveli_blackmagic:1147189435109224558> Blacklisted",
                description="You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/dwarika)",
                color=0x2f3136
            )
            return await self.context.reply(embed=embed, mention_author=False)
        elif str(self.context.channel.id) in randi["ids"]:
            return None
        else:
            hacker = f">>> {command.help}" if command.help else '>>> No Help Provided...'
            embed = discord.Embed(
                description=f"""```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```\n{hacker}""",
                color=0x2f3136
            )
            alias = ' | '.join(command.aliases)
            embed.add_field(name="**Aliases**", value=f"{alias}" if command.aliases else "No Aliases", inline=False)
            embed.add_field(name="**Usage**", value=f"`{self.context.prefix}{command.signature}`\n")
            embed.set_author(name=f"{command.cog.qualified_name.title()}", icon_url=self.context.bot.user.display_avatar.url)
            await self.context.reply(embed=embed, mention_author=False)

    async def send_group_help(self, group):
        with open('db/ignore.json', 'r') as heck:
            randi = json.load(heck)
        with open('db/blacklist.json', 'r') as f:
            idk = json.load(f)
        if str(self.context.author.id) in idk["ids"]:
            embed = discord.Embed(
                title="<a:Haveli_blackmagic:1147189435109224558> Blacklisted",
                description="You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/dwarika)",
                color=0x2f3136
            )
            return await self.context.reply(embed=embed, mention_author=False)
        elif str(self.context.channel.id) in randi["ids"]:
            return None
        else:
            entries = [(
                f"`{self.context.prefix}{cmd.qualified_name}`",
                f"{cmd.short_doc if cmd.short_doc else 'No Description Provided...'}\n\n"
            ) for cmd in group.commands]
            paginator = Paginator(source=FieldPagePaginator(
                entries=entries,
                title=f"{group.qualified_name} Commands",
                description="<...> Duty | [...] Optional\n\n",
                color=0x2f3136,
                per_page=10
            ), ctx=self.context)
            await paginator.paginate()

    async def send_cog_help(self, cog):
        with open('db/ignore.json', 'r') as heck:
            randi = json.load(heck)
        with open('db/blacklist.json', 'r') as f:
            data = json.load(f)
        if str(self.context.author.id) in data["ids"]:
            embed = discord.Embed(
                title="<a:Haveli_blackmagic:1147189435109224558> Blacklisted",
                description="You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/dwarika)",
                color=0x2f3136
            )
            return await self.context.reply(embed=embed, mention_author=False)
        elif str(self.context.channel.id) in randi["ids"]:
            return None
        entries = [(
            f"`{self.context.prefix}{cmd.qualified_name}`",
            f"{cmd.short_doc if cmd.short_doc else 'No Description Provided...'}\n\n"
        ) for cmd in cog.get_commands()]
        paginator = Paginator(source=FieldPagePaginator(
            entries=entries,
            title=f"{cog.qualified_name.title()} ({len(cog.get_commands())})",
            description="<...> Duty | [...] Optional\n\n",
            color=0x2f3136,
            per_page=10
        ), ctx=self.context)
        await paginator.paginate()

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
