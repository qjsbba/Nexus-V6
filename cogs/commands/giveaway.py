import discord
import asyncio
from discord.ext import commands
import datetime
import time 
import json
import random
from discord.ui import View, Button
import aiohttp
from typing import Union
from utils.Tools import *

giveaway_users = []


def convert(date):
    pos = ["s", "m", "h", "d"]
    time_dic = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
    i = {"s": "Seconds", "m": "Minutes", "h": "Hours", "d": "Days"}
    unit = date[-1]
    if unit not in pos:
        return -1
    try:
        val = int(date[:-1])

    except ValueError:
        return -2

    if val == 1:
        return val * time_dic[unit], i[unit][:-1]
    else:
        return val * time_dic[unit], i[unit]

class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = None):
        super().__init__(timeout=timeout)
        self.ctx = ctx

class test(BasicView):
    def __init__(self, ctx: commands.Context, time):
        super().__init__(ctx, timeout=time)
        self.value = None
    
    @discord.ui.button(label=f"0",emoji=f'<a:bb_eg_tada:1144981797122347098>', style=discord.ButtonStyle.gray,custom_id=f'give')
    async def dare(self, interaction: discord.Interaction, button):
        pass
        '''giveaway_users = []
        try:
            with open(f"giveaway_users/{interaction.channel.name}.txt", "r") as file:
                for line in file:
                    stripped_line = line.strip()
                    giveaway_users.append(stripped_line)

            if str(interaction.user.id) not in giveaway_users:
                number = int(button.label) if button.label else 0
                button.label = str(number + 1)
                await interaction.response.edit_message(view=self)
                await interaction.channel.send(f"<@{interaction.user.id}> You have successfully entered the giveaway!", delete_after=1)
                a = interaction.user.id
                with open(f"giveaway_users/{interaction.channel.name}.txt", "a") as file:
                    file.write(f"{str(a)}\n")

            else:
                number = int(button.label)
                button.label = str(number - 1)
                await interaction.response.edit_message(view=self)
                await interaction.channel.send(f"<@{interaction.user.id}> You have successfully left the giveaway!", delete_after=1)
                #await interaction.response.send_message("Left Giveaway", ephemeral=True)
                a = interaction.user.id
                giveaway_users.remove(str(a))
                with open(f"giveaway_users/{interaction.channel.name}.txt", 'w') as file:
                    idk = file.read().split('\n').remove(str(a))
                file.write(f"{idk}")
                #await interaction.response.send_message("You Have Left This Giveaway", ephemeral=True)
        except IOError:
            if len(str(interaction.channel.name)) <= 4:
                await interaction.response.send_message(f"<:cross:1077478135794245743> This Giveaway Has Been Ended.", ephemeral=True)'''


