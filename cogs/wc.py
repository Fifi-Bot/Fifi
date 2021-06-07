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
import json
import asyncio

class WC(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @commands.command()
    async def menu(self,ctx):
      embed = discord.Embed(title = 'MENU OF THE WHYFAI CAFE', description = '<:turtle:849453698844327936> = FiBucks and ⏣ = Dank Memer Coins \n\nNOTE: Dank Memer Coin transactions have 8% tax.', color = discord.Color.blue())
      embed.add_field(name = 'Pizza:', value = 'Pepperoni Pizza : <:turtle:849453698844327936>100 / ⏣ 1,000 \nCheese Pizza : <:turtle:849453698844327936>50 / ⏣ 500', inline = False),embed.add_field(name = 'Pizza Toppings:', value = 'Extra Cheese : <:turtle:849453698844327936>20 / ⏣ 200', inline = False)
      embed.add_field(name = 'Miscellaneous:', value = 'Kit Kat : <:turtle:849453698844327936>30 \ ⏣ 300 \nFried Fish : <:turtle:849453698844327936>150 \ ⏣ 1,500')
      embed.add_field(name = 'Drinks:', value = '**Milkshakes - <:turtle:849453698844327936>30 \ ⏣ 300 each:** \nChocolate Milkshake \nVanilla Milkshake \nStrawberry Milkshake \n\n**Coffee - <:turtle:849453698844327936>40 / ⏣ 400 each:** \nCappucino \nBlack Coffee \nLatte \nEspresso \nDalgona Coffee', inline = False)
      return await ctx.reply(embed=embed)
    
    food_info = {"pepperoni pizza":{"price":100,"gif/image":"https://tenor.com/view/pizza-pepperoni-damn-cheese-yasss-gif-4287751"},
    "cheese pizza":{"price":50,"gif/image":"https://tenor.com/view/dominos-pizza-pizza-cheese-pizza-fast-food-pizza-day-gif-16773779"},
    "chocolate milkshake":{"price":30,"gif/image":"https://cdn.discordapp.com/attachments/844813872975839244/845202489800261672/chocolate_milkshake.jpg"},
    "vanilla milkshake":{"price":30,"gif/image":"https://cdn.discordapp.com/attachments/844813872975839244/845203989515862056/Classic-Vanilla-Milkshake-2-700px.png"},
    "strawberry milkshake":{"price":30,"gif/image":"https://cdn.discordapp.com/attachments/844813872975839244/845203039950471218/strawberry-milkshake.png"},
    "cappucino":{"price":40,"gif/image":"https://cdn.discordapp.com/attachments/749875006238097478/845978629552209930/844ad4d1-38e3-4d89-b45f-f2fb172dcacc.png"},
    "black coffee":{"price":40,"gif/image":"https://cdn.discordapp.com/attachments/836859795587727381/845979155426312192/blackcoffee-1561170296.png"},
    "latte":{"price":40,"gif/image":"https://tenor.com/view/coffee-latte-milk-gif-7929800"},
    "espresso":{"price":40,"gif/image":"https://cdn.discordapp.com/attachments/836859795587727381/845979630111686676/5f7a1e1a209d9.png"},
    "dalgona coffee":{"price":40,"gif/image":"https://cdn.discordapp.com/attachments/749875006238097478/845290406387646524/5e7eb044aa9a2.png"},
    "kit kat":{"price":30,"gif/image":"https://tenor.com/view/kit-kat-break-break-time-breaks-are-good-give-me-a-break-gif-12380930"},
    "fried fish":{"price":150,"gif/image":"https://cdn.discordapp.com/attachments/836859795587727381/845980723944882206/Fried-Fish.png"}}

    @commands.command()
    async def order(self,ctx,food=None):
      return await ctx.send("This command has been deprecated. Please use `w!order` instead. Thank you.")
      if food == None:
        return await ctx.reply("Please specify what you want to order, if you are unsure please run `f.menu` or check the pins in whyfai cafe.")
      else:
        try:
          food = food.lower()
          image = self.food_info[food]["gif/image"]
          price = self.food_info[food]["price"]
          await ctx.reply("🍳 Your order is now being prepared! Please wait...")
          await asyncio.sleep(10)
          await ctx.reply(f"Here is your {food} ({image})")
          await asyncio.sleep(3)
          await ctx.send(f"Your bill is {price} DMC. Please give whyfai the money.")
          await asyncio.sleep(3)
          return await ctx.send("We hope you liked the service! Tell your feedback in <#845108315793129482>")
        except KeyError:
          return await ctx.reply("That is not something in the menu!")

def setup(bot):
    bot.add_cog(WC(bot))
