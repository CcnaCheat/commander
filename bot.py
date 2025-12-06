import discord
from discord.ext import commands
import os
import random

MP3_FOLDER = "mp3"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def play(ctx, filename: str = None):
    if ctx.author.voice is None:
        await ctx.send("❗ You need to be in a voice channel first.")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        vc = await channel.connect()
    else:
        vc = ctx.voice_client
        await vc.move_to(channel)

    # If no filename, pick random
    if filename is None:
        files = [f for f in os.listdir(MP3_FOLDER) if f.endswith(".mp3")]
        if not files:
            await ctx.send("❌ No MP3 files found in folder!")
            return
        filename = random.choice(files)

    # Full path
    path = os.path.join(MP3_FOLDER, filename)

    if not os.path.isfile(path):
        await ctx.send(f"❌ File `{filename}` not found!")
        return

    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=path))
    await ctx.send(f"▶️ Now playing `{filename}`!")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Stopped playing and left the voice channel.")
    else:
        await ctx.send("❌ I'm not in a voice channel!")

bot.run(os.getenv("DISCORD_TOKEN"))
