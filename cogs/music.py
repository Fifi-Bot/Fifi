"""
MIT License

Copyright (c) 2021 Meme Studios

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sellcopies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import discord
from discord.ext import commands
import DiscordUtils
import datetime

music = DiscordUtils.Music()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['p'])
    async def play(self, ctx, *, url):
        if ctx.voice_client is None:
            try:
                await ctx.author.voice.channel.connect() #Joins author's voice channel
                await ctx.reply(f'<a:ablobjoin:829985443399467018> Joined `{ctx.author.voice.channel.name}`.')
            except:
                await ctx.send('You are not in a Voice Channel! Please join a voice channel and try again!\nIf you are in a Voice Channel, maybe the bot has no permission of joining the VC. Try to check. \nThanks!')
                return

            try:
                player = music.get_player(guild_id=ctx.guild.id)
                if not player:
                    player = music.create_player(ctx, ffmpeg_error_betterfix=True)
                if not ctx.voice_client.is_playing():
                    await ctx.send(f'<a:loading:829244740293099530> Searching for `{url}` in YouTube.. Please Wait')
                    await player.queue(url, bettersearch=True)
                    song = await player.play()
                    await ctx.send(f"<:green_play_button:851322498250571787> Now Playing `{song.name}`")
                else:
                    await ctx.send(f'<a:loading:829244740293099530> Searching for `{url}` in YouTube.. Please Wait')
                    song = await player.queue(url, bettersearch=True)
                    await ctx.send(f"<:green_queue_button:833517336110563409> Queued `{song.name}`")
            except:
                await ctx.send('This is an error. It is probably because of YouTube. Please try again!')
        else:
            try:
                player = music.get_player(guild_id=ctx.guild.id)
                if not player:
                    player = music.create_player(ctx, ffmpeg_error_betterfix=True)
                if not ctx.voice_client.is_playing():
                    await ctx.send(f'<a:loading:829244740293099530> Searching for `{url}` in YouTube.. Please Wait')
                    await player.queue(url, bettersearch=True)
                    song = await player.play()
                    await ctx.send(f"<:green_play_button:851322498250571787> Now Playing `{song.name}`")
                else:
                    await ctx.send(f'<a:loading:829244740293099530> Searching for `{url}` in YouTube.. Please Wait')
                    song = await player.queue(url, bettersearch=True)
                    await ctx.send(f"<:green_queue_button:833517336110563409> Queued `{song.name}`")
            except:
                await ctx.send('This is an error. It is probably because of YouTube. Please try again!')

    @commands.command(aliases = ['j'])
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect() #Joins author's voice channel
        except:
            await ctx.send('You are not in a Voice Channel! Please join a voice channel and try again!\nIf you are in a Voice Channel, maybe the bot has no permission of joining the VC. Try to check. \nThanks!')
            return
        await ctx.reply(f'<a:ablobjoin:829985443399467018> Joined `{ctx.author.voice.channel.name}`.')

    @commands.command(aliases = ['disconnect'])
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
        except:
            await ctx.reply(f'I am not in a Voice Channel {ctx.author.mention}!')
            return
        await ctx.reply('<a:ablobleave:829985456283189249> Left/Disconnected from the Voice Channel.')

    @commands.command()
    async def pause(self, ctx):
        try:
            player = music.get_player(guild_id=ctx.guild.id)
            song = await player.pause()
            await ctx.reply(f"<:green_pause_button:851338985216147487> Paused `{song.name}`")
        except:
            await ctx.reply('Nothing is currently playing right now.')

    @commands.command()
    async def resume(self, ctx):
        try:
            player = music.get_player(guild_id=ctx.guild.id)
            song = await player.resume()
            await ctx.reply(f"<:green_play_button:851322498250571787> Resumed `{song.name}`")
        except:
            await ctx.reply('Nothing is currently playing right now.')

    @commands.command()
    async def stop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        await player.stop()
        await ctx.reply("<:green_stop_button:851352256615546890> Stopped playing music!")

    @commands.command(aliases = ['l'])
    async def loop(self, ctx):
        try:
            player = music.get_player(guild_id=ctx.guild.id)
            song = await player.toggle_song_loop()
            if song.duration == 0.0:
                await ctx.reply('You cannot Loop a Live Video!')
            else:
                if song.is_looping:
                    await ctx.reply(f"🔂 Enabled loop for `{song.name}`")
                else:
                    await ctx.reply(f"🔂 Disabled loop for `{song.name}`")
        except:
            await ctx.reply('Nothing is currently playing!')

    @commands.command(aliases = ['vol'])
    async def volume(self, ctx, vol):
        try:
            player = music.get_player(guild_id=ctx.guild.id)
            song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
            await ctx.reply(f"Changed volume of `{song.name}` to `{vol}%`")
        except:
            await ctx.reply('You cannot change the volume if you are not playing any songs!')
            return

    @commands.command(aliases = ['rm'])
    async def remove(self, ctx, index):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.remove_from_queue(int(index))
        await ctx.reply(f"Removed `{song.name}` from queue")

    @commands.command(aliases = ['q'])
    async def queue(self, ctx):
      try:
        player = music.get_player(guild_id=ctx.guild.id)
        embed = discord.Embed(
              color = discord.Color.green(),
              title = '<:green_queue_button:833517336110563409> Queue <:green_queue_button:833517336110563409> ',
              description = "\n".join([song.name for song in player.current_queue()])
            )
        await ctx.reply(embed=embed)
      except: #AttributeError
         embed = discord.Embed(
              color = discord.Color.green(),
              title = '<:green_queue_button:833517336110563409> Queue <:green_queue_button:833517336110563409>',
              description = "There is no music in the queue!"
         )
         await ctx.reply(embed=embed)
      #except:
          #ctx.send("An Error Occured! Please report it to whyfai#0777 the developer. We will fix it ASAP!")


    @commands.command(aliases = ['np']) #Make Hyperlinks in the nowplaying command!
    async def nowplaying(self, ctx):
        try:
            player = music.get_player(guild_id=ctx.guild.id)
            song = player.now_playing()
            if song.duration == 0.0:
                embed = discord.Embed(
                color = discord.Color.green(),
                    title = '<:green_play_pause_button:833517317463212122> Now/Currently Playing:',
                    description = f'[{song.name}]({song.url} "Takes you to the YouTube Video!")'
                )
                embed.set_thumbnail(url = song.thumbnail)
                embed.add_field(name = 'Duration: ', value = 'LIVE', inline=True)
                embed.add_field(name = 'Channel Name: ', value = f'[{song.channel}]({song.channel_url} "Takes you to the YouTube Channel!")', inline=True)
                await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(
                  color = discord.Color.green(),
                  title = '<:green_play_pause_button:833517317463212122> Now/Currently Playing:',
                  description = f'[{song.name}]({song.url} "Takes you to the YouTube Video!")'
                )
                embed.set_thumbnail(url = song.thumbnail)
                embed.add_field(name = 'Duration: ', value = f'{str(datetime.timedelta(seconds = int(song.duration)))}', inline=True)
                embed.add_field(name = 'Loop: ', value = f'{song.is_looping}', inline=True)
                embed.add_field(name = 'Channel Name: ', value = f'[{song.channel}]({song.channel_url} "Takes you to the YouTube Channel!")', inline=True)
                await ctx.reply(embed=embed)
        except:
            embed = discord.Embed(
                color = discord.Color.green(),
                title = '<:green_play_pause_button:833517317463212122> Now/Currently Playing:',
                description = f'Nothing is currently playing right now!'
            )
            await ctx.reply(embed=embed)

    @commands.command(aliases = ['fs', 's', 'forceskip'])
    async def skip(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        data = await player.skip(force=True)
        if len(data) == 2:
            await ctx.reply(f"<:green_next_button:833517290892951603> Skipped from `{data[0].name}` to `{data[1].name}`")
        else:
            await ctx.reply(f"<:green_next_button:833517290892951603> Skipped `{data[0].name}`")

def setup(bot):
    bot.add_cog(Music(bot))
    print("Music Cog is Ready!")
