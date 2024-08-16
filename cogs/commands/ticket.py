import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import sqlite3
import datetime
import os

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('db/tickets.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ticket_panels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            channel_id INTEGER,
            title TEXT,
            description TEXT,
            image TEXT,
            category_id INTEGER,
            role_id INTEGER
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            channel_id INTEGER,
            created_at TIMESTAMP,
            status TEXT
        )
        ''')
        self.conn.commit()

    @commands.group(name="ticket", invoke_without_command=True, help="Manage tickets")
    async def ticket(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Ticket Commands",
            description="Here are the available commands for managing tickets:",
            color=discord.Color.blue()
        )
        embed.add_field(name="ticket panel create", value="Create a new ticket panel", inline=False)
        embed.add_field(name="ticket panel delete", value="Delete an existing ticket panel by ID", inline=False)
        embed.add_field(name="ticket panel list", value="List all ticket panels in this server", inline=False)
        embed.add_field(name="ticket create", value="Create a new ticket", inline=False)
        embed.add_field(name="ticket close", value="Close an existing ticket", inline=False)
        embed.add_field(name="ticket transcript", value="Generate a transcript for a closed ticket", inline=False)
        await ctx.send(embed=embed)

    @ticket.group(name="panel", invoke_without_command=True, help="Manage ticket panels")
    async def ticket_panel(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Panel Commands",
            description="Here are the available commands for managing ticket panels:",
            color=discord.Color.blue()
        )
        embed.add_field(name="ticket panel create", value="Create a new ticket panel", inline=False)
        embed.add_field(name="ticket panel delete", value="Delete an existing ticket panel by ID", inline=False)
        embed.add_field(name="ticket panel list", value="List all ticket panels in this server", inline=False)
        await ctx.send(embed=embed)

    @ticket_panel.command(name="create", help="Create a ticket panel")
    @commands.has_permissions(administrator=True)
    async def ticket_panel_create(self, ctx: commands.Context):
        responses = {}

        async def ask_questions():
            questions = {
                "channel": "Mention the channel where the panel will be created",
                "title": "What will be the title of the panel?",
                "description": "What will be the description of the panel?",
                "image": "Provide the URL of the image (or 'none' to skip)",
                "category": "Mention the ticket category (channel will be created here)",
                "role": "Mention the role to be pinged (or 'none' to skip)"
            }

            for key, question in questions.items():
                await ctx.send(question)
                message = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                responses[key] = message.content if key != "channel" else message.channel_mentions[0]

            # Convert responses
            responses["image"] = None if responses["image"].lower() == 'none' else responses["image"]
            responses["category_id"] = int(responses["category"].id)
            responses["role_id"] = None if responses["role"].lower() == 'none' else int(responses["role"][3:-1])

            # Insert panel into database
            self.insert_panel(
                ctx.guild.id, responses["channel"].id, responses["title"], 
                responses["description"], responses["image"], 
                responses["category_id"], responses["role_id"]
            )

            # Create the panel message
            embed = discord.Embed(title=responses["title"], description=responses["description"], color=discord.Color.green())
            if responses["image"]:
                embed.set_image(url=responses["image"])

            button = Button(label="Create Ticket", style=discord.ButtonStyle.green)
            view = View()
            view.add_item(button)

            await responses["channel"].send(embed=embed, view=view)

            await ctx.send(embed=discord.Embed(
                title="Panel Created",
                description=f"Ticket panel '{responses['title']}' created successfully.",
                color=discord.Color.green()
            ))

        await ask_questions()

    @ticket_panel.command(name="delete", help="Delete a ticket panel")
    @commands.has_permissions(administrator=True)
    async def ticket_panel_delete(self, ctx: commands.Context, panel_id: int):
        self.delete_panel(panel_id)
        await ctx.send(embed=discord.Embed(
            title="Panel Deleted",
            description=f"Ticket panel with ID {panel_id} has been deleted.",
            color=discord.Color.red()
        ))

    @ticket_panel.command(name="list", help="List all ticket panels")
    @commands.has_permissions(administrator=True)
    async def ticket_panel_list(self, ctx: commands.Context):
        panels = self.fetch_panels(ctx.guild.id)
        if panels:
            description = "\n".join([f"ID: {panel[0]} | Title: {panel[1]}" for panel in panels])
            embed = discord.Embed(
                title="Ticket Panels",
                description=description,
                color=discord.Color.blue()
            )
        else:
            embed = discord.Embed(
                title="No Panels Found",
                description="No ticket panels found for this guild.",
                color=discord.Color.orange()
            )
        await ctx.send(embed=embed)

    @ticket.command(name="create", help="Create a ticket")
    async def ticket_create(self, ctx: commands.Context):
        existing_ticket = self.fetch_open_ticket(ctx.guild.id, ctx.author.id)
        if existing_ticket:
            await ctx.send("You already have an open ticket.")
            return

        # Create a new channel for the ticket
        guild = ctx.guild
        category = discord.utils.get(guild.categories, id=self.fetch_category(ctx.guild.id))
        channel = await guild.create_text_channel(f"ticket-{ctx.author.name}", category=category)

        # Save ticket info to database
        self.insert_ticket(ctx.guild.id, ctx.author.id, channel.id)

        await channel.send(f"Ticket created by {ctx.author.mention}.")
        await ctx.send(f"Your ticket has been created: {channel.mention}")

    @ticket.command(name="close", help="Close a ticket")
    @commands.has_permissions(administrator=True)
    async def ticket_close(self, ctx: commands.Context):
        ticket_info = self.fetch_ticket_by_channel(ctx.guild.id, ctx.channel.id)
        if not ticket_info:
            await ctx.send("This channel is not associated with a ticket.")
            return

        # Change ticket status to closed
        self.update_ticket_status(ticket_info[0], "closed")

        await ctx.send("Ticket closed. Generating transcript...")
        await self.generate_transcript(ctx.channel)
        await ctx.channel.delete()

    @ticket.command(name="transcript", help="Generate a transcript for a ticket")
    @commands.has_permissions(administrator=True)
    async def ticket_transcript(self, ctx: commands.Context):
        await self.generate_transcript(ctx.channel)

    async def generate_transcript(self, channel):
        messages = await channel.history(limit=None, oldest_first=True).flatten()
        transcript = ""

        for message in messages:
            timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            transcript += f"[{timestamp}] {message.author}: {message.content}\n"

        transcript_file = f"transcripts/{channel.name}.txt"
        with open(transcript_file, "w") as f:
            f.write(transcript)

        await channel.send(file=discord.File(transcript_file))

    # Helper Methods
    def insert_panel(self, guild_id, channel_id, title, description, image, category_id, role_id):
        self.cursor.execute('''
        INSERT INTO ticket_panels (guild_id, channel_id, title, description, image, category_id, role_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (guild_id, channel_id, title, description, image, category_id, role_id))
        self.conn.commit()

    def delete_panel(self, panel_id):
        self.cursor.execute('DELETE FROM ticket_panels WHERE id = ?', (panel_id,))
        self.conn.commit()

    def fetch_panels(self, guild_id):
        self.cursor.execute('SELECT id, title FROM ticket_panels WHERE guild_id = ?', (guild_id,))
        return self.cursor.fetchall()

    def insert_ticket(self, guild_id, user_id, channel_id):
        self.cursor.execute('''
        INSERT INTO tickets (guild_id, user_id, channel_id, created_at, status)
        VALUES (?, ?, ?, ?, 'open')
        ''', (guild_id, user_id, channel_id, datetime.datetime.utcnow()))
        self.conn.commit()

    def fetch_open_ticket(self, guild_id, user_id):
        self.cursor.execute('''
        SELECT id FROM tickets WHERE guild_id = ? AND user_id = ? AND status =
        'open'
        ''', (guild_id, user_id))
        return self.cursor.fetchone()

    def fetch_ticket_by_channel(self, guild_id, channel_id):
        self.cursor.execute('''
        SELECT id FROM tickets WHERE guild_id = ? AND channel_id = ? AND status = 'open'
        ''', (guild_id, channel_id))
        return self.cursor.fetchone()

    def update_ticket_status(self, ticket_id, status):
        self.cursor.execute('''
        UPDATE tickets SET status = ? WHERE id = ?
        ''', (status, ticket_id))
        self.conn.commit()

    def fetch_category(self, guild_id):
        self.cursor.execute('''
        SELECT category_id FROM ticket_panels WHERE guild_id = ? LIMIT 1
        ''', (guild_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

def setup(bot):
    bot.add_cog(Ticket(bot))
