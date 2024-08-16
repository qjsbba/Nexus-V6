import os
import discord
from discord.ext import commands
import json
import datetime
from reactionmenu import ViewMenu, ViewButton

class PaginationViewWallah:
    def __init__(self, embed_list, ctx):
        self.elist = embed_list
        self.context = ctx

    def disable_button(self, menu):
        tax = str(menu.message.embeds[0].footer.text).replace(" ", "").replace("Page", "")
        num = int(tax[0])
        if num == 1:
            fis = menu.get_button("2", search_by="id")
            bax = menu.get_button("1", search_by="id")

    def enable_button(self, menu):
        tax = str(menu.message.embeds[0].footer.text).replace(" ", "").replace("Page", "")
        num = int(tax[0])
        if num != 1:
            fis = menu.get_button("2", search_by="id")
            bax = menu.get_button("1", search_by="id")
            print(bax)

    async def start(self, ctx, disxd=False):
        style = f"{ctx.bot.user.name} • Page $/&"
        menu = ViewMenu(ctx, menu_type=ViewMenu.TypeEmbed, style=style)
        for xem in self.elist:
            menu.add_page(xem)
        lax = ViewButton(style=discord.ButtonStyle.secondary, label=None, emoji='⏪', custom_id=ViewButton.ID_GO_TO_FIRST_PAGE)
        menu.add_button(lax)
        bax = ViewButton(style=discord.ButtonStyle.secondary, label=None, emoji='◀️', custom_id=ViewButton.ID_PREVIOUS_PAGE)
        menu.add_button(bax)
        bax2 = ViewButton(style=discord.ButtonStyle.secondary, label=None, emoji='⏹️', custom_id=ViewButton.ID_END_SESSION)
        menu.add_button(bax2)
        bax3 = ViewButton(style=discord.ButtonStyle.secondary, label=None, emoji='▶️', custom_id=ViewButton.ID_NEXT_PAGE)
        menu.add_button(bax3)
        sax = ViewButton(style=discord.ButtonStyle.secondary, label=None, emoji='⏩', custom_id=ViewButton.ID_GO_TO_LAST_PAGE)
        menu.add_button(sax)
        if disxd:
            menu.disable_all_buttons()
        menu.disable_button(lax)
        menu.disable_button(bax)

        async def all_in_one_xd(payload):
            newmsg = await ctx.channel.fetch_message(menu.message.id)
            tax = str(newmsg.embeds[0].footer.text).replace(f"{ctx.bot.user.name}", "").replace(" ", "").replace("Page", "").replace("•", "")
            saxl = tax.split("/")
            num = int(saxl[0])
            numw = int(saxl[1])
            if num == 1:
                menu.disable_button(lax)
                menu.disable_button(bax)
            else:
                menu.enable_button(lax)
                menu.enable_button(bax)
            if num == numw:
                menu.disable_button(bax3)
                menu.disable_button(sax)
            else:
                menu.enable_button(bax3)
                menu.enable_button(sax)
            await menu.refresh_menu_items()

        menu.set_relay(all_in_one_xd)
        await menu.start()

async def working_lister(ctx, color, listxd, *, title):
    embed_array = []
    t = title
    clr = color
    sent = []
    your_list = listxd
    count = 0
    idkh = True
    embed = discord.Embed(color=clr, description="", title=t)
    embed.set_footer(icon_url=ctx.bot.user.avatar)
    if idkh:
        for i in range(len(listxd)):
            for i__ in range(10):
                if not your_list[i].id in sent:
                    count += 1
                    if str(count).endswith("0") or len(str(count)) != 1:
                        actualcount = str(count)
                    else:
                        actualcount = f"0{count}"
                    embed.description += f"`[{actualcount}]` | {your_list[i]} [<@{your_list[i].id}>]\n"
                    sent.append(your_list[i].id)
            if str(count).endswith("0") or str(count) == str(len(your_list)):
                embed_array.append(embed)
                embed = discord.Embed(color=clr, description="", title=t)
                embed.set_footer(icon_url=ctx.bot.user.avatar)

    if len(embed_array) == 0:
        embed_array.append(embed)
    pag = PaginationViewWallah(embed_array, ctx)
    if len(embed_array) == 1:
        await pag.start(ctx, True)
    else:
        await pag.start(ctx)


