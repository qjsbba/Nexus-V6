import json
import discord
from discord.ext import commands

class react(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_triggers = {}


        try:
            with open('reaction_triggers.json', 'r') as f:
                self.reaction_triggers = json.load(f)
        except FileNotFoundError:
            pass


    def save_reaction_triggers(self):
        with open('reaction_triggers.json', 'w') as f:
            json.dump(self.reaction_triggers, f)


    def is_admin():
        def predicate(ctx):
            return ctx.author.guild_permissions.administrator
        return commands.check(predicate)

    @commands.group(invoke_without_command=True)
    @is_admin()
    async def react(self, ctx):
        await ctx.send("**<:Nexus_cross:1144687282176147629> | Invalid action. Available actions: `remove`, `clear`, `list`, `add`")

    @react.command()
    async def remove(self, ctx, *, trigger):
        if trigger in self.reaction_triggers:
            del self.reaction_triggers[trigger]
            self.save_reaction_triggers()
            await ctx.send(f"** <:Nexus_tick:1144687280540369018>  | Removed reaction trigger for {trigger} **")
        else:
            await ctx.send(f"**<:icons_exclamation:1144986614804787310> |No reaction trigger found for '{trigger}'**")

    @react.command()
    async def clear(self, ctx):
        self.reaction_triggers.clear()
        self.save_reaction_triggers()
        await ctx.send("Cleared all reaction triggers")

    @react.command()
    async def list(self, ctx, *, view=None):
        if not self.reaction_triggers:
            await ctx.send("**<:icons_exclamation:1144986614804787310> |There are no reaction triggers set**")
        else:
            if view == 'raw':
                await ctx.send(self.reaction_triggers)
            else:
                message = "Current reaction triggers:\n"
                for trigger, reaction in self.reaction_triggers.items():
                    message += f"{trigger}: {reaction}\n"
                await ctx.send(message)

    @react.command()
    async def add(self, ctx, trigger, *reactions):
      if len(reactions) > 3:
        await ctx.send("**<:icons_exclamation:1144986614804787310> | You can only add up to 3 emojis to any reaction.**")
        return

      reaction = " ".join(reactions)  # concatenate the list of emojis into a single string
      self.reaction_triggers[trigger] = reaction
      self.save_reaction_triggers()
      await ctx.send(f"** <:Nexus_tick:1144687280540369018> | Added reaction trigger for {trigger} with {reaction} emoji reaction.**")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        for trigger, reaction in self.reaction_triggers.items():
            if trigger.lower() in message.content.lower():
                await message.add_reaction(reaction)