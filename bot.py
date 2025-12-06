import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from elevenlabs import generate, ElevenLabs

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
client = ElevenLabs(api_key=ELEVEN_API_KEY)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def say(ctx, *, text):
    # User must be in voice channel
    if ctx.author.voice is None:
        await ctx.send("❗ Join a voice channel first.")
        return

    channel = ctx.author.voice.channel

    # Connect to channel
    if ctx.voice_client is None:
        vc = await channel.connect()
    else:
        vc = ctx.voice_client
        await vc.move_to(channel)

    await ctx.send("🎤 Generating voice...")

    # ElevenLabs TTS
    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=text,
        output_format="mp3_44100_128"
    )

    # Save MP3
    audio_path = "response.mp3"
    with open(audio_path, "wb") as f:
        f.write(audio)

    # Play it in Discord
    vc.play(discord.FFmpegPCMAudio(audio_path))

    await ctx.send(f"🎧 Speaking in voice channel with your custom voice!")

bot.run(os.getenv("DISCORD_TOKEN"))