async def working_lister_hai(ctx, color, listxd, *, title):
    embed_array = []
    t = title
    clr = color
    sent = []
    your_list = listxd
    count = 0
    idkh = True
    embed = discord.Embed(color=clr, description="", title=t)
    embed.set_footer(icon_url=ctx.bot.user.avatar)
    if idkh:
        for i in range(len(listxd)):
            for i__ in range(10):
                if not your_list[i][0].id in sent:
                    count += 1
                    if str(count).endswith("0") or len(str(count)) != 1:
                        actualcount = str(count)
                    else:
                        actualcount = f"0{count}"
                    embed.description += f"`[{actualcount}]` | {your_list[i][0]} [<@{your_list[i][0].id}>] - Msgs {your_list[i][1]}\n"
                    sent.append(your_list[i][0].id)
            if str(count).endswith("0") or str(count) == str(len(your_list)):
                embed_array.append(embed)
                embed = discord.Embed(color=clr, description="", title=t)
                embed.set_footer(icon_url=ctx.bot.user.avatar)

    if len(embed_array) == 0:
        embed_array.append(embed)
    pag = PaginationViewWallah(embed_array, ctx)
    if len(embed_array) == 1:
        await pag.start(ctx, True)
    else:
        await pag.start(ctx)


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = bot
        self.path = "db/messagedb.json"
        self.initialize_db()

    def initialize_db(self):
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, 'w') as f:
                json.dump({}, f, indent=4)

    def set_msg(self, author, guild, created):
        with open(self.path, "r") as f:
            file = json.load(f)

        # Check if guild exists
        if str(guild) not in file:
            file[str(guild)] = {"list": []}

        # Find existing message count for the author
        amnt = sum(1 for i in file[str(guild)]["list"] if i["author"] == author)
        file[str(guild)]["list"].append({"author": author, "created": created, "amount": amnt})

        with open(self.path, "w") as f:
            json.dump(file, f, indent=4)

    def reset(self, guild):
        with open(self.path, "r") as f:
            file = json.load(f)

        # Reset only if the guild exists
        if str(guild) in file:
            file[str(guild)]["list"] = []

            with open(self.path, "w") as f:
                json.dump(file, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.set_msg(guild.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild:
            return
        self.set_msg(message.author.id, message.guild.id, f"{datetime.date.today()}")

    @commands.group(name="messages", aliases=["message"], invoke_without_command=True)
    async def _msg(self, ctx, user: discord.Member = None):
        alr = user or ctx.author
        with open(self.path, "r") as f:
            ok = json.load(f)

        # Check if the guild exists in the database
        if str(ctx.guild.id) not in ok:
            return await ctx.send("No Message Data Found For This Guild. Created Database For This Guild")

        knt = 0
        tnt = 0
        for item in ok[str(ctx.guild.id)]["list"]:
            if int(item.get("author")) == alr.id:
                knt += 1
                if item.get("created") == f"{datetime.date.today()}":
                    tnt += 1
        if knt != 0:
            embed = discord.Embed(title="", description=f"{alr.mention} sent a total of **{knt}** messages in this server out of which **{tnt}** are sent today.", color=0x2f3136)
            embed.set_author(name=f"{alr}", icon_url=alr.avatar)
            embed.set_footer(text="Nexus", icon_url=self.client.user.avatar)
            return await ctx.send(embed=embed)
        lund = discord.Embed(title="", description=f"{alr.mention} didn't send any messages in this server yet.", color=0x2f3136)
        lund.set_author(name=f"{alr}", icon_url=alr.avatar)
        lund.set_footer(text="Nexus", icon_url=self.client.user.avatar)
        await ctx.send(embed=lund)

    @_msg.command(name="leaderboard", aliases=["lb"])
    async def _leaderboard(self, ctx):
        with open(self.path, "r") as f:
            ok = json.load(f)

        # Check if the guild exists in the database
        if str(ctx.guild.id) not in ok:
            return await ctx.send("No message data found for this guild.")

        old_list = ok[str(ctx.guild.id)]["list"]
        leaderboard = {}
        for user in old_list:
            leaderboard[user["author"]] = leaderboard.get(user["author"], 0) + 1

        sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
        sorted_users = [(ctx.guild.get_member(int(user_id)), msg_count) for user_id, msg_count in sorted_leaderboard]
        await working_lister_hai(ctx, 0x2f3136, sorted_users, title="Top Message Senders")

    @_msg.command(name="reset")
    @commands.has_permissions(manage_messages=True)
    async def _reset(self, ctx):
        self.reset(ctx.guild.id)
        await ctx.send("Message leaderboard has been reset.")
