import discord
import wavelink
from wavelink.ext import spotify
from discord.ext import commands
import logging
from typing import Any, Dict, Union, Optional
from discord.enums import try_enum
import os
import datetime
import datetime as dt
import datetime
from discord.ui import Button
import typing as t
import requests
import re
from discord.ext.commands.errors import CheckFailure
import asyncio
import os
from wavelink import Player
import async_timeout
from PIL import Image, ImageDraw, ImageFont
import io
from io import BytesIO
import colorama
from colorama import Fore

LYRICS_URL = "https://some-random-api.ml/lyrics?title="
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"


class NotConnectedToVoice(CheckFailure):
    """User not connected to any voice channel"""

    pass


class PlayerNotConnected(CheckFailure):
    """Player not connected"""

    pass


class MustBeSameChannel(CheckFailure):
    """Player and user not in same channel"""

    pass


class NothingIsPlaying(CheckFailure):
    """Nothing is playing"""

    pass


class NotEnoughSong(CheckFailure):
    """Not enough songs in queue"""

    pass


class InvalidLoopMode(CheckFailure):
    """Invalid loop mode"""

    pass


class DisPlayer(Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue = asyncio.Queue()
        self.bound_channel = None
        self.track_provider = "yt"

    async def destroy(self) -> None:
        self.queue = None

        await super().stop()
        await super().disconnect()

    async def do_next(self) -> None:
        if self.is_playing():
            return

        timeout = int(os.getenv("DISMUSIC_TIMEOUT", 300))

        try:
            with async_timeout.timeout(timeout):
                track = await self.queue.get()
        except asyncio.TimeoutError:
            if not self.is_playing():
                await self.destroy()

            return

        self._source = track
        await self.play(track)
        self.client.dispatch("dismusic_track_start", self, track)
        await self.invoke_player()

    async def invoke_player(self, ctx: commands.Context = None) -> None:
        track = self.source

        if not track:
            raise NothingIsPlaying("Player is not playing anything.")

        embed = discord.Embed(title=track.title, url=track.uri, color=0x2f3136)
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(
            name=track.author,
            url=track.uri,
            icon_url=self.client.user.display_avatar.url,
        )
        try:
            embed.set_thumbnail(url=track.thumb)
        except AttributeError:
            embed.set_thumbnail(
                url=
          "https://media.discordapp.net/attachments/1066637418557624340/1068042323088379914/2491-couple-matching-1-2.gif"
            )

        embed.add_field(
            name="Length",
            value=f"{int(track.length // 60)}:{int(track.length % 60)}",
        )
        embed.add_field(name="Looping", value=self.loop)
        embed.add_field(name="Volume", value=self.volume)

        next_song = ""

        if self.loop == "CURRENT":
            next_song = self.source.title
        else:
            if len(self.queue._queue) > 0:
                next_song = self.queue._queue[0].title

        if next_song:
            embed.add_field(name="Next Song", value=next_song, inline=False)

        if not ctx:
            return await self.bound_channel.send(embed=embed)

        await ctx.send(embed=embed)


class Check:

    async def userInVoiceChannel(self, ctx, bot):
        """Check if the user is in a voice channel"""
        if ctx.author.voice:
            return True
        hacker5 = discord.Embed(
            title="Redox",
            description=
            f"<a:crossss:1131829269509709875> {ctx.author.mention} You are not connected in a voice channel",
            color=0x2f3136)
        hacker5.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        hacker5.timestamp = discord.utils.utcnow()
        await ctx.channel.send(embed=hacker5)
        return False

    async def botInVoiceChannel(self, ctx, bot):
        """Check if the bot is in a voice channel"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player.is_connected:
            return True
        hacker5 = discord.Embed(
            title="Redox",
            description=
            f"<a:crossss:1131829269509709875> {ctx.author.mention} I'm not connected in a voice channel",
            color=0x00FFED)
        hacker5.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        hacker5.timestamp = discord.utils.utcnow()
        await ctx.channel.send(embed=hacker5)
        return False

    async def botNotInVoiceChannel(self, ctx, bot):
        """Check if the bot is not in a voice channel"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if not player.is_connected:
            return True
        hacker5 = discord.Embed(
            title="Redox",
            description=
            f"<a:crossss:1131829269509709875> I'm already connected in a voice channel",
            color=0x00FFED)
        hacker5.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        hacker5.timestamp = discord.utils.utcnow()
        await ctx.channel.send(embed=hacker5)
        return False

    async def userAndBotInSameVoiceChannel(self, ctx, bot):
        """Check if the user and the bot are in the same voice channel"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ((bot.user.id in ctx.author.voice.channel.voice_states)
                and (ctx.author.id in ctx.author.voice.channel.voice_states)):
            return True
        hacker5 = discord.Embed(
            title="Redox",
            description=
            f"<a:crossss:1131829269509709875> You are not connected in the same voice channel that the bot",
            color=0x00FFED)
        hacker5.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        hacker5.timestamp = discord.utils.utcnow()
        await ctx.channel.send(embed=hacker5)
        return False

    async def botIsPlaying(self, ctx, bot):
        """Check if the bot is playing"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        if player.is_playing:
            return True
        hacker5 = discord.Embed(
            title="Redox",
            description=
            f"<a:crossss:1131829269509709875> There is currently no song to replay",
            color=0x00FFED)
        hacker5.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        hacker5.timestamp = discord.utils.utcnow()
        await ctx.channel.send(embed=hacker5)
        return False


__all__ = (
    "WavelinkError",
    "AuthorizationFailure",
    "LavalinkException",
    "LoadTrackError",
    "BuildTrackError",
    "NodeOccupied",
    "InvalidIDProvided",
    "ZeroConnectedNodes",
    "NoMatchingNode",
    "QueueException",
    "QueueFull",
    "QueueEmpty",
)


class WavelinkError(Exception):
    """Base WaveLink Exception"""


class InvalidEqPreset(commands.CommandError):
    pass


class AuthorizationFailure(WavelinkError):
    """Exception raised when an invalid password is provided toa node."""


class LavalinkException(WavelinkError):
    """Exception raised when an error occurs talking to Lavalink."""


class LoadTrackError(LavalinkException):
    """Exception raised when an error occurred when loading a track."""


class NoLyricsFound(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class BuildTrackError(LavalinkException):
    """Exception raised when a track is failed to be decoded and re-built."""

    def __init__(self, data):
        super().__init__(data["error"])


class NodeOccupied(WavelinkError):
    """Exception raised when node identifiers conflict."""


class InvalidTimeString(commands.CommandError):
    pass


class InvalidIDProvided(WavelinkError):
    """Exception raised when an invalid ID is passed somewhere in Wavelink."""


class ZeroConnectedNodes(WavelinkError):
    """Exception raised when an operation is attempted with nodes, when there are None connected."""


class InvalidRepeatMode(commands.CommandError):
    pass


class NoMatchingNode(WavelinkError):
    """Exception raised when a Node is attempted to be retrieved with a incorrect identifier."""


class QueueIsEmpty(commands.CommandError):
    """AtLeast Have  Queue"""


class QueueException(WavelinkError):
    """Base WaveLink Queue exception."""

    pass


class QueueFull(QueueException):
    """Exception raised when attempting to add to a full Queue."""

    pass


class QueueEmpty(QueueException):
    """Exception raised when attempting to retrieve from an empty Queue."""

    pass


VoiceChannel = Union[discord.VoiceChannel, discord.StageChannel]

logger: logging.Logger = logging.getLogger(__name__)


class TrackNotFound(commands.CommandError):
    pass


class Buttons(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

#<:volume_down:1056039813712707654>
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
     node = wavelink.NodePool.get_node()
     player = node.get_player(interaction.guild)

     if interaction.user.voice and player:
        if interaction.user.voice.channel == player.channel:
            return True
        else:
            await interaction.response.send_message('You must be in the same voice channel as the player to control this menu!', ephemeral=True)
            return False
     else:
        await interaction.response.send_message('There is no active player or you are not in a voice channel!', ephemeral=True)
        return False
    
    @discord.ui.button(emoji="<:Volume_Down:1238073243215331390>",
                       style=discord.ButtonStyle.grey,
                       row=0)
    async def volume_button(self, interaction: discord.Interaction,
                            button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | I am not connected to a voice channel.",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker,
                                                           ephemeral=True)
        if player.is_playing:
            await player.set_volume(50)
            hacker1 = discord.Embed(
                description=
                "<a:tickkk:1130730211382661171> | Successfully changed player volume to : `50`",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker1,
                                                           ephemeral=True)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:crossss:1131829269509709875> | I am not playing anything.",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker2,
                                                           ephemeral=True)

    @discord.ui.button(emoji="<:previous:1238100970634743868>",
                       style=discord.ButtonStyle.grey,
                       row=0)
    async def seek_button(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | I am not connected to a voice channel.",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker,
                                                           ephemeral=True)

        if player.is_playing:
            await player.seek(10 * 1000)
            hacker1 = discord.Embed(
                description=
                "<a:tickkk:1130730211382661171> | Seeked the current player to `10 seconds` .",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker1,
                                                           ephemeral=True)
        else:
            hacker2 = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | I am not playing anything.",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker2,
                                                           ephemeral=True)

    @discord.ui.button(emoji="<:StopMusic:1238073080421810218>",
                       style=discord.ButtonStyle.danger,
                       row=0)
    async def stop_button(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | I am not connected to a voice channel.",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker,
                                                           ephemeral=True)

        if player.is_playing:
            player.queue.clear()
            await player.stop()
            hacker1 = discord.Embed(
                description=
                f"<a:tickkk:1130730211382661171> | Destroyed the player.",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker1,
                                                           ephemeral=True)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:crossss:1131829269509709875> | I am not playing anything.",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker2,
                                                           ephemeral=True)

    @discord.ui.button(emoji="<:skip:1238091502396112958>",
                       style=discord.ButtonStyle.grey,
                       row=0)
    async def skip_button(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | I am not connected to a voice channel.",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker,
                                                           ephemeral=True)

        if player.is_playing:
            await player.stop()
            hacker1 = discord.Embed(
                description=
                "<a:tickkk:1130730211382661171> | Successfully Skipped the track .",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker1,
                                                           ephemeral=True)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:crossss:1131829269509709875> | I am not playing anything.",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker2,
                                                           ephemeral=True)

    @discord.ui.button(emoji="<:Volume_Up:1238073358269284423>",
                       style=discord.ButtonStyle.grey,
                       row=0)
    async def vol_button(self, interaction: discord.Interaction,
                         button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | I am not connected to a voice channel.",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker,
                                                           ephemeral=True)

        if player.is_playing:
            await player.set_volume(100)
            hacker1 = discord.Embed(
                description=
                "<a:tickkk:1130730211382661171> | Successfully changed player volume to : `100`",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker1,
                                                           ephemeral=True)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:crossss:1131829269509709875> | I am not playing anything.",
                color=0x00FFED)
            return await interaction.response.send_message(embed=hacker2,
                                                           ephemeral=True)

