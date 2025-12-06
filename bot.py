import discord
from discord.ext import commands
import os
import random

MP3_FOLDER = "mp3"

intents = discord.Intents.default()
intents.message_content = True  # You already enabled this in the portal

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def play(ctx, filename: str = None):
    print(f"[DEBUG] !play called by {ctx.author}")

    if ctx.author.voice is None:
        await ctx.send("❌ You need to be in a voice channel first.")
        return

    channel = ctx.author.voice.channel
    vc = ctx.voice_client

    if vc is None:
        print(f"[DEBUG] Connecting to {channel}")
        vc = await channel.connect()
    elif vc.channel != channel:
        print(f"[DEBUG] Moving to {channel}")
        await vc.move_to(channel)

    if filename is None:
        files = [f for f in os.listdir(MP3_FOLDER) if f.lower().endswith(".mp3")]
        if not files:
            await ctx.send("❌ No MP3 files found!")
            return
        filename = random.choice(files)
        await ctx.send(f"🎲 Random track → `{filename}`")
    else:
        if not filename.lower().endswith(".mp3"):
            filename += ".mp3"

    path = os.path.join(MP3_FOLDER, filename)
    if not os.path.isfile(path):
        await ctx.send(f"❌ File `{filename}` not found!")
        return

    if vc.is_playing():
        vc.stop()

    print(f"[DEBUG] Playing {path}")
    try:
        source = discord.FFmpegPCMAudio(path, before_options="-nostdin")
        vc.play(source, after=lambda e: print("Finished playing" if not e else f"Error: {e}"))
        await ctx.send(f"▶️ Now playing `{filename}`")
    except Exception as e:
        print(f"[ERROR] Failed to play: {e}")
        await ctx.send(f"❌ Error playing file: {e}")

@bot.command()
async def stop(ctx):
    vc = ctx.voice_client
    if vc and vc.is_connected():
        await vc.disconnect()
        await ctx.send("⏹️ Stopped and disconnected.")
    else:
        await ctx.send("❌ Not in a voice channel!")

bot.run(os.getenv("DISCORD_TOKEN"))
