# Base
import logging
import os
import asyncio

# Third party
from dotenv import load_dotenv

# Discord
import discord
from discord.ext import commands

# Ours
from youtube import download

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

member_to_themes = {}

class AnnouncerBot(commands.Bot):
    """
    Announcer Bot
    """

    async def on_ready(self):
        print(f"{self.user} connected to Discord's API.")

        print("Guilds:")
        for guild in self.guilds:
            print(guild)

        print("Voice Clients:")
        for vc in self.voice_clients:
            print(vc)

    async def on_voice_state_update(self, member, before, after):
        # Don't do anything if it's the bot
        if member == self.user:
            return

        # A user joined the voice channel
        if before.channel == None and after.channel != None:
            # If member doesn't have theme, don't do anything
            if member.id not in member_to_themes:
                return

            # Lookup member's theme song
            theme_song = member_to_themes[member.id]
            print(f"Playing {theme_song}")

            # Join voice channel if not already in it
            channel_to_join = after.channel
            if channel_to_join not in self.voice_clients:
                voice_client = await channel_to_join.connect()

            # Play theme song
            audio_source = discord.FFmpegPCMAudio(theme_song)
            if not voice_client.is_playing():
                voice_client.play(audio_source)

bot = AnnouncerBot(command_prefix='$ ')

@bot.command(name='hello')
async def command_hello_world(ctx):
    await ctx.send("hello world")

@bot.command(name='theme')
async def command_theme(ctx, theme_song_name, youtube_url):
    # Who submitted the command
    member = ctx.author.id
    theme_song_name = theme_song_name + ".mp3"
    member_to_themes[member] = theme_song_name

    print(f"Downloading {youtube_url} as {theme_song_name}")

    download(theme_song_name, youtube_url)

bot.run(DISCORD_TOKEN)
