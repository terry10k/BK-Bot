import discord
from discord.ext import commands

import youtube_dl
from youtube_search import YoutubeSearch

import random

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}



class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    queue = {}

    @commands.command()
    async def join(self, ctx):

        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel!")
            return
        else:
            channel = ctx.message.author.voice.channel
            self.queue = {}
            await ctx.send(f'Connected to ``{channel}``')

        await channel.connect()

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



            async with ctx.typing():

                if (args.startswith('https://') == False):
                    results = YoutubeSearch(args, max_results=1).to_dict()
                    args = "https://www.youtube.com/watch?v=" + results[0]['id']
                # end if

                YDL_OPTIONS = {'format': 'bestaudio', 'acodec': 'mp3', 'source_address': '0.0.0.0'}


                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(args, download=False)

                    url2 = info['formats'][0]['url']

                player = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

                if len(self.queue) == 0:

                    self.start_playing(ctx.voice_client, player)
                    await ctx.send(" Now Playing : " + info['title'])


                else:


                    self.queue[len(self.queue)] = player
                    await ctx.send(" Queued Up : " + info['title'])


    def start_playing(self, voice_client, player):

        self.queue[0] = player

        i = 0
        while i < len(self.queue):
            try:
                voice_client.play(self.queue[i], after=lambda e: print('Player error: %s' % e) if e else None)

            except:
                pass
            i += 1

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

