from nextcord.ext import commands
import nextcord
import youtube_dl
import asyncio
import logging


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ""


ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    "source_address": "0.0.0.0",
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source,  data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.ytdl = youtube_dl.YoutubeDL(
            {'format': 'bestaudio', 'noplaylist': 'True'})
        self.ytdl_cache = {}
        logging.info("Music cog loaded!")

    @nextcord.slash_command(description="Use this to play some music!")
    async def play(self, interaction: nextcord.Interaction, url: str) -> None:
        if not self.voice:
            self.voice = await interaction.author.voice.channel.connect()
        async with interaction.channel.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            self.queue.append(player)
        await interaction.response.send_message("Added to queue")

    @nextcord.slash_command(description="Use this to skip the current song!")
    async def skip(self, interaction: nextcord.Interaction) -> None:
        self.voice.stop()
        await interaction.response.send_message("Skipped song")

    @nextcord.slash_command(description="Use this to stop the music!")
    async def stop(self, interaction: nextcord.Interaction) -> None:
        self.voice.stop()
        self.queue.clear()
        await interaction.response.send_message("Stopped music")

    @nextcord.slash_command(description="Use this to pause the music!")
    async def pause(self, interaction: nextcord.Interaction) -> None:
        self.voice.pause()
        await interaction.response.send_message("Paused music")

    @nextcord.slash_command(description="Use this to resume the music!")
    async def resume(self, interaction: nextcord.Interaction) -> None:
        self.voice.resume()
        await interaction.response.send_message("Resumed music")

    @nextcord.slash_command(description="Use this to see the queue!")
    async def queue(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.send_message(self.queue)

    @nextcord.slash_command(description="Use this to see the current song!")
    async def current(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.send_message(self.current)

    @nextcord.slash_command(description="Use this to change the volume!")
    async def volume(self, interaction: nextcord.Interaction, volume: int) -> None:
        self.voice.source.volume = volume / 100
        await interaction.response.send_message(f"Changed volume to {volume}")

    async def play_next(self):
        self.next.clear()
        if not self.queue:
            return
        self.current = self.queue.pop(0)
        self.voice.play(
            self.current, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
        await self.next.wait()

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await self.play_next()
            await asyncio.sleep(1)
