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
import random

class Battlefield(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.shoot.add_check(self.shoot_check)
  
  @commands.Cog.listener()
  async def on_message(self, message):
    with open("battle_db.json", "r") as f:
      db = json.load(f)
    if str(message.author.id) not in db["max_health"]:
      db["max_health"][str(message.author.id)] = 100
    if str(message.author.id) not in db["owned_guns"]:
      db["owned_guns"][str(message.author.id)] = []
    if str(message.author.id) not in db["in_battlefield"]:
      db["in_battlefield"][str(message.author.id)] = False
    if str(message.author.id) not in db["current_health"]:
      db["current_health"][str(message.author.id)] = 100
    if str(message.author.id) not in db["potion"]:
      db["potion"][str(message.author.id)] = 0
    with open("battle_db.json", "w") as f:
      json.dump(db, f, indent=4)

  gun_info = {
    "AK-47": {
      "price": 2900,
      "damage_low": 10,
      "damage_high": 20,
      "success_rate": 70,
      "ammo": 10
      }
  }

  @commands.group()
  async def gunshop(self,ctx):
    if ctx.invoked_subcommand is None:
      embed = discord.Embed(title="Gun Shop",description="Here are the guns you can buy")
      for gun in self.gun_info:
        embed.add_field(name="{} - <:turtle:849453698844327936> {:,}".format(gun,self.gun_info[gun]["price"]),value="Damage per shot: {:,}-{:,}, Success Rate: {}%".format(self.gun_info[gun]["damage_low"],self.gun_info[gun]["damage_high"],self.gun_info[gun]["success_rate"]))
      return await ctx.reply(embed=embed)

  @gunshop.command()
  async def buy(self,ctx,gun=None):
    if gun not in self.gun_info:
      return await ctx.reply("That is not a gun in the shop!")
    else:
      with open("wallet.json","r") as f:
        db = json.load(f)
      if db["wallet"][str(ctx.author.id)] < self.gun_info[gun]["price"]:
        return await ctx.reply("You do not have enough FiBucks in wallet to buy this!")
      else:
        db["wallet"][str(ctx.author.id)] -= self.gun_info[gun]["price"]
        with open("battle_db.json","r") as x:
          battle_db = json.load(x)
        battle_db["owned_guns"][str(ctx.author.id)].append(gun)
        with open("wallet.json","w") as f:
          json.dump(db, f, indent=4)
        with open("battle_db.json","w") as x:
          json.dump(battle_db, x, indent=4)
        return await ctx.reply("You have bought a {} for <:turtle:849453698844327936>{:,}".format(gun,self.gun_info[gun]["price"]))

  @commands.group()
  async def battlefield(self,ctx):
    if ctx.invoked_subcommand is None:
      return await ctx.reply("Please specify either `join` or `leave`")

  @battlefield.command(aliases=["spawn","respawn"])
  async def join(self,ctx):
    with open("battle_db.json","r") as x:
      battle_db = json.load(x)
    if str(ctx.author.id) not in battle_db['equipped_gun']:
      return await ctx.reply("You do not have a gun equipped")
    if battle_db["equipped_gun"][str(ctx.author.id)] == None:
      return await ctx.reply("You do not have a gun equipped")
    else:
      battle_db["in_battlefield"][str(ctx.author.id)] = True
      battle_db["sector"][str(ctx.author.id)] = random.randint(1,30)
      sector = battle_db["sector"][str(ctx.author.id)]
      with open("battle_db.json","w") as x:
        json.dump(battle_db, x, indent=4)
      return await ctx.reply("You have joined the battlefield and spawned in sector {}!".format(sector))

  @battlefield.command(aliases=["quit"])
  async def leave(self,ctx):
    with open("battle_db.json","r") as x:
      battle_db = json.load(x)
    battle_db["in_battlefield"][str(ctx.author.id)] = False
    with open("battle_db.json","w") as x:
      json.dump(battle_db, x, indent=4)
    return await ctx.reply("You have left the battlefield")
  
  @battlefield.command()
  async def profile(self,ctx):
    with open("battle_db.json", "r") as f:
      db = json.load(f)
    embed = discord.Embed(title=f"{ctx.author}'s Battlefield Stats",description="Here is your stats in the battlefield",color=discord.Colour.green())
    embed.add_field(name="❤ Max Health",value=db["max_health"][str(ctx.author.id)])
    embed.add_field(name="💕 Current Health",value=db["current_health"][str(ctx.author.id)])
    return await ctx.reply(embed=embed)

  @commands.command()
  async def shoot(self,ctx,target : discord.Member):
    with open("battle_db.json","r") as x:
      battle_db = json.load(x)
    if battle_db["in_battlefield"][str(ctx.author.id)] == False:
      return await ctx.reply("You are not in the battlefield!")
    if battle_db["in_battlefield"][str(target.id)] == False:
      return await ctx.reply("That person is not in battlefield")
    if battle_db["sector"][str(ctx.author.id)] != battle_db["sector"][str(target.id)]:
      return await ctx.reply("You are not in the same sector as your target, they are in sector {}".format(battle_db["sector"][str(target.id)]))
    else:
      equipped_gun = battle_db["equipped_gun"][str(ctx.author.id)]
      damage = random.randint(self.gun_info[equipped_gun]["damage_low"],self.gun_info[equipped_gun]["damage_high"])
      success_fail = random.randint(0,100)
      if success_fail > self.gun_info[equipped_gun]["success_rate"]:
        await ctx.reply("You tried shooting at {} but you missed! Better luck next time".format(target))
      elif damage > battle_db["current_health"][str(target.id)]:
        with open("wallet.json","r") as f:
          db = json.load(f)
        db["wallet"][str(ctx.author.id)] += 2000
        db["wallet"][str(target.id)] -= 1250
        with open("wallet.json","w") as f:
          json.dump(db, f, indent=4)
        battle_db["current_health"][str(target.id)] = battle_db["max_health"][str(target.id)]
        with open("battle_db.json","w") as x:
          json.dump(battle_db, x, indent=4)
        await ctx.reply("You dealt {:,} damage to {} and defeated them. You earned <:turtle:849453698844327936>2,000 and they lost <:turtle:849453698844327936>1,250".format(damage,target))
      else:
        battle_db["current_health"][str(target.id)] -= damage
        target_health = battle_db["current_health"][str(target.id)]
        with open("battle_db.json","w") as x:
          json.dump(battle_db, x, indent=4)
        await ctx.reply("You dealt {:,} damage to {}. They now have {:,} health!".format(damage,target,target_health))

      if str(ctx.author.id) in battle_db['shots']:
        if battle_db["equipped_gun"][str(ctx.author.id)] in battle_db['shots'][str(ctx.author.id)]:
          battle_db['shots'][str(ctx.author.id)][battle_db["equipped_gun"][str(ctx.author.id)]] += 1
        else:
          battle_db['shots'][str(ctx.author.id)][battle_db["equipped_gun"][str(ctx.author.id)]] = 1
      else:
        battle_db['shots'][str(ctx.author.id)] = {}
        battle_db['shots'][str(ctx.author.id)][battle_db["equipped_gun"][str(ctx.author.id)]] = 1

      with open("wallet.json","w") as f:
        json.dump(db, f, indent=4)

  #@shoot.check
  async def shoot_check(self, ctx):
    try:
      with open("battle_db.json","r") as x:
        battle_db = json.load(x)

      equipped_gun = battle_db["equipped_gun"][str(ctx.author.id)]
      shots_taken = battle_db['shots'][equipped_gun]

      if self.gun_info[equipped_gun]['ammo'] <= shots_taken:
        await ctx.send("Please reload your weapon! `f.reload`")
        return False
      else:
        return True
    except KeyError:
      return True

  @commands.command()
  async def reload(self,ctx,gun=None):
    with open("battle_db.json","r") as x:
      battle_db = json.load(x)

    gun = gun or battle_db["equipped_gun"].get([str(ctx.author.id)], None)

    if gun is None:
      return await ctx.send("You do not have any guns!")
    elif gun not in self.gun_info:
      return await ctx.send("Not a valid gun!")
    elif gun not in battle_db["equipped_gun"][str(ctx.author.id)]:
      return await ctx.send("You do not own that gun!")

    if str(ctx.author.id) in battle_db['shots']:
      if battle_db["equipped_gun"][str(ctx.author.id)] in battle_db['shots'][str(ctx.author.id)]:
        battle_db['shots'][str(ctx.author.id)][battle_db["equipped_gun"][str(ctx.author.id)]] += 0

    with open("battle_db.json","w") as x:
      json.dump(battle_db, x, indent=4)

    await ctx.send("Reloaded your `{}` gun.".format(gun))

  @commands.command()
  async def equip(self,ctx,gun):
    with open("battle_db.json","r") as x:
      db = json.load(x)
    if gun not in db["owned_guns"][str(ctx.author.id)]:
      return await ctx.reply("You either do not own that gun or that is not a vaild gun!")
    else:
      db["equipped_gun"][str(ctx.author.id)] = gun
      with open("battle_db.json","w") as x:
          json.dump(db, x, indent=4)
      return await ctx.reply("You have equipped {}".format(gun))
  
  @commands.command()
  async def run(self,ctx,sector:int=None):
    with open("battle_db.json","r") as x:
      db = json.load(x)
    if db["in_battlefield"][str(ctx.author.id)] == False:
      return await ctx.reply("You are not in the battlefield")
    if sector == None:
      return await ctx.reply("Please specify what sector you want to run to!")
    if sector > 30:
      return await ctx.reply("There are only 30 sectors!")
    if sector > db["sector"][str(ctx.author.id)] + 5:
      return await ctx.reply("You can only run to the 5 nearest sectors")
    if sector < db["sector"][str(ctx.author.id)] - 5:
      return await ctx.reply("You can only run to the 5 nearest sectors")
    else:
      db["sector"][str(ctx.author.id)] = sector
      with open("battle_db.json","w") as x:
          json.dump(db, x, indent=4)
      return await ctx.reply("You have ran to sector {}".format(sector))

  @commands.group(aliases=["drink"])
  async def use(self,ctx):
    if ctx.invoked_subcommand == None:
      return await ctx.reply("Please specify what you want to use!/drink")

  @use.command()
  async def potion(self,ctx):
    with open("battle_db.json","r") as x:
      db = json.load(x)
    if db["potion"][str(ctx.author.id)] == 0:
      return await ctx.reply("You do not have any potions!")
    if db["current_health"][str(ctx.author.id)] == db["max_health"][str(ctx.author.id)]:
      return await ctx.reply("You already are full health!")
    else:
      db["potion"][str(ctx.author.id)] -= 1
      if db["current_health"][str(ctx.author.id)] + 50 > db["max_health"][str(ctx.author.id)]:
        db["current_health"][str(ctx.author.id)] = db["max_health"][str(ctx.author.id)]
      else:
        db["current_health"][str(ctx.author.id)] = db["current_health"][str(ctx.author.id)] + 50
        health = db["current_health"][str(ctx.author.id)]
        with open("battle_db.json","w") as x:
          json.dump(db, x, indent=4)
        return await ctx.reply("You have used a potion and now you have {:,} health.".format(health))

def setup(bot):
  bot.add_cog(Battlefield(bot))
