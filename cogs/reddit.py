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
import praw
from discord.ext import commands
import json
import os
import datetime
import random
import humanize
from discord.ext import flags

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['meme'])
    async def memes(self, ctx):
        await self.reddit(ctx, subreddit="memes")

    @commands.command(aliases = ['red', 'redd', 'reddits'])
    async def reddit(self, ctx, *, subreddit = None):
        if subreddit == None:
            return await ctx.send("Missing required argument, `subreddit`.")
        if subreddit == "hentai" or subreddit == "porn" or subreddit == "NSFW":
            return await ctx.send("no u, This bot is family friendly")

        async with self.bot.session.get(f"https://www.reddit.com/r/{subreddit}/new.json") as resp:
            r = await resp.json()

        if r.get("error", None) is not None:
            return await ctx.send("Couldn't find a subreddit with that name.")

        posts = r["data"]["children"]
        if not posts:
            return await ctx.send("Apparently there are no posts in this subreddit...")

        random_post = random.choice(posts)["data"]
        posted_when = datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(random_post["created"])

        embed = discord.Embed(
            title=random_post["title"], url=random_post["url"],
            description=f"Posted by `u/{random_post['author']}` {humanize.naturaldelta(posted_when)} ago\n"
            f"\U0001f44d {random_post['ups']} \U0001f44e {random_post['downs']}",
            colour=0x0fffff if ctx.author.color.value == 0 else ctx.author.color
        )
        embed.set_image(url = random_post["url"])

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Reddit(bot))
    print("Reddit Cog is Ready!")
