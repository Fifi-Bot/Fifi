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
import asyncio
from asyncio import create_task as tasks
import json
import asyncio
import datetime
import random

cooldownFiveHour = 2700

ResetCooldownTime = datetime.time(hour=0)

class Currency(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.currencyCooldown = []
    self.pauseCurrency = False
    self.robbed = []
    self.passiveCooldown = []
    resetCooldownTask = bot.loop.create_task(self.resetCooldown())
    resetCooldownTask.add_done_callback(self.exception_catching_callback)
  
  def exception_catching_callback(self, task):
    if task.exception():
      task.print_stack()

  async def cog_check(self, ctx):
    if self.pauseCurrency:
      return False
    else:
      return True

  def removeAllItems(self, js, key):
    keys = js[key]
    for item in keys:
      if isinstance(keys, list):
        keys.remove(item)
    
    return js

  async def resetCooldown(self):
    await self.bot.wait_until_ready()
    while True:
      now = datetime.datetime.utcnow()
      date = now.date()
      if now.time() > ResetCooldownTime:
        date = now.date() + datetime.timedelta(days=1)
      then = datetime.datetime.combine(date, ResetCooldownTime)
      await discord.utils.sleep_until(then)
      with open("wallet.json", "r") as f:
        js = json.load(f)

      if "onDailyCooldown" in js:
        for item in js["onDailyCooldown"]:
          js["onDailyCooldown"].remove(item)
      
        with open("wallet.json", "w") as f:
          json.dump(js, f, indent=4)

  async def cog_command_error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
      return await ctx.reply("Currency is currently paused.")

  @commands.Cog.listener()
  async def on_member_join(self, member):
    if self.pauseCurrency:
      return
    with open("wallet.json", "r") as f:
      db = json.load(f)
    if not member.bot: #Isn't this easy whyfai.......
      db["wallet"][str(member.id)] = 500
    with open("wallet.json", "w") as f:
      json.dump(db, f, indent=4)
      
  async def addCooldown(self, userID, *, seconds = 5):
    self.currencyCooldown += [userID]
    await asyncio.sleep(seconds)
    try:
      self.currencyCooldown.remove(userID)
    except:
      try:
        self.currencyCooldown.pop(self.currencyCooldown.index(userID))
      except:
        pass

  #@commands.command()
  #@commands.is_owner()
  async def removeBotFromDatabase(self, ctx):
    self.pauseCurrency = True
    await asyncio.sleep(5)
    with open("wallet.json", "r") as f:
      db = json.load(f)
    #for x in db:
    #  for i in db[x]:
    #    mem = self.bot.get_user(int(str(i)))
    #    if mem is not None:
    #      if mem.bot:
    #        del db[x][i]

    d = {}
    for k, v in db.items():
      d[k] = {}
      for vi, idk in k[v]:
        mem = self.bot.get_user(int(str(vi)))
        if not mem.bot:
          d[k][vi] = idk
        
    #db = {k : v for k, v in db.items() for vi,idk in k[v].items() if not self.bot.get_user(int(str(vi))).bot} 

    with open("wallet.json", "w") as f:
      db = json.dump(db, f, indent=4)

    await ctx.reply("Done.")
    self.pauseCurrency = False

  @commands.command()
  @commands.is_owner()
  async def setPause(self, ctx):
    self.pauseCurrency = not self.pauseCurrency
    await ctx.reply("Done.")

  async def addUserToDatabse(self, userID):
    #with open("wallet.json", "r") as f:
      #db = json.load(f)
    if self.bot.get_user(int(userID)).bot:
      return
    #if userID not in db["wallet"]:
      #db["wallet"][str(userID)] = 10000
    #if userID not in db["bank"]:
      #db["bank"][str(userID)] = False
    #if userID not in db["bankspace"]:
      #db["bankspace"][str(userID)] = 0
    #if userID not in db["amt_in_bank"]:
      #db["amt_in_bank"][str(userID)] = 0
    #if userID not in db["dm_notifs"]:
      #db["dm_notifs"][str(userID)] = True
    #if userID not in db["passive"]:
      #db["passive"][str(userID)] = False
      #with open("wallet.json", "w") as f:
        #json.dump(db, f, indent=4)

    #return db["wallet"][userID]

    db = await self.bot.pool.fetch("SELECT * FROM currency WHERE user_id = $1", str(userID))

    if db:
      return db

    await self.bot.pool.execute("INSERT INTO currency (user_id, wallet, amt_in_bank, bankspace, passive, claimed_daily) VALUES ($1, $2, $3, $4, $5, $6)", str(userID), "10000", "0", "0", False, False)

    db = await self.bot.pool.fetchrow("SELECT * FROM currency WHERE user_id = $1", str(userID))

  async def addBalanceToUser(self,userID, c = 1):
    db = await self.addUserToDatabse(userID)
    #with open("wallet.json", "r") as f:
      #db = json.load(f)
    if self.bot.get_user(int(userID)).bot:
      return
    #c = 1
    #if "passive" in db:
      #if str(userID) in db["passive"]:
    if db["passive"] == True:
      c = (c / 2) # wait why u adding 5 money . No. thats the default. I am just changing c from 5 to 3. ah k
    #if userID not in db["wallet"]:
    await self.bot.pool.execute("""
    UPDATE currency
    SET wallet = $2
    WHERE user_id = $1
    """, str(userID), str(int(db["wallet"]) + c))
      #db["wallet"][str(userID)] += c
    #with open("wallet.json", "w") as f:
      #json.dump(db, f, indent=4)

  async def getDatabase(self,userID):
    return await self.bot.pool.fetchrow("SELECT * FROM currency WHERE user_id = $1", str(userID))

  async def addBalanceToUserCounting(self,userID):
    #self.addUserToDatabse(userID)
    #with open("wallet.json", "r") as f:
      #db = json.load(f)
    #if self.bot.get_user(int(userID)).bot:
      #return
    #c = 10
    #if "passive" in db:
      #if str(userID) in db["passive"]:
        #if db["passive"][str(userID)] == True:
          #c = 5 #This is already fine, just fix other one
    #if userID not in db["wallet"]:
      #db["wallet"][str(userID)] = c
    #else:
      #db["wallet"][str(userID)] += c
    #with open("wallet.json", "w") as f:
      #json.dump(db, f, indent=4)

    await self.addBalanceToUser(userID, 10)

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.guild.id == 720991608425807932:
      if self.pauseCurrency:
        return
      #self.removeBotFromDatabase()
      if message.author.bot:
        return
      if message.channel.id == 802011668233715723:
        return
      if message.author.id in self.currencyCooldown:
        return
      if message.channel.id == 771639893411495957:
        await self.addBalanceToUserCounting(str(message.author.id))
      else:  
        await self.addBalanceToUser(str(message.author.id))
        await self.addCooldown(message.author.id)

    #await self.bot.process_commands(message)

  @commands.command(aliases=['bal','money','fibucks', 'bucks'])
  async def balance(self, ctx, member : discord.Member = None):
    if self.pauseCurrency:
      return await ctx.reply("Currency is currently paused. Will be back soon.")
    member = member or ctx.author
    if member.bot and member.id != 775986947796762645:
      return await ctx.reply("Really?")
    #with open("wallet.json", "r") as f:
      #db = json.load(f)
    db = await self.addUserToDatabse(str(member.id)) #Fixed by adding this whyfai
    money = db['wallet']
    bankspace = db["bankspace"] #{"wallet": {...}, "bankspace": {...}} --> It will be in this format. go to wallet.json
    amt_in_bank = db["amt_in_bank"]
    embed = discord.Embed(color=discord.Color.green(), title=f"{member}'s Balance")
    embed.add_field(name="Wallet:", value="<:turtle:849453698844327936>{:,}".format(int(money))) #The {:,} is for seperating the number with , like instead of 1000, it's 1,000. 
    embed.add_field(name="Bank:", value="<:turtle:849453698844327936>{:,}/<:turtle:849453698844327936>{:,}".format(int(amt_in_bank),int(bankspace)))
    await ctx.reply(embed=embed)

  def depositAll(self, ctx, userID, db):
    bankspace = db["bankspace"]
    amt_in_bank = db["amt_in_bank"]
    wallet = db["wallet"]
    amount = 0

    c = 0

    c += amt_in_bank

    while True:
      if c == bankspace:
        break
      
      if wallet == 0:
        break

      amount += 1
      c += 1
      wallet -= 1
      
    return amount

  @commands.command(aliases=['dep'])
  async def deposit(self,ctx,amount:str="0"):
    #with open("wallet.json") as f:
      #db = json.load(f)

    db = await self.getDatabase(str(ctx.author.id))
    bankspace = int(db["bankspace"])
    amt_in_bank = int(db["amt_in_bank"])
    if bankspace == 0:
      return await ctx.reply("You do not have a bank yet. Buy it from the shop!")
    if amount in ["max", "all"]:
      amount = self.depositAll(ctx, ctx.author.id, db)
      #return await ctx.reply("You have deposited {<:turtle:849453698844327936>{:,}. You now have <:turtle:849453698844327936>{:,} in your bank!".format(int(amount),int(db["amt_in_bank"][str(ctx.author.id)])))
    amount = int(amount)
    if amount > int(db["wallet"]):
      return await ctx.reply("You do not have this much money to deposit")
    if amt_in_bank + amount > bankspace:
      return await ctx.reply("You can only deposit a maximum of <:turtle:849453698844327936>{:,} in your current bank".format(int(bankspace)))
    if amt_in_bank + amount <= bankspace and int(db["wallet"]) >= amount:
      new_wallet = str(int(db["wallet"]) - amount)
      new_bank = str(int(db["amt_in_bank"]) + amount)

      await self.bot.pool.execute("""
      UPDATE currency
      SET wallet = $2,
          amt_in_bank = $3

      WHERE user_id = $1
      """, str(ctx.author.id), new_wallet, new_bank)
      #with open("wallet.json", "w") as f:
        #json.dump(db, f, indent=4)

      db = await self.getDatabase(str(ctx.author.id))

      return await ctx.reply("You have deposited {<:turtle:849453698844327936>{:,}. You now have <:turtle:849453698844327936>{:,} in your bank!".format(int(amount),int(db["amt_in_bank"])))
    #if amount == "max" or "all":
      #return await ctx.reply("Depositing max/all is still under construction!")

  @commands.command(aliases=["with"])
  async def withdraw(self,ctx,amount:str="0"):
    #with open("wallet.json") as f:
      #db = json.load(f)

    db = await self.getDatabase(str(ctx.author.id))

    amt_in_bank = int(db["amt_in_bank"])
    wallet = int(db["wallet"])
    if amount in ["max", "all"]:
      amount = amt_in_bank
    amount = int(amount)
    if amount == 0:
      return await ctx.reply("Please specify an amount to withdraw!")
    if amount > amt_in_bank:
      return await ctx.reply("You do not have that much money in your bank!")
    if amount > 0 and amount <= amt_in_bank:
      new_bank = (amt_in_bank - amount)
      new_wallet = (wallet + amount)
      #with open("wallet.json", "w") as f:
        #json.dump(db, f, indent=4)

      await self.bot.pool.execute("""
      UPDATE currency
      SET wallet = $2,
          amt_in_bank = $3

      WHERE user_id = $1
      """, str(ctx.author.id), new_wallet, new_bank)

      return await ctx.reply("You have withdrawed <:turtle:849453698844327936>{:,} from your bank!".format(int(amount)))
    #if amount == "max" or "all":
      #return await ctx.reply("Withdrawing max/all is still under construction!")

  async def insertToDatabase(self, db, *, wallet = None, bank = None, amt_in_bank = None, passive = None, claimed_daily = None):
    wallet = wallet or db['wallet']
    wallet = str(wallet)
    bank = bank or db['bank']
    bank = str(bank)
    amt_in_bank = amt_in_bank or db['bank']
    amt_in_bank = str(amt_in_bank)
    passive = passive or db['passive']
    claimed_daily = claimed_daily or db['claimed_daily']

  @commands.command(aliases=['steal','ripoff'])
  @commands.cooldown(1, 120, commands.BucketType.user)
  async def rob(self,ctx,*, target : discord.Member = None):
    #with open("wallet.json", "r") as f:
      #db = json.load(f)

    if target.bot or target == ctx.author: return await ctx.reply("Really?")

    db_target = await self.getDatabase(target.id)
    db_author = await self.getDatabase(ctx.author.id)
    
    #if "passive" in db:
    if db_author['passive'] == True:
      #if db["passive"][str(ctx.author.id)] == True:
      await ctx.reply("You are in passive mode!")
      ctx.command.reset_cooldown(ctx)
      return
    if db_target['passive'] == True:
      #if db["passive"][str(target.id)] == True:
      await ctx.reply("They are in passive mode!")
      ctx.command.reset_cooldown(ctx)
      return
          
    if int(db_author["wallet"]) < 500:
      await ctx.reply("You need at least <:turtle:849453698844327936>500 in wallet to rob!")
      ctx.command.reset_cooldown(ctx)
      return

    if target.id in self.robbed:
      await ctx.reply("Please give them some time. They have been robbed recently.")
      return ctx.command.reset_cooldown(ctx)
    else:
      try:
        if 100 > db_target["wallet"]:
          await ctx.reply("Not worth it man.")
          ctx.command.reset_cooldown(ctx)
          return
      except KeyError:
        await ctx.reply("Not worth it man.")
        ctx.command.reset_cooldown(ctx)
        return

      random_num = random.randint(1,3)
    
      if random_num == 1:
        amount = random.randint(0, db_target["wallet"])

        new_wallet_target = (db["wallet"][str(target.id)] - amount)
        new_wallet_author = (db["wallet"][str(ctx.author.id)] + amount)

        with open("wallet.json", "w") as f:
          json.dump(db, f, indent=4)

        if amount == 0:
          if db["dm_notifs"][str(ctx.author.id)] == True:
            embed = discord.Embed(color=discord.Color.red(), title="Someone tried to rob you!", description=f"**{ctx.author}** tried to rob you but they failed!")
            await target.send(embed=embed)
          return await ctx.reply("Too bad, you didn't steal any money. You aren't lucky for now.")

        if db["dm_notifs"][str(ctx.author.id)] == True:
          embed = discord.Embed(color=discord.Color.red(), title="Someone robbed you!", description=f"**{ctx.author}** stole **<:turtle:849453698844327936>{amount}** from you!")
          await target.send(embed=embed)
        await ctx.reply("You stole <:turtle:849453698844327936>{0} from {1}!\nNow you have <:turtle:849453698844327936>{2} and {1} has <:turtle:849453698844327936>{3}! Nice job!".format(amount, target, db_author["wallet"], db_target["wallet"]))
        self.robbed += [target.id]
        await asyncio.sleep(cooldownFiveHour)
        self.robbed.remove(target.id)
      else:
        fine = random.randint(round(int(db["wallet"][str(ctx.author.id)]))/5,round(int(db["wallet"][str(ctx.author.id)])/2))

        new_wallet_author = (int(db_author["wallet"]) - fine)
        new_wallet_target = (int(db["wallet"]) + fine)

        #with open("wallet.json", "w") as f:
          #json.dump(db, f, indent=4)
        if db["dm_notifs"][str(ctx.author.id)] == True:
          embed = discord.Embed(color=discord.Color.red(), title="Someone tried to rob you!",description=f"**{ctx.author}** tried to rob you but they failed!")
        await target.send(embed=embed)
        return await ctx.reply("You got fined <:turtle:849453698844327936>{:,} while robbing {}!".format(fine, target))

  @commands.command(aliases=['richest','toponepercent','leaderboard','lb'])
  async def rich(self,ctx):
     with open("wallet.json", "r") as f:
      db = json.load(f)

      sorted_leaderboard = []
      sort_leaderboard = sorted(db["wallet"].items(), key=lambda x: x[1], reverse=True)

      loop_count = 0
      for i in sort_leaderboard:
        if loop_count == 10:
          joined_lb = "\n".join(sorted_leaderboard)
          embed = discord.Embed(color=discord.Color.green(), title="Top 10 Richest People",description=f"Here are the top 10 richest people in fifi! This is calculated from the wallet and not the bank.").add_field(name=None, value=joined_lb)
          return await ctx.reply(embed=embed)
          break
        else:
          try:
            sorted_leaderboard.append("**" + str(await self.bot.fetch_user(i[0])) + "** - <:turtle:849453698844327936>" + str(i[1]))
            loop_count +=1
          except:
            continue

  @commands.command(aliases=['item','items'])
  async def shop(self,ctx):
    embed = discord.Embed(color=discord.Color.green(), title="Shop Items")
    embed.add_field(name="🏦 Bank - <:turtle:849453698844327936>1,000", value="Buy the bank to get 500 base bankspace and be able to expand it with banknotes.", inline = False)
    embed.add_field(name="<a:space:831341497785909308> Bank Space - <:turtle:849453698844327936>500", value="Expand your bankspace by 250 by buying Bank Space. Bank required to use Bank Space", inline = False)
    await ctx.reply(embed=embed)

  @commands.command()
  async def buy(self,ctx,item=None):
    with open("wallet.json", "r") as f:
      db = json.load(f)
    if item == None:
      await ctx.reply("Please specify the item you want to buy!")

    if item == "bankspace":

      if db["bank"][str(ctx.author.id)] == False:
        return await ctx.reply("You need to buy a bank first to expand bankspace")

      if db["wallet"][str(ctx.author.id)] < 500:
        return await ctx.reply("You do not have enough money to buy bankspace!")

      if db["wallet"][str(ctx.author.id)] >= 500 and db["bank"][str(ctx.author.id)] == True:
        db["wallet"][str(ctx.author.id)] -= 500
        db["bankspace"][str(ctx.author.id)] += 250
        with open("wallet.json", "w") as f:
          json.dump(db, f, indent=4)
        return await ctx.reply("You bought bankspace and your bankspace has been increased by <:turtle:849453698844327936>250. You now have <:turtle:849453698844327936>{:,} bankspace".format(db["bankspace"][str(ctx.author.id)]))

    if item == "bank":

      if db["bank"][str(ctx.author.id)] == True:
        return await ctx.reply("You already have a bank. If you want to expand your bank buy bankspace")

      if db["wallet"][str(ctx.author.id)] < 1000:
        return await ctx.reply("You do not have enough money to buy a bank!")

      if db["wallet"][str(ctx.author.id)] > 1000 and db["bank"][str(ctx.author.id)] == False:
        db["wallet"][str(ctx.author.id)] -= 1000
        db["bank"][str(ctx.author.id)] = True
        db["bankspace"][str(ctx.author.id)] += 500
        with open("wallet.json", "w") as f:
          json.dump(db, f, indent=4)

        return await ctx.reply("You bought a bank! You now have 500 base bankspace and can expand it with bankspace. Use `f.deposit` to put FiBucks into the bank")

    if item == "potion":

      if db["wallet"][str(ctx.author.id)] < 100:
        return await ctx.reply("You do not have enough money to buy a potion!")

      else:
        db["wallet"][str(ctx.author.id)] -= 100
        with open("battle_db.json","r") as x:
          battle_db = json.load(x)
        battle_db["potion"][str(ctx.author.id)] += 1
        potions = battle_db["potion"][str(ctx.author.id)]
        with open("wallet.json", "w") as f:
          json.dump(db, f, indent=4)
        with open("battle_db.json","w") as x:
          json.dump(battle_db, x, indent=4)

        return await ctx.reply("You bought a potion! Now you have {} potions".format(potions))
    
    else:
      return await ctx.reply("That is not an item you can buy!")

  @commands.command()
  async def give(self,ctx,target = None,amount=0):
    with open("wallet.json", "r") as f:
      db = json.load(f)
    target = str(target)
    _target = target
    target = await commands.MemberConverter().convert(ctx, target)
    if _target not in [f"<@{target.id}>", f"<@!{target.id}>"]:
      return await ctx.reply("Member not found.")
    if ctx.author == discord.User.bot:
      return await ctx.reply("Why would you even want to waste your FiBucks to give bots")
    if target == ctx.author:
      return await ctx.reply("You cannot give FiBucks to yourself!")
    if target == None:
      return await ctx.reply("Please specify who you are giving the FiBucks to")
    if amount == 0:
      return await ctx.reply("Please enter the amount of FiBucks you want to give")
    if "passive" in db:
      if str(ctx.author.id) in db["passive"]:
        if db["passive"][str(ctx.author.id)] == True:
          return await ctx.reply("You are in passive mode!")
      if str(target.id) in db["passive"]:
        if db["passive"][str(target.id)] == True:
          return await ctx.reply("They are in passive mode!")
    try:
      db["wallet"][str(ctx.author.id)]
    except KeyError:
      return await ctx.reply("You do not have enough money to give {} <:turtle:849453698844327936>{:,}".format(target,amount))
    if amount > db["wallet"][str(ctx.author.id)]:
      return await ctx.reply("You do not have enough money to give {} <:turtle:849453698844327936>{:,}".format(target,amount))
    if amount < db["wallet"][str(ctx.author.id)]:
      try:
        db["wallet"][str(ctx.author.id)] -= amount
      except:
        return await ctx.reply("You do not have enough money to give {} <:turtle:849453698844327936>{:,}".format(target,amount))
      try:
        db["wallet"][str(target.id)] += amount
      except KeyError:
        db["wallet"][str(target.id)] = amount

      with open("wallet.json", "w") as f:
        json.dump(db, f, indent=4)
      if db["dm_notifs"][str(ctx.author.id)] == True:
        embed = discord.Embed(color=discord.Color.green(), title="Someone gave you FiBucks!",description=f"**{ctx.author}** gave you **<:turtle:849453698844327936>{amount}**!")
      await target.send(embed=embed)
      return await ctx.reply("You gave <:turtle:849453698844327936>{:,} to {} \nNow you have <:turtle:849453698844327936>{:,} and they have <:turtle:849453698844327936>{:,}".format(amount,target,db["wallet"][str(ctx.author.id)],db["wallet"][str(target.id)]))
    else:
      return await ctx.reply("An error occured, please try again later.")
  
  @commands.command() #Added cooldown. Will reset every 00.00 UTC like Dank Memer. Look at the resetCooldown function.
  #@commands.cooldown(1, 86400, commands.BucketType.user)
  async def daily(self,ctx):
    daily_earning = 1000
    
    with open("wallet.json", "r") as f:
      db = json.load(f)

    if 'onDailyCooldown' not in db:
      db['onDailyCooldown'] = []

    if str(ctx.author.id) in db['onDailyCooldown']:
      return await ctx.reply(f"You have claimed your Daily Earnings in the last 24 hours. Try again later.")

    db["wallet"][str(ctx.author.id)] += daily_earning

    db["onDailyCooldown"] += [str(ctx.author.id)]
    with open("wallet.json", "w") as f:
      json.dump(db, f, indent=4)
    return await ctx.reply("You have claimed your daily and earned <:turtle:849453698844327936>{:,}. You can claim your daily again after 00:00 UTC.".format(int(daily_earning)))

  @commands.command()
  async def dm_notifs(self,ctx,option:str=None):
    with open("wallet.json", "r") as f:
      db = json.load(f)
    if option == "on":
      db["dm_notifs"][str(ctx.author.id)] = True
      return await ctx.reply("DM Notifs have been turned on!")
    if option == "off":
      db["dm_notifs"][str(ctx.author.id)] = False
      return await ctx.reply("DM Notifs have been turned off!")
    else:
      return await ctx.reply("Please specify a valid option (`on`/`off`)")

  @commands.command()
  async def passive(self,ctx,option:str=None):
    with open("wallet.json", "r") as f:
      db = json.load(f)
    if "passive" not in db:
      db["passive"] = {} #huh???? So it doesn't raise KeyError. k
    if option == "on":
      if str(ctx.author.id) in db["passive"]:
        if db["passive"][str(ctx.author.id)] is True:
          return await ctx.send("Your passive mode has been enabled since before.")
      db["passive"][str(ctx.author.id)] = True
      await ctx.reply("Passive Mode has been turned on! \n\n**NOTE: You get half the FiBucks while chatting in passive mode**")
    elif option == "off":
      if str(ctx.author.id) in db["passive"]:
        if db["passive"][str(ctx.author.id)] is False:
          return await ctx.send("Your passive mode has been disabled since before.")
      db["passive"][str(ctx.author.id)] = False
      await ctx.reply("Passive Mode has been turned off! You need to wait 12 hours to turn passive mode back on!")
      
    else:
      if option is None:
        if str(ctx.author.id) in db['passive']:
          return await ctx.reply(f"Your Passive Setting is currently {'enabled' if db['passive'][str(ctx.author.id)] else 'disabled'}.")
        else:
          return await ctx.reply("Your Passive Setting is currently disabled.")
      return await ctx.reply("Please specify a valid option (`on`/`off`)")

    with open("wallet.json", "w") as f: #We didn't dump it whyfai lol. LMAO
      json.dump(db, f, indent=4)

def setup(bot):
  bot.add_cog(Currency(bot))
  
# ty proguy
# Ur welcome :)
# Finally made currency work thanks to u :))
