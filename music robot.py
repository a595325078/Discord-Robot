import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

music_queue = []
current_song = None

@bot.event
async def on_ready():
    print(f"已登入為 {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        
        if not isinstance(voice, discord.VoiceClient):
            await channel.connect()
            await ctx.send(f"已加入: {channel}")
        else:
            await voice.move_to(channel)
            await ctx.send(f"已移動至: {channel}")
    else:
        await ctx.send("你不在語音頻道裡啦")

async def play_music(ctx, voice):
    global current_song

    if len(music_queue) == 0:
        current_song = None
        return

    current_song = music_queue.pop(0)

    if current_song is None:
        await ctx.send("清單中發現無效項目，已跳過。")
        await play_music(ctx, voice)
        return

    base_path = os.path.dirname(os.path.abspath(__file__)) 
    file_path = os.path.join(base_path, current_song)

    if not os.path.isfile(file_path):
        await ctx.send(f"找不到檔案 `{current_song}`，跳過。")
        await play_music(ctx, voice)
        return

    def after_play(err):
        if err:
            print(f"播放錯誤: {err}")
        
        asyncio.run_coroutine_threadsafe(play_music(ctx, voice), bot.loop)

    if isinstance(voice, discord.VoiceClient):
        voice.play(
            discord.FFmpegPCMAudio(file_path, before_options="-nostdin", options="-vn"),
            after=after_play
        )
        await ctx.send(f"正在播放: `{current_song}`")

@bot.command()
async def play(ctx, *, filename: Optional[str] = None):
    global current_song

    if not filename:
        await ctx.send("請輸入要播放的檔案名稱，例如：`$play song1.mp3`")
        return

    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        
        if not isinstance(voice, discord.VoiceClient):
            voice = await channel.connect()

        music_queue.append(filename)

        if isinstance(voice, discord.VoiceClient):
            if not voice.is_playing() and not current_song:
                await play_music(ctx, voice)
            else:
                await ctx.send(f"已加入清單: `{filename}`")
    else:
        await ctx.send("你沒進來怎麼播")

@bot.command()
async def skip(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if isinstance(voice, discord.VoiceClient) and voice.is_playing():
        voice.stop()
        await ctx.send("已跳過歌曲")
    else:
        await ctx.send("沒有正在播放的歌曲")

@bot.command()
async def queue(ctx):
    if len(music_queue) == 0:
        await ctx.send("播放清單是空的")
    else:
        queue_list = "\n".join([f"{i+1}. {song}" for i, song in enumerate(music_queue)])
        await ctx.send(f"播放清單：\n{queue_list}")

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if isinstance(voice, discord.VoiceClient) and voice.is_playing():
        voice.pause()
        await ctx.send("停止播放啦")
    else:
        await ctx.send("沒有音樂在播放啦")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if isinstance(voice, discord.VoiceClient) and voice.is_paused():
        voice.resume()
        await ctx.send("繼續播放")
    else:
        await ctx.send("沒有音樂在暫停狀態")

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if isinstance(voice, discord.VoiceClient):
        await voice.disconnect(force=True)
        await ctx.send("掛掉了")
    else:
        await ctx.send("不在啦")

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    print("錯誤：找不到 DISCORD_TOKEN 環境變數。")
    print("請在 .env 檔案中設定 DISCORD_TOKEN = '你的TOKEN'")
else:
    bot.run(TOKEN)