class Dropdown(discord.ui.Select):

  def __init__(self):
    options = [
      discord.SelectOption(label="Reset",
                           description="Clears all Filter",
                           emoji="<a:diamond:1106118913894387712>"),
      discord.SelectOption(label="Slowed",
                           description="Enables Slowed Filter",
                           emoji="<a:diamond:1106118913894387712>"),
      discord.SelectOption(label="Chipmunk",
                           description="Enables Chipmunk Filter",
                           emoji="<a:diamond:1106118913894387712>"),
      discord.SelectOption(label="Nightcore",
                           description="Enables Nightcore Filter",
                           emoji="<a:diamond:1106118913894387712>"),
      discord.SelectOption(label="Lofi",
                           description="Enables Lofi Filter",
                           emoji="<a:diamond:1106118913894387712>"),
      discord.SelectOption(label="8D",
                           description="Enables 8D Filter",
                           emoji="<a:diamond:1106118913894387712>"),
      discord.SelectOption(label="Karaoke",
                           description="Enables Karaoke Filter",
                           emoji="<a:diamond:1106118913894387712>"),
      discord.SelectOption(label="DeepBass",
                           description="Enables Deep Bass Filter",
                           emoji="<a:diamond:1106118913894387712>")
    ]
    super().__init__(placeholder="Select Filter",
                     options=options,
                     min_values=1,
                     max_values=1)

  async def callback(self, interaction: discord.Interaction):
    selected_filter = self.values[0]
    if selected_filter == "Reset":
      vc = interaction.guild.voice_client
      await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer.flat()),
                          seek=False)
    elif selected_filter == "Slowed":
      vc = interaction.guild.voice_client
      await vc.set_filter(
        wavelink.Filter(timescale=wavelink.Timescale(rate=0.9)), seek=False)

    elif selected_filter == "Chipmunk":
      vc = interaction.guild.voice_client
      await vc.set_filter(
        wavelink.Filter(timescale=wavelink.Timescale(rate=1.3)), seek=False)

    elif selected_filter == "Nightcore":
      vc = interaction.guild.voice_client
      await vc.set_filter(
        wavelink.Filter(timescale=wavelink.Timescale(speed=1.25, pitch=1.3)),
        seek=False)

    elif selected_filter == "Lofi":
      vc = interaction.guild.voice_client
      await vc.set_filter(
        wavelink.Filter(timescale=wavelink.Timescale(rate=0.8)), seek=False)

    elif selected_filter == "8D":
      vc = interaction.guild.voice_client
      await vc.set_filter(
        wavelink.Filter(rotation=wavelink.Rotation(speed=0.15)), seek=False)

    elif selected_filter == "Karaoke":
      vc = interaction.guild.voice_client
      await vc.set_filter(wavelink.Filter(karaoke=wavelink.Karaoke(
        level=0.9, mono_level=0.9, filter_band=220.0, filter_width=110.0)),
                          seek=False)

    elif selected_filter == "DeepBass":
      vc = interaction.guild.voice_client
      bands = [(0, 0.3), (1, 0.2), (2, 0.1), (3, 0.05), (4, -0.05), (5, -0.1),
               (6, -0.1), (7, -0.1), (8, -0.1), (9, -0.1), (10, -0.1),
               (11, -0.1), (12, -0.1), (13, -0.1), (14, -0.1)]
      await vc.set_filter(
        wavelink.Filter(
          equalizer=wavelink.Equalizer(name="Deepbass", bands=bands)))

    embed = discord.Embed(
      description=f"`{selected_filter}` **filter will be applied soon...**")
    await interaction.response.send_message(embed=embed, ephemeral=True)




