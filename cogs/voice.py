import nextcord
from nextcord.ext import commands
from core.audio.voice_recorder import VoiceRecorder
import logging

logger = logging.getLogger(__name__)

class Voice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.recorder = VoiceRecorder()
        self.active_recordings = set()
        logger.info("✅ Voice cog initialized")

    @commands.command()
    async def join(self, ctx):
        if not ctx.author.voice:
            return await ctx.send("❌ You're not in a voice channel!")
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"✅ Joined {channel.name}")

    @commands.command(aliases=["forcejoin"])
    async def force_join(self, ctx):
        if not ctx.author.voice:
            return await ctx.send("❌ You're not in a voice channel!")
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        await channel.connect()
        await ctx.send(f"✅ Force joined {channel.name}")

    @commands.command()
    async def record(self, ctx, seconds: int = 5):
        if not ctx.voice_client:
            return await ctx.send("❌ I'm not in a voice channel!")
        if ctx.channel.id in self.active_recordings:
            return await ctx.send("❌ Already recording in this channel!")
        if seconds < 5 or seconds > 60:
            return await ctx.send("❌ Please specify 5–60 seconds!")

        self.active_recordings.add(ctx.channel.id)
        try:
            await ctx.send(f"🔴 Recording {seconds} seconds...")
            transcription = await self.recorder.record_and_transcribe(seconds)
            await ctx.send(f"💬 Transcription:\n```{transcription}```")
        except Exception as e:
            await ctx.send(f"❌ Recording failed: {str(e)}")
        finally:
            self.active_recordings.discard(ctx.channel.id)

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            self.recorder.cleanup()
            await ctx.voice_client.disconnect()
            await ctx.send("✅ Left voice channel")
        else:
            await ctx.send("❌ I'm not in a voice channel!")

# ✅ PROPER async setup function for nextcord.ext.commands
async def setup(bot: commands.Bot):
    await bot.add_cog(Voice(bot))
    logging.info("✅ Voice cog successfully added")
