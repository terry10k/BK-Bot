import discord
from discord.ext import commands

import youtube_dl
from youtube_search import YoutubeSearch

import random

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if (ctx.author.voice is None):
            await ctx.send("You're... not in a voice channel?")
            return

        voice_channel = ctx.author.voice.channel
        if (ctx.voice_client is None):
            await voice_channel.connect()
            await self.laugh(ctx)
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Bye")

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused ⏸")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resumed ⏯")

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.send("Stopped 👍")

    @commands.command()
    async def play(self, ctx, *, args):
        await self.join(ctx)

        ctx.voice_client.stop()

        #search yt if not url
        if(args.startswith('https://') == False):
            results = YoutubeSearch(args, max_results=1).to_dict()
            args = "https://www.youtube.com/watch?v=" + results[0]['id']
        #end if


        YDL_OPTIONS = {'format': 'bestaudio','acodec': 'mp3', 'source_address': '0.0.0.0'}

        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(args, download=False)

            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

            vc.play(source)

    @commands.command()
    async def laugh(self, ctx):
        chance = 1
        lNum = random.randint(1,3)

        if(chance == 1):

            vc = ctx.voice_client

            url = "BK-Laugh " + str(lNum) + ".mp3"

            source = discord.FFmpegPCMAudio(source=url)

            vc.play(source)


def setup(client):
    client.add_cog(music(client))