class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.msg = None
        self.playlist = []
        self.user_timer = {}
        self.user_all_time = {}

    async def create_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host="node.raidenbot.xyz",
            port="5500",
            password="pwd",
            https=False,
            spotify_client=spotify.SpotifyClient(
                client_id="a48224141ca649079fbc5f443a6396ab",
                client_secret="a4008dc4c4994dab932e30a7e9ae16f3"))


    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.RED+"MADE BY RAVAN X VOID💝")
        await self.bot.loop.create_task(self.create_nodes())

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.identifier}> is now Ready!")

    @commands.command(name="play", usage="play <search>", aliases=[("p")])

    async def play(self, ctx: commands.Context, *, search: str):
        await ctx.defer()
        if not getattr(ctx.author, "voice", None):
            nv = discord.Embed(
                description=
                '<a:crossss:1131829269509709875> | You are not connected to a voice channel.',
                color=0x00FFED)
            await ctx.send(embed=nv)
            return
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player, self_deaf=True)
            embed = discord.Embed(
                description=
                f"Successfully Connected To {ctx.author.voice.channel.mention}",
                color=0xff0000)
            embed.timestamp = discord.utils.utcnow()

            await ctx.send(
                f"<a:tickkk:1130730211382661171> | Successfully Connected To {ctx.author.voice.channel.mention}"
            )
        else:
            vc: wavelink.Player = ctx.voice_client
            vc.chanctx = ctx.channel

        if 'https://open.spotify.com' in str(search):

            if vc.queue.is_empty and not vc.is_playing():

                track = await spotify.SpotifyTrack.search(query=search,
                                                          return_first=True)

                await vc.play(track)
                background = Image.open('ma.jpg').convert("RGBA")
                draw = ImageDraw.Draw(background)
                artist_name = f'{track.author}'
                song_title = f'{track}'
                album_name = f'Requested By: {ctx.author}'
                additional_text = f'{ round(track.duration / 60, 2)}'
                font_path = "sha.ttf"
                song_title_font = ImageFont.truetype(font_path, 80)
                artist_name_font = ImageFont.truetype(font_path, 50)
                album_name_font = ImageFont.truetype(font_path, 50)
                additional_text_font = ImageFont.truetype(font_path, 40)
                song_title_position = (500, 10)
                artist_name_position = (500, 110)
                album_name_position = (500, 180)
                additional_text_position = (1160, 360)
                white = (255, 255, 255) 
                artist_name_color = (255, 255, 0)
                album_name_color = (0, 255, 255)
                draw.text(song_title_position, song_title, font=song_title_font, fill=white)
                draw.text(artist_name_position, artist_name, font=artist_name_font, fill=artist_name_color)
                draw.text(album_name_position, album_name, font=album_name_font, fill=album_name_color)
                draw.text(additional_text_position, additional_text, font=additional_text_font, fill=white)
                draw.text((530,360), "0:00", font=additional_text_font, fill=white)
                response = requests.get(track.thumb)
                round_image = Image.open(BytesIO(response.content)).convert("RGBA")
                round_image_size = (360, 240)
                round_image = round_image.resize(round_image_size)
                background.paste(round_image, (50, 60), round_image)
                img_byte_array = io.BytesIO()
                background.save(img_byte_array, format='PNG')
                img_byte_array.seek(0)
                file = discord.File(img_byte_array, filename='image.png')
                view = Buttons()
                self.msg = await ctx.send(file=file,view=view)

            else:
                track = await spotify.SpotifyTrack.search(query=search,
                                                          return_first=True)
                await vc.queue.put_wait(track)
                background = Image.open('db/mu.png').convert("RGBA")
                draw = ImageDraw.Draw(background)
                song_title = f'Queue added : {track}'
                artist_name = f'{track.author}'
                album_name = f'Requested By: {ctx.author}'
                additional_text = f'Duration : { round(track.duration / 60, 2)} Minutes'
                font_path = "sha.ttf"
                song_title_font = ImageFont.truetype(font_path, 90)
                artist_name_font = ImageFont.truetype(font_path, 60)
                album_name_font = ImageFont.truetype(font_path, 60)
                additional_text_font = ImageFont.truetype(font_path, 60)
                song_title_position = (360, 20)
                artist_name_position = (360, 150)
                album_name_position = (360, 230)
                additional_text_position = (360, 340)
                white = (255, 255, 255) 
                artist_name_color = (255, 255, 0)
                album_name_color = (0, 255, 255)
                draw.text(song_title_position, song_title, font=song_title_font, fill=white)
                draw.text(artist_name_position, artist_name, font=artist_name_font, fill=artist_name_color)
                draw.text(album_name_position, album_name, font=album_name_font, fill=album_name_color)
                draw.text(additional_text_position, additional_text, font=additional_text_font, fill=white)
                response = requests.get(track.thumb)
                round_image = Image.open(BytesIO(response.content)).convert("RGBA")
                round_image_size = (300, 240)
                round_image = round_image.resize(round_image_size)
                background.paste(round_image, (20, 100), round_image)
                img_byte_array = io.BytesIO()
                background.save(img_byte_array, format='PNG')
                img_byte_array.seek(0)
                file = discord.File(img_byte_array, filename='image.png')
                await ctx.send(file=file)

        elif 'https://www.youtube.com/' in str(search):

            if vc.queue.is_empty and not vc.is_playing():

                track1 = await vc.node.get_tracks(query=search,cls=wavelink.Track)

                await vc.play(track1[0])
                url = f"{search}"
                video_id = url.split("=")[-1]

                background = Image.open('db/ma.jpg').convert("RGBA")
                draw = ImageDraw.Draw(background)
                song_title = f"{track1}"
                artist_name = f'none'
                album_name = f'Requested By: {ctx.author}'
                additional_text = f'0:00'
                font_path = "db/sha.ttf"
                song_title_font = ImageFont.truetype(font_path, 80)
                artist_name_font = ImageFont.truetype(font_path, 50)
                album_name_font = ImageFont.truetype(font_path, 50)
                additional_text_font = ImageFont.truetype(font_path, 40)
                song_title_position = (500, 10)
                artist_name_position = (500, 110)
                album_name_position = (500, 180)
                additional_text_position = (1160, 360)
                white = (255, 255, 255) 
                artist_name_color = (255, 255, 0)
                album_name_color = (0, 255, 255)
                draw.text(song_title_position, song_title, font=song_title_font, fill=white)
                draw.text(artist_name_position, artist_name, font=artist_name_font, fill=artist_name_color)
                draw.text(album_name_position, album_name, font=album_name_font, fill=album_name_color)
                draw.text(additional_text_position, additional_text, font=additional_text_font, fill=white)
                draw.text((530,360), "0:00", font=additional_text_font, fill=white)
                response = requests.get(f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg")
                round_image = Image.open(BytesIO(response.content)).convert("RGBA")
                round_image_size = (360, 240)
                round_image = round_image.resize(round_image_size)
                background.paste(round_image, (50, 60), round_image)
                img_byte_array = io.BytesIO()
                background.save(img_byte_array, format='PNG')
                img_byte_array.seek(0)
                file = discord.File(img_byte_array, filename='image.png')
                view = Buttons()
                self.msg = await ctx.send(file=file,view=view)

            else:
                track1 = await vc.node.get_tracks(query=search,
                                                  cls=wavelink.Track)
                await vc.queue.put_wait(track1[0])
                background = Image.open('mu.png').convert("RGBA")
                draw = ImageDraw.Draw(background)
                url = f"{search}"
                video_id = url.split("=")[-1]
                song_title = f'Queue added : {track1}'
                artist_name = f'None'
                album_name = f'Requested By: {ctx.author}'
                additional_text = 'Duration : None'
                font_path = "sha.ttf"
                song_title_font = ImageFont.truetype(font_path, 90)
                artist_name_font = ImageFont.truetype(font_path, 60)
                album_name_font = ImageFont.truetype(font_path, 60)
                additional_text_font = ImageFont.truetype(font_path, 60)
                song_title_position = (360, 20)
                artist_name_position = (360, 150)
                album_name_position = (360, 230)
                additional_text_position = (360, 340)
                white = (255, 255, 255) 
                artist_name_color = (255, 255, 0)
                album_name_color = (0, 255, 255)
                draw.text(song_title_position, song_title, font=song_title_font, fill=white)
                draw.text(artist_name_position, artist_name, font=artist_name_font, fill=artist_name_color)
                draw.text(album_name_position, album_name, font=album_name_font, fill=album_name_color)
                draw.text(additional_text_position, additional_text, font=additional_text_font, fill=white)
                response = requests.get(f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg")
                round_image = Image.open(BytesIO(response.content)).convert("RGBA")
                round_image_size = (300, 240)
                round_image = round_image.resize(round_image_size)
                background.paste(round_image, (20, 100), round_image)
                img_byte_array = io.BytesIO()
                background.save(img_byte_array, format='PNG')
                img_byte_array.seek(0)
                file = discord.File(img_byte_array, filename='image.png')
                await ctx.send(file=file)

        else:

            if vc.queue.is_empty and not vc.is_playing():

                track2 = await wavelink.YouTubeTrack.search(query=search,
                                                            return_first=True)

                await vc.play(track2)
                background = Image.open('ma.jpg').convert("RGBA")
                draw = ImageDraw.Draw(background)
                song_title = f'{track2}'
                artist_name = f'{track2.author}'
                album_name = f'Requested By: {ctx.author}'
                additional_text = f'{ round(track2.duration / 60, 2)}'
                font_path = "sha.ttf"
                song_title_font = ImageFont.truetype(font_path, 80)
                artist_name_font = ImageFont.truetype(font_path, 50)
                album_name_font = ImageFont.truetype(font_path, 50)
                additional_text_font = ImageFont.truetype(font_path, 40)
                song_title_position = (500, 10)
                artist_name_position = (500, 110)
                album_name_position = (500, 180)
                additional_text_position = (1160, 360)
                white = (255, 255, 255) 
                artist_name_color = (255, 255, 0)
                album_name_color = (0, 255, 255)
                draw.text(song_title_position, song_title, font=song_title_font, fill=white)
                draw.text(artist_name_position, artist_name, font=artist_name_font, fill=artist_name_color)
                draw.text(album_name_position, album_name, font=album_name_font, fill=album_name_color)
                draw.text(additional_text_position, additional_text, font=additional_text_font, fill=white)
                draw.text((530,360), "0:00", font=additional_text_font, fill=white)
                response = requests.get(track2.thumb)
                round_image = Image.open(BytesIO(response.content)).convert("RGBA")
                round_image_size = (360, 280)
                round_image = round_image.resize(round_image_size)
                background.paste(round_image, (50, 60), round_image)
                img_byte_array = io.BytesIO()
                background.save(img_byte_array, format='PNG')
                img_byte_array.seek(0)
                file = discord.File(img_byte_array, filename='image.png')
                view = Buttons()
                self.msg = await ctx.send(file=file,view=view)
            else:

                track2 = await wavelink.YouTubeTrack.search(query=search,
                                                            return_first=True)
                await vc.queue.put_wait(track2)
                background = Image.open('mu.png').convert("RGBA")
                draw = ImageDraw.Draw(background)
                song_title = f'Queue added : {track2}'
                artist_name = f'{track2.author}'
                album_name = f'Requested By: {ctx.author}'
                additional_text = f'Duration : { round(track2.duration / 60, 2)} Minutes'
                font_path = "sha.ttf"
                song_title_font = ImageFont.truetype(font_path, 90)
                artist_name_font = ImageFont.truetype(font_path, 60)
                album_name_font = ImageFont.truetype(font_path, 60)
                additional_text_font = ImageFont.truetype(font_path, 60)
                song_title_position = (360, 20)
                artist_name_position = (360, 150)
                album_name_position = (360, 230)
                additional_text_position = (360, 340)
                white = (255, 255, 255) 
                artist_name_color = (255, 255, 0)
                album_name_color = (0, 255, 255)
                draw.text(song_title_position, song_title, font=song_title_font, fill=white)
                draw.text(artist_name_position, artist_name, font=artist_name_font, fill=artist_name_color)
                draw.text(album_name_position, album_name, font=album_name_font, fill=album_name_color)
                draw.text(additional_text_position, additional_text, font=additional_text_font, fill=white)
                response = requests.get(track2.thumb)
                round_image = Image.open(BytesIO(response.content)).convert("RGBA")
                round_image_size = (300, 240)
                round_image = round_image.resize(round_image_size)
                background.paste(round_image, (20, 100), round_image)
                img_byte_array = io.BytesIO()
                background.save(img_byte_array, format='PNG')
                img_byte_array.seek(0)
                file = discord.File(img_byte_array, filename='image.png')
                await ctx.send(file=file)



    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track,
                                    reason):

        if not player.queue.is_empty:
            ctx = player.chanctx
            new_song = player.queue.get()
            await player.play(new_song)

            if hasattr(new_song, 'thumb'):
                background = Image.open('ma.jpg').convert("RGBA")
                draw = ImageDraw.Draw(background)
                song_title = f'{new_song}'
                artist_name = f'{new_song.author}'
               # album_name = f'Requested By: {track.album}'
                additional_text = f'{ round(new_song.duration / 60, 2)}'
                font_path = "sha.ttf"
                song_title_font = ImageFont.truetype(font_path, 80)
                artist_name_font = ImageFont.truetype(font_path, 50)
                album_name_font = ImageFont.truetype(font_path, 50)
                additional_text_font = ImageFont.truetype(font_path, 40)
                song_title_position = (500, 10)
                artist_name_position = (500, 150)
                album_name_position = (500, 180)
                additional_text_position = (1160, 360)
                white = (255, 255, 255) 
                artist_name_color = (255, 255, 0)
                album_name_color = (0, 255, 255)
                draw.text(song_title_position, song_title, font=song_title_font, fill=white)
                draw.text(artist_name_position, artist_name, font=artist_name_font, fill=artist_name_color)
                #draw.text(album_name_position, album_name, font=album_name_font, fill=album_name_color)
                draw.text(additional_text_position, additional_text, font=additional_text_font, fill=white)
                draw.text((530,360), "0:00", font=additional_text_font, fill=white)
                response = requests.get(new_song.thumb)
                round_image = Image.open(BytesIO(response.content)).convert("RGBA")
                round_image_size = (350, 240)
                round_image = round_image.resize(round_image_size)
                background.paste(round_image, (50, 60), round_image)
                img_byte_array = io.BytesIO()
                background.save(img_byte_array, format='PNG')
                img_byte_array.seek(0)
                file = discord.File(img_byte_array, filename='image.png')
               
                view = Buttons()
                await self.msg.edit(view=None)
                self.msg = await ctx.send(file=file,view=view)
            else:
              background = Image.open('ma.jpg').convert("RGBA")
              draw = ImageDraw.Draw(background)
              song_title = f'{new_song}'
              artist_name = f'{new_song.author}'
              #album_name = f'Requested By: {track.album}'
              additional_text = f'{ round(new_song.duration / 60, 2)}'
              font_path = "sha.ttf"
              song_title_font = ImageFont.truetype(font_path, 80)
              artist_name_font = ImageFont.truetype(font_path, 50)
              album_name_font = ImageFont.truetype(font_path, 50)
              additional_text_font = ImageFont.truetype(font_path, 40)
              song_title_position = (500, 10)
              artist_name_position = (500, 110)
              album_name_position = (500, 180)
              additional_text_position = (1160, 360)
              white = (255, 255, 255) 
              artist_name_color = (255, 255, 0)
              album_name_color = (0, 255, 255)
              draw.text(song_title_position, song_title, font=song_title_font, fill=white)
              draw.text(artist_name_position, artist_name, font=artist_name_font, fill=artist_name_color)
             # draw.text(album_name_position, album_name, font=album_name_font, fill=album_name_color)
              draw.text(additional_text_position, additional_text, font=additional_text_font, fill=white)
              draw.text((530,360), "0:00", font=additional_text_font, fill=white)
              response = requests.get(new_song.thumb)
              round_image = Image.open(BytesIO(response.content)).convert("RGBA")
              round_image_size = (360, 240)
              round_image = round_image.resize(round_image_size)
              background.paste(round_image, (50, 60), round_image)
              img_byte_array = io.BytesIO()
              background.save(img_byte_array, format='PNG')
              img_byte_array.seek(0)
              file = discord.File(img_byte_array, filename='image.png')
             
              view = Buttons()
             
              await self.msg.edit(view=None)
              self.msg = await ctx.send(file=file,view=view)
        else:
          view = discord.ui.View()
          btn = discord.ui.Button(style=discord.ButtonStyle.link,label="Invite Me",url="https://discord.com/oauth2/authorize?client_id=1126351590064930847&permissions=1239031351480&scope=bot")
          btns = discord.ui.Button(style=discord.ButtonStyle.link,label="Support Server",url="https://discord.com/invite/5SUKAB7n93")
          view.add_item(btn)
          view.add_item(btns)
          await self.msg.edit(view=None)
          await self.msg.reply(embed = discord.Embed(description="**🎶 Queue has ended! Thanks for listening. I'm leaving the voice channel now. 🎶**"),view=view)
          await player.disconnect()
    @commands.command(name="connect",
                      help="connect to your channel .",
                      aliases=["join", "j", "jvc"],
                      usage="connect [channel]")


    @commands.cooldown(1, 5, commands.BucketType.user)
    async def connect(self,
                      ctx: commands.Context,
                      *,
                      channel: discord.VoiceChannel = None):
        """Connects to a voice channel."""
        if not getattr(ctx.author, "voice", None):
            nv = discord.Embed(
                description=
                f'<a:crossss:1131829269509709875> | You are not connected to a voice channel.',
                color=0x00FFED)
            await ctx.send(embed=nv)
            return
        if channel is None:
            channel = ctx.author.voice.channel
        elif ctx.voice_client:
            av = discord.Embed(
                description=
                f"<a:crossss:1131829269509709875> | I am already connected to a voice channel.",
                color=0x00FFED)
            await ctx.send(embed=av)
            return
        vc: wavelink.Player = await channel.connect(cls=wavelink.Player,
                                                    self_deaf=True)
        sc = discord.Embed(
            description=
            f"<a:tickkk:1130730211382661171> | Successfully connected to {channel.mention}.",
            color=0x00FFED)
        await ctx.send(embed=sc)

    @commands.command(name="disconnect",
                      usage="disconnect [channel]",
                      aliases=[("leave")])


    async def leave_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You are not connected to a voice channel.",
                color=0x00FFED)

            #hacker.set_thumbnail(url = f"{ctx.author.avatar}")

            return await ctx.reply(embed=hacker)

        await player.disconnect()
        hacker1 = discord.Embed(
            description=
            f"<a:tickkk:1130730211382661171> | Successfully disconnected from {ctx.author.voice.channel.mention}",
            color=0x00FFED)

        await ctx.send(embed=hacker1)

    @commands.command(name="stop", usage="stop")


    async def stop_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You are not connected to a voice channel.",
                color=0x00FFED)

            return await ctx.reply(embed=hacker)

        if player.is_playing:
            player.queue.clear()
            await player.stop()
            hacker1 = discord.Embed(
                description=
                f"<a:tickkk:1130730211382661171> | Destroyed the player.",
                color=0x00FFED)

            await ctx.send(embed=hacker1)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:crossss:1131829269509709875> | I am not playing anything.",
                color=0x00FFED)

            #hacker2.set_thumbnail(url = f"{ctx.author.avatar}")

            return await ctx.reply(embed=hacker2)

    @commands.command(name="skip", usage="skip", aliases=[("s")])


    async def skip_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You are not connected to a voice channel.",
                color=0x00FFED)
            return await ctx.reply(embed=hacker)

        if player.is_playing:
            await player.stop()
            hacker1 = discord.Embed(
                description=
                f"<a:tickkk:1130730211382661171> | Successfully Skipped the track .",
                color=0x00FFED)

            await ctx.send(embed=hacker1)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:crossss:1131829269509709875> | I am not playing anything.",
                color=0x00FFED)
            return await ctx.reply(embed=hacker2)

    @commands.command(name="pause", usage="pause")


    async def pause_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You are not connected to a voice channel.",
                color=0x00FFED)
            hacker.set_footer(text=f"Requested By {ctx.author}",
                              icon_url=f"{ctx.author.avatar}")
            #hacker.set_thumbnail(url = f"{ctx.author.avatar}")

            return await ctx.reply(embed=hacker)

        if not player.is_paused():
            if player.is_playing():
                await player.pause()
                hacker1 = discord.Embed(
                    description=
                    f"<a:tickkk:1130730211382661171> | Successfully paused the player .",
                    color=0x00FFED)
                view = discord.ui.View()
                view = Buttons()
                view.add_item(Dropdown())
                await ctx.send(embed=hacker1)
            else:
                hacker2 = discord.Embed(
                    description=
                    f"<a:crossss:1131829269509709875> | I am not playing anything.",
                    color=0x00FFED)
                return await ctx.reply(embed=hacker2)
        else:
            hacker3 = discord.Embed(
                description=
                f"<a:crossss:1131829269509709875> | Player is already paused .",
                color=0x00FFED)

            return await ctx.reply(embed=hacker3)

    @commands.command(name="resume", usage="resume")


    async def resume_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You are not connected to a voice channel.",
                color=0x00FFED)


            return await ctx.reply(embed=hacker)

        if player.is_paused():
            await player.resume()
            hacker1 = discord.Embed(
                description=
                f"<a:tickkk:1130730211382661171> | Successfully resumed the player .",
                color=0x00FFED)

            await ctx.send(embed=hacker1)
        else:
            hacker3 = discord.Embed(
                description=
                f"<a:crossss:1131829269509709875> | Player is already resumed .",
                color=0x00FFED)

            return await ctx.reply(embed=hacker3)



    @commands.group(name="bassboost",
                    invoke_without_command=True,
                    aliases=['bass'])


    async def _bass(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_bass.command(name="enable", aliases=[("on")])


    async def boost_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if vc is None:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You are not connected to a voice channel.",
                color=0x00FFED)
            hacker.set_footer(text=f"Requested By {ctx.author}",
                              icon_url=f"{ctx.author.avatar}")
            #hacker.set_thumbnail(url = f"{ctx.author.avatar}")

            return await ctx.reply(embed=hacker)
        bands = [(0, 0.2), (1, 0.15), (2, 0.1), (3, 0.05), (4, 0.0),
                 (5, -0.05), (6, -0.1), (7, -0.1), (8, -0.1), (9, -0.1),
                 (10, -0.1), (11, -0.1), (12, -0.1), (13, -0.1), (14, -0.1)]
        await vc.set_filter(wavelink.Filter(
            equalizer=wavelink.Equalizer(name="MyOwnFilter", bands=bands)),
                            seek=True)
        hacker4 = discord.Embed(
            description=
            "<a:tickkk:1130730211382661171> | Successfully enabled `bass boost` .",
            color=0x00FFED)

        await ctx.reply(embed=hacker4)

    @_bass.command(name="disable", aliases=[("off")])
    @commands.has_permissions(administrator=False)


    async def rmvboost_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            description=
            "<a:tickkk:1130730211382661171> | Successfully disabled `bass boost` .",
            color=0x00FFED)
        await ctx.reply(embed=hacker4)

    @commands.hybrid_command(name="move", usage="move <VoiceChannel>",help="Moves the bot to the specified voice channel.")


    async def move_to(self, ctx, channel: discord.VoiceChannel) -> None:
        await ctx.guild.change_voice_state(channel=channel)
        hacker4 = discord.Embed(
            description=f"Moving to voice channel:: {channel.id} .",
            color=0x00FFED)

        await ctx.send(embed=hacker4)

    @commands.command(name="volume", usage="volume <vol>", aliases=[("vol")])
    @commands.guild_only()


    @commands.cooldown(1, 5, commands.BucketType.member)
    async def volume(self, ctx, volume):

        if not await Check().userInVoiceChannel(ctx, self.bot): return
        if not await Check().botInVoiceChannel(ctx, self.bot): return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        if ((not volume.isdigit()) or (int(volume)) < 0
                or (int(volume) > 150)):
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | Volume Must Be 0 To 150 .",
                color=0x00FFED)
            hacker.set_footer(text=f"Requested By {ctx.author}",
                              icon_url=f"{ctx.author.avatar}")
            #hacker.set_thumbnail(url = f"{ctx.author.avatar}")

            return await ctx.send(embed=hacker)
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        volume = int(volume)
        await player.set_volume(volume)
        hacker4 = discord.Embed(
            description=
            f"<a:tickkk:1130730211382661171> | Successfully changed player volume to : `{volume}%`",
            color=0xff0000)

        await ctx.send(embed=hacker4)

    @commands.command(name="nowplaying", usage="nowplaying", aliases=['now',])


    async def playing(self, ctx):
        if not ctx.voice_client:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | I am not connected to a voice channel.",
                color=0x00FFED)
            hacker.set_footer(text=f"Requested By {ctx.author}",
                              icon_url=f"{ctx.author.avatar}")

            return await ctx.send(embed=hacker)
        elif not getattr(ctx.author.voice, "channel", None):
            hacker1 = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You are not connected to a voice channel.",
                color=0x00FFED)
            hacker1.set_footer(text=f"Requested By {ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            hacker1.set_thumbnail(url=f"{ctx.author.avatar}")
            hacker1.timestamp = discord.utils.utcnow()
            return await ctx.send(embed=hacker1)
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            hacker1 = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | I am not playing anything .",
                color=0x00FFED)
            hacker1.set_footer(text=f"Requested By {ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            hacker1.set_thumbnail(url=f"{ctx.author.avatar}")
            hacker1.timestamp = discord.utils.utcnow()
            return await ctx.send(embed=hacker1)

        em = discord.Embed(
            description=f"[{vc.track}](https://discord.com/invite/CCYef4Ad4M)",
            color=0x00FFED)

        em.add_field(name="<:invitesss:1125056655567101972> Song By",
                     value=f"`{vc.track.author}`")
        em.add_field(
            name="<:icons_clock:1125056773640949823> Duration",
            value=f"`❯ {datetime.timedelta(seconds=vc.track.length)}`")
        em.set_footer(text=f"Requested By {ctx.author}",
                      icon_url=f"{ctx.author.avatar}")
        em.set_author(name="NOW PLAYING", icon_url=f"{ctx.author.avatar}")
        em.set_thumbnail(url=f"{ctx.author.avatar}")
        em.timestamp = discord.utils.utcnow()
        return await ctx.send(embed=em)

    @commands.command(name="shuffle", usage="shuffle", aliases=[("shuff")])


    async def shuffle(self, ctx):
        if not ctx.voice_client:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | Not connected to a voice channel.",
                color=0x00FFED)


            return await ctx.send(embed=hacker)
        elif not getattr(ctx.author.voice, "channel", None):
            hacker1 = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You are not connected to a voice channel.",
                color=0x00FFED)

            return await ctx.send(embed=hacker1)
        else:
            vc: wavelink.Player = ctx.voice_client

        copy = vc.queue.copy()
        random.shuffle(copy)
        vc.queue = copy
        hacker2 = discord.Embed(
            description=
            "<a:tickkk:1130730211382661171> | Successfully shuffled the current queue .",
            color=0x00FFED)
        await ctx.send(embed=hacker2)

    @commands.command(name="pull", usage="pull <index>")


    async def pull(self, ctx, index: int):
        if not ctx.voice_client:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | Not connected to a voice channel.",
                color=0x00FFED)

            return await ctx.send(embed=hacker)
        elif not getattr(ctx.author.voice, "channel", None):
            hacker1 = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You are not connected to a voice channel.",
                color=0x00FFED)
            return await ctx.send(embed=hacker1)
        else:
            vc: wavelink.Player = ctx.voice_client

        if index > len(vc.queue) or index < 1:
            hacker2 = discord.Embed(
                description=
                f"<a:crossss:1131829269509709875> | Must Be Between 1 And {len(vc.queue)} .",
                color=0x00FFED)
            return await ctx.reply(embed=hacker2)

        removed = vc.queue.pop(index - 1)
        hacker3 = discord.Embed(
            description=
            f"<a:tickkk:1130730211382661171> | Successfully pulled out `{removed.title}` From Queue .",
            color=0x00FFED)
        await ctx.send(embed=hacker3)

    @commands.group(name="queue", invoke_without_command=True, aliases=['q'])


    async def _queue(self, ctx):
        if not ctx.voice_client:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You are not connected to a voice channel.",
                color=0x00FFED)


            return await ctx.reply(embed=hacker)
        elif not getattr(ctx.author.voice, "channel", None):
            hacker1 = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You need to join a voice channel to play something .",
                color=0x00FFED)
            return await ctx.send(embed=hacker1)
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty:
            hacker3 = discord.Embed(
                description=
                f"<a:crossss:1131829269509709875> | No songs in queue .",
                color=0x00FFED)
            hacker3.set_footer(text=f"Requested By {ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            # hacker3.set_thumbnail(url = f"{ctx.author.avatar}")
            hacker3.timestamp = discord.utils.utcnow()
            return await ctx.send(embed=hacker3)
        hacker4 = discord.Embed(title="Music | Queue", color=0x00FFED)
        hacker4.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker4.set_thumbnail(url=f"{ctx.author.avatar}")

        copy = vc.queue.copy()
        count = 0
        for song in copy:
            count += 1
            hacker4.add_field(name=f"Position : {count}",
                              value=f"[{song.title}](https://discord.com/invite/CCYef4Ad4M)")
        return await ctx.send(embed=hacker4)

    @_queue.command(name="clear", aliases=[("c")])


    async def _clear(self, ctx):
        if not ctx.voice_client:
            hacker = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | Not connected to a voice channel.",
                color=0x00FFED)


            return await ctx.send(embed=hacker)
        elif not getattr(ctx.author.voice, "channel", None):
            hacker1 = discord.Embed(
                description=
                "<a:crossss:1131829269509709875> | You are not connected to a voice channel.",
                color=0x00FFED)

            return await ctx.send(embed=hacker1)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.queue.clear()
        hacker3 = discord.Embed(
            description=
            f"<a:tickkk:1130730211382661171> | Successfully Clears The current Queue .",
            color=0x00FFED)
        hacker3.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        return await ctx.send(embed=hacker3)

    @commands.command(name="seek", aliases=["sk"], usage="seek")


    async def seek_command(self, ctx, position: str):
        node = wavelink.NodePool.get_node()
        player: Player = node.get_player(ctx.guild)

        if not (match := re.match(TIME_REGEX, position)):
            raise InvalidTimeString

        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        await player.seek(secs * 1000)
        hacker3 = discord.Embed(
            description=
            f"<a:tickkk:1130730211382661171> | Successfully Seeked the current player to {secs} .",
            color=0x00FFED)
        await ctx.reply(embed=hacker3)
async def setup(bot):
    await bot.add_cog(Music(bot))