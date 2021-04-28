import asyncio, discord, youtube_dl, datetime as dt
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='-')
now = dt.datetime.now()
datetime = now.strftime("%m/%d/%Y, %H:%M:%S")

class MusicCom(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @client.command()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        guild = ctx.message.guild
        voice = guild.voice_client

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"({datetime}) Bot has left {channel}")
        else:
            print(f"({datetime}) Bot was told to leave voice channel, but was not in one")

    @client.command(aliases=['next'])
    async def skip(self, ctx):
        guild = ctx.message.guild
        voice = guild.voice_client

        if voice and voice.is_playing():
            print(f"({datetime}) Skipping song")
            voice.stop()
            await ctx.send("Skipping song")
        else:
            print(f"({datetime}) Attempted to skip song, but music not playing")
            await ctx.send("Music not playing")

    @client.command()
    async def play(self, ctx, *url):
        channel = ctx.message.author.voice.channel
        guild = ctx.message.guild
        voice = guild.voice_client
        url = ' '.join(url)

    # Checks if bot is connected to voice channel
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"({datetime}) Bot has connected to {channel}")

    # Sets youtube download options for video processing 
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True, # Removes extra ydl options
        }
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
        }
    # Grabs youtube audio file data
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print(f"({datetime}) Extracting audio data")
            # try:
            #     get(url) 
            # except:
            vidinfo = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
            # else:
            #     vidinfo = ydl.extract_info(url, download=False)
            URL = vidinfo['formats'][0]['url']
            title = vidinfo['title']

    # Plays audio file. After song plays, check queue for more songs
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.4 # Keep low or audio will be VERY LOUD (and distorted) (Max is 1)

        # nname = name.rsplit("-", 1)
        await ctx.send(f'Playing: {title}')
        print(f'({datetime}) Playing')

        while voice.is_playing():
            await asyncio.sleep(5)
            if (len(channel.members) < 2):
                voice.stop()
                await voice.disconnect()
            else:
                await asyncio.sleep(30)
                while voice.is_playing(): #and checks once again if the bot is not playing
                    break #if it's playing it breaks
                else:
                    await voice.disconnect()
    
    @client.command()
    async def pause(self, ctx):
        guild = ctx.message.guild
        voice = guild.voice_client

        if voice and voice.is_playing():
            print(f"({datetime}) Music paused")
            voice.pause()
            await ctx.send("Music paused")
        else:
            print(f"({datetime}) Attempted to pause music, but no music playing")
            await ctx.send("Could not pause music. Is there music playing?")

    @client.command()
    async def resume(self, ctx):
        guild = ctx.message.guild
        voice = guild.voice_client

        if voice and voice.is_paused():
            print(f"({datetime}) Music resumed")
            voice.resume()
            await ctx.send("Music resumed")
        else:
            print(f"({datetime}) Attempted to resume music, but music not paused")
            await ctx.send("Could not resume music. Is there music playing?")
    
    @client.command()
    async def stop(self, ctx):
        guild = ctx.message.guild
        voice = guild.voice_client

        if voice and voice.is_playing():
            print(f"({datetime}) Music stopped")
            voice.stop()
            await ctx.send("Music stopped")
        else:
            print(f"({datetime}) Attempted to stop music, but music not playing")
            await ctx.send("Music not playing")

def setup(client):
  client.add_cog(MusicCom(client))