import discord, os
from discord.ext import commands
from discord.ext.commands import is_owner as owner_only

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @owner_only()
    async def pull(self, ctx):
        os.system("git pull")
        await ctx.send("Done.")
        
def setup(bot):
    bot.add_cog(Owner(bot))
