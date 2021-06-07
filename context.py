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

from discord.ext import commands
import discord
import asyncio

class MyContext(commands.Context):
  def __init__(self):
    self.kek = "kek"
    
  async def confirmWithoutMessage(self, msg: discord.Message = None, *, reactions : list = ["<a:a_yes:815779246973779968>", "<a:a_no:815779276984156200>"], UserIsAuthor = True, timeout = 60.0):
        msg = msg or self.message
        yes, no = reactions
        await msg.add_reaction(yes)
        await msg.add_reaction(no)
        if UserIsAuthor:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check = lambda reaction, user: reaction.message == msg and user == self.author and str(reaction.emoji) in reactions, timeout=timeout)
            except asyncio.TimeoutError:
                return None, None, msg
        else:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check = lambda reaction, user: reaction.message == msg and str(reaction.emoji) in reactions, timeout=timeout)
            except asyncio.TimeoutError:
                return None, None, msg

        if str(reaction.emoji) == yes:
            return True, str(reaction.emoji), reaction.message
        else:
            return False, str(reaction.emoji), reaction.message

  async def three_rr(self, reaction1, reaction2, reaction3, msg: discord.Message = None, *, UserIsAuthor = True, timeout = 60.0):
        reactions = [reaction1,reaction2,reaction3]
        msg = msg or self.message
        await msg.add_reaction(reaction1)
        await msg.add_reaction(reaction2)
        await msg.add_reaction(reaction3)
        if UserIsAuthor:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check = lambda reaction, user: reaction.message == msg and user == self.author and str(reaction.emoji) in reactions, timeout=timeout)
            except asyncio.TimeoutError:
                return None, None, msg
        else:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check = lambda reaction, user: reaction.message == msg and str(reaction.emoji) in reactions, timeout=timeout)
            except asyncio.TimeoutError:
                return None, None, msg


            return str(reaction.emoji), reaction.message