class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2f3136

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
      if interaction.type == discord.InteractionType.component:
        with open('db/giveaways.json', 'r') as f:
          data = json.load(f)
        if str(interaction.message.id) in data:
          button = interaction.message.components[0].children[0]
          giveaway_users = []
          try:
              with open(f"db/giveaway_users/{interaction.channel.name}.txt", "r") as file:
                for line in file:
                    stripped_line = line.strip()
                    giveaway_users.append(stripped_line)

              if str(interaction.user.id) not in giveaway_users:
                number = int(button.label) if button.label else 0
                btn = Button(label=str(number+1),emoji=f'<a:bb_eg_tada:1144981797122347098>', style=discord.ButtonStyle.gray,custom_id=f'give')
                view = View()
                view.add_item(btn)
                await interaction.response.edit_message(view=view)
                
                a = interaction.user.id
                with open(f"giveaway_users/{interaction.channel.name}.txt", "a") as file:
                    file.write(f"{str(a)}\n")

              else:
                number = int(button.label)
                btn = Button(label=str(number-1),emoji=f'<a:bb_eg_tada:1144981797122347098>', style=discord.ButtonStyle.gray,custom_id=f'give')
                view = View()
                view.add_item(btn)
                await interaction.response.edit_message(view=view)
                
                #await interaction.response.send_message("Left Giveaway", ephemeral=True)
                a = interaction.user.id
                giveaway_users.remove(str(a))
                with open(f"giveaway_users/{interaction.channel.name}.txt", 'w') as file:
                    idk = file.read().split('\n').remove(str(a))
                file.write(f"{idk}")
                #await interaction.response.send_message("You Have Left This Giveaway", ephemeral=True)
          except IOError:
            if len(str(interaction.channel.name)) <= 4:
                await interaction.response.send_message(f"<:Nexus_cross:1144687282176147629> This Giveaway Has Been Ended.", ephemeral=True)
        else:
          pass
      else:
        pass

    @commands.hybrid_command(description="Creates a giveaway")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @iuser_check()
    async def gstart(self, ctx):
        await ctx.message.delete()
        init = await ctx.send(embed=discord.Embed(
            title=f"<a:nexus_giveaways:1144982543049969825> New Giveaway ! <a:nexus_giveaways:1144982543049969825>",
            description=f"Please answer the following questions to finalize the creation of the Giveaway",
            color=self.color)
                              .set_footer(icon_url=self.bot.user.display_avatar.url, text=self.bot.user.name))

        questions = [
            "Can You Tell Me What The Giveaway Prize Will Be ?\nLike : `Nitro Boost`",
            f"In What Channel Would You Like The Giveaway To Be Held ? ( Please Mention The Giveaway Channel )\nExample : {ctx.channel.mention}",
            "Can You Tell Me How Long The Giveaway Will Run ?\nExample: `10d` | `10h` | `10m` | `10s`",
            "How Many Winners Do You Want For This Giveaway ?\nExample: `1` | `2` | `3`"
        ]

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        index = 1
        answers = []
        now = int(time.time())
        question_message = None
        for question in questions:
            embed = discord.Embed(
                title=f"<a:nexus_giveaways:1144982543049969825> Giveaway",
                description=question,
                color=0x2f3136
            ).set_footer(icon_url=self.bot.user.display_avatar.url, text=f"Giveaway !")
            if index == 1:
                question_message = await ctx.send(embed=embed)
            else:
                await question_message.edit(embed=embed)

            try:
                user_response = await self.bot.wait_for(f"message", timeout=None, check=check)
                await user_response.delete()
            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(
                    title=f"Error",
                    color=self.color,
                    description=f"<:Nexus_cross:1144687282176147629> | Please setup the giveaway again ):."
                ))
                return
            else:
                answers.append(user_response.content)
                index += 1
        try:
            channel_id = int(answers[1][2:-1])
        except ValueError:
            await ctx.send("<:Nexus_cross:1144687282176147629> | Mention The Channel Correctly!, do it like {}.".format(ctx.channel.mention))
            return

        try:
            winners = abs(int(answers[3]))
            if winners == 0:
                await ctx.send(f"<:Nexus_cross:1144687282176147629> | You did not enter the number correctly.")
                return
        except ValueError:
            await ctx.send(f"<:Nexus_cross:1144687282176147629> | You did not enter an correctly.")
            return
        prize = answers[0].title()
        channel = self.bot.get_channel(channel_id)
        converted_time = convert(answers[2])
        if converted_time == -1:
            await ctx.send(f"<:Nexus_cross:1144687282176147629> | Enter The Time Correctly (s|m|d|h)")
        elif converted_time == -2:
            await ctx.send(f"<:Nexus_cross:1144687282176147629> | Enter The Time Correctly (s|m|d|h)")
            return
        await init.delete()
        await question_message.delete()
        giveaway_embed = discord.Embed(
            title="<a:Tada_Animated:1144981727840829532> {} <a:Tada_Animated:1144981727840829532>".format(prize),
            color=self.color,
            description=f'Click On <a:bb_eg_tada:1144981797122347098> To Get Into The Giveaway.\n'
                        f'Winner : *{winners} winner*\n'
                        f'Ends: <t:{now + converted_time[0]}:R> (<t:{now + converted_time[0]}:f>)\n'
                        f'Hosted by: {ctx.author.mention}\n\n'
                        f'[Invite Nexus](https://nexus-bot.carrd.co/) 🔹 [Support Server](https://discord.gg/zvU2mGPa6Y)\n'
                        
        ) \
            .set_footer(icon_url=self.bot.user.display_avatar.url, text=f"Ends at") \
            #.set_thumbnail(url=self.bot.user.display_avatar.url)

        giveaway_embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=converted_time[0])
        action_row = test(ctx, now+converted_time[0])
        giveaway_message = await channel.send(embed=giveaway_embed, view=action_row)
        with open(f"db/giveaways.json", "r") as f:
            giveaways = json.load(f)

            data = {
                "prize": prize,
                "host": ctx.author.id,
                "winners": winners,
                "end_time": now + converted_time[0],
                "channel_id": channel.id,
                "button_id": channel.name,
                "link": giveaway_message.jump_url,
                "ended": False
            }
            giveaways[str(giveaway_message.id)] = data

        with open(f"db/giveaways.json", "w") as f:
            json.dump(giveaways, f, indent=4)
        with open(f"giveaway_users/{data['button_id']}.txt", "w"):
            pass


    @commands.hybrid_command(description="Ends a giveaway early")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @iuser_check()
    async def gend(self, ctx, message: int):
      try:
        msg = await ctx.fetch_message(message)
      except:
        await ctx.send("Error")
      with open('db/giveaways.json', 'r') as f:
        data = json.load(f)
      if not str(message) in data:
        return await ctx.send("No ongoing giveaway found")
      data2 = {
                "prize": data[str(message)]["prize"],
                "host": data[str(message)]['host'],
                "winners": data[str(message)]["winners"],
                "end_time": int(time.time()),
                "channel_id": data[str(message)]["channel_id"],
                "button_id": data[str(message)]["button_id"],
                "link": data[str(message)]["link"], 
                "ended": False
            }
      data[str(message)] = data2
      with open(f"db/giveaways.json", "w") as f:
        json.dump(data, f, indent=4)


    @commands.hybrid_command(description="Reroll a giveaway")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @iuser_check()
    async def greroll(self, ctx, message: int):
      users = []
      try:
        msg = await ctx.fetch_message(message)
      except:
        await ctx.send("Error")
      with open('db/giveaways.json', 'r') as f:
        data = json.load(f)
      if str(message) not in data:
        return await ctx.send("No previous giveaway found with this message id")
      elif not data[str(message)]["ended"]:
        return await ctx.send("Giveaway is still going on")
      else:
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        await ctx.send("Winners do you want to reroll for the giveaway?\n\n**Note**: You must choose a number between 1 and 15.")
        try:
          user_response = await self.bot.wait_for(f"message", timeout=None, check=check)
          await user_response.delete()
        except asyncio.TimeoutError:
          await ctx.send(embed=discord.Embed(
                    title=f"Error",
                    color=self.color,
                    description=f"<:tick:1076042204310679562> | You took too long to answer this question, Please setup the giveaway again ):."
                ))
          return
        try:
          winners = int(user_response.content)
        except:
          await ctx.send("Invalid Winners, run command again!")
        if winners > 15 or winners < 1:
          return await ctx.send("Either winners are more than 15 or less than 1")
        with open(f"db/giveaway_users/{data[str(message)]['button_id']}.txt", "r") as file:
          for line in file:
            stripped_line = line.strip()
            users.append(stripped_line)
          if len(users) < winners:
            winners = len(users)
          msg = ''
          winner = random.sample(users, winners)
          for i in winner:
            if len(winner) == 1:
              msg += f'<@{i}>'
            else:
              msg += f'<@{i}>\n'
          prize = data[str(message)]["prize"]
          link = data[str(message)]["link"]
          host = data[str(message)]["host"]
          result_embed = discord.Embed(color=0x2f3136,
                    description=f"You won **[{prize}]({link})**. Contact the giveaway host - <@{host}> - to claim your rewards!")
          #result_embed.set_thumbnail(url=self.bot.user.display_avatar.url)
          await ctx.channel.send(content=f"**Congratulations** {msg}!", embed=result_embed, view=None)

