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