import discord
from discord.ext import commands
import os
import random

MP3_FOLDER = "mp3"

# Use only default intents (no privileged intents needed)
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def play(ctx, filename: str = None):
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("❗ You need to be in a voice channel first.")
        return

    channel = ctx.author.voice.channel

    # Connect or move to the voice channel
    vc = ctx.voice_client
    if vc is None:
        try:
            vc = await channel.connect()
        except discord.ClientException:
            await ctx.send("❌ Already connected somewhere else!")
            return
        except discord.errors.Forbidden:
            await ctx.send("❌ I don't have permission to join the voice channel!")
            return
    elif vc.channel != channel:
        await vc.move_to(channel)

    # Choose a file if none specified
    if filename is None:
        files = [f for f in os.listdir(MP3_FOLDER) if f.endswith(".mp3")]
        if not files:
            await ctx.send("❌ No MP3 files found!")
            return
        filename = random.choice(files)

    path = os.path.join(MP3_FOLDER, filename)
    if not os.path.isfile(path):
        await ctx.send(f"❌ File `{filename}` not found!")
        return

    # Stop any currently playing audio
    if vc.is_playing():
        vc.stop()

    # Play the file
    # With this (more reliable):
    source = discord.FFmpegPCMAudio(path, executable="ffmpeg")
    vc.play(source, after=lambda e: print(f"Player error: {e}" if e else None))
    await ctx.send(f"▶️ Now playing `{filename}`!")

@bot.command()
async def stop(ctx):
    vc = ctx.voice_client
    if vc and vc.is_connected():
        await vc.disconnect()
        await ctx.send("⏹️ Stopped playing and left the voice channel.")
    else:
        await ctx.send("❌ I'm not in a voice channel!")

bot.run(os.getenv("DISCORD_TOKEN"))
