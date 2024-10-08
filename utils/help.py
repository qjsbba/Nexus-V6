import discord
import functools
from utils.Tools import *


class Dropdown(discord.ui.Select):

    def __init__(self, ctx, options):
        super().__init__(placeholder="Please Select A Module From Here.",
                         min_values=1,
                         max_values=1,
                         options=options)
        self.invoker = ctx.author

    async def callback(self, interaction: discord.Interaction):
        if self.invoker == interaction.user:
            index = self.view.find_index_from_select(self.values[0])
            if not index: index = 0
            await self.view.set_page(index, interaction)
        else:
            await interaction.response.send_message(
                "Run Your Own Help Command", ephemeral=True)

class Dropdown2(discord.ui.Select):

    def __init__(self, ctx, options):
        super().__init__(placeholder="› Nexus Is Love.",
                         min_values=1,
                         max_values=1,
                         options=options)
        self.invoker = ctx.author

    async def callback(self, interaction: discord.Interaction):
        if self.invoker == interaction.user:
            index = self.view.find_index_from_select(self.values[0])
            if not index: index = 0
            await self.view.set_page(index, interaction)
        else:
            await interaction.response.send_message(
                "Run Your Own Help Command", ephemeral=True)

class Dropdown3(discord.ui.Select):

    def __init__(self, ctx, options):
        super().__init__(placeholder="Please Select A Module From Here.",
                         min_values=1,
                         max_values=1,
                         options=options)
        self.invoker = ctx.author

    async def callback(self, interaction: discord.Interaction):
        if self.invoker == interaction.user:
            index = self.view.find_index_from_select(self.values[0])
            if not index: index = 0
            await self.view.set_page(index, interaction)
        else:
            await interaction.response.send_message(
                "Run Your Own Help Command", ephemeral=True)


class Buttons(discord.ui.Button):

    def __init__(self,
                 command,
                 ctx,
                 emoji,
                 style: discord.ButtonStyle,
                 args=None):
        disable = False
        if args == -1 or args == 0: disable = True
        super().__init__(emoji=emoji, style=style, disabled=disable)
        self.command = command
        self.invoker = ctx.author
        self.args = args

    async def callback(self, interaction: discord.Interaction):
        if self.invoker == interaction.user:
            if self.args or self.args == 0:
                func = functools.partial(self.command, self.args, interaction)
                await func()
            else:
                await self.command(interaction)
        else:
            await interaction.response.send_message(
                "Run Your Own Help Command", ephemeral=True)
           


class View(discord.ui.View):

    def __init__(self, mapping: dict,
                 ctx: discord.ext.commands.context.Context,
                 homeembed: discord.embeds.Embed, ui: int):
        super().__init__()
        self.mapping, self.ctx, self.home = mapping, ctx, homeembed
        self.index, self.buttons = 0, None

        self.options, self.embeds = self.gen_embeds()

        if ui == 0: self.add_item(Dropdown(ctx=self.ctx, options=self.options))
        #if ui == 0: self.add_item(Dropdown2(ctx=self.ctx, options=self.options))
       #if ui == 0: self.add_item(Dropdown3(ctx=self.ctx, options=self.options))     
        elif ui == 1: self.buttons = self.add_buttons()
        else:
            self.buttons = self.add_buttons()
            self.add_item(Dropdown(ctx=self.ctx, options=self.options))
            #self.add_item(Dropdown2(ctx=self.ctx, options=self.options))
            #self.add_item(Dropdown3(ctx=self.ctx, options=self.options))

    def add_buttons(self):
        self.startB = Buttons(emoji="<:arrowleft:1153634053992489012>",
                              style=discord.ButtonStyle.grey,
                              command=self.set_page,
                              args=0,
                              ctx=self.ctx)
        self.backB = Buttons(emoji="<:labs_left:1153633608943284324>",
                             style=discord.ButtonStyle.grey,
                             command=self.to_page,
                             args=-1,
                             ctx=self.ctx)
        self.nextB = Buttons(emoji="<:labs_right:1153633611149496330>",
                             style=discord.ButtonStyle.grey,
                             command=self.to_page,
                             args=+1,
                             ctx=self.ctx)
        self.endB = Buttons(emoji="<:IconArrow:1153634053799546910>",
                            style=discord.ButtonStyle.grey,
                            command=self.set_page,
                            args=len(self.options) - 1,
                            ctx=self.ctx)
        self.quitB = Buttons(emoji="<:delete_icons:1153633682301648906>",
                             style=discord.ButtonStyle.grey,
                             command=self.quit,
                             ctx=self.ctx)
        buttons = [self.startB, self.backB, self.quitB, self.nextB, self.endB]
        for button in buttons:
            self.add_item(button)
        return buttons

    def find_index_from_select(self, value):
        i = 0
        for cog in self.get_cogs():
            if "help_custom" in dir(cog):
                _, label, _ = cog.help_custom()
                if label == value: return i + 1
                i += 1

    def get_cogs(self):
        cogs = []
        for cog in self.mapping.keys():
            cogs.append(cog)
        return cogs

    def gen_embeds(self):
        options, embeds = [], []
        options.append(
            discord.SelectOption(label="Home",
                              emoji='<:nexus_home:1144620610450894978>'))
        embeds.append(self.home)
        for cog in self.get_cogs():
            if "help_custom" in dir(cog):
                emoji, label, description = cog.help_custom()
                options.append(discord.SelectOption(label=label, emoji=emoji, description=description))
                embed = discord.Embed(title=f"{emoji} {label} Commands",
                                      color=0x2f3136)
                embed.set_footer(
                    text="Made with 💖 by Cosmic Owners",
                    icon_url="https://cdn.discordapp.com/avatars/1096394407823028276/706ed7412d2f615b61c084ae5c6524e1.webp?size=2048"
                )
                for command in cog.get_commands():
                    params = ""
                    for param in command.clean_params:
                        params += f" <{param}>"
                    embed.add_field(name=f"{command.name}{params}",
                                    value=f"{command.help}\n\u200b",
                                    inline=False)
                embeds.append(embed)
        return options, embeds

    async def quit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.message.delete()

    async def to_page(self, page: int, interaction: discord.Interaction):
        if not self.index + page < 0 or not self.index + page > len(
                self.options):
            await self.set_index(page)
            embed = self.embeds[self.index]

            await interaction.response.edit_message(embed=embed, view=self)

    async def set_page(self, page: int, interaction: discord.Interaction):
        self.index = page
        await self.to_page(0, interaction)

    async def set_index(self, page):
        self.index += page
        if self.buttons:
            for button in self.buttons[0:-1]:
                button.disabled = False
            if self.index == 0:
                self.backB.disabled = True
                self.startB.disabled = True
            elif self.index == len(self.options) - 1:
                self.nextB.disabled = True
                self.endB.disabled = True