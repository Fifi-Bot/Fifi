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

import os

os.system("pip install DiscordUtils")
#os.system("pip install disrank")

TOKEN = ...

import discord
from discord.ext import commands
import asyncio
import flask
from startServer import FifiServer
import json
#import thread
from context import MyContext

#class Bot(commands.Bot):
  #async def get_context(self, message, *, cls = MyContext):
    #return await super().get_context(message, cls=cls)
 
intents = discord.Intents.default()
intents.members = True 
intents.reactions
client = commands.Bot(command_prefix = 'f.', intents=intents, help_command=commands.MinimalHelpCommand(no_category = "Miscellaneous"), activity=discord.Activity(type = discord.ActivityType.playing, name = 'f.help | Helping the Server | https://discord.gg/3c5kc8M'), owner_ids=[621266489596444672, 699839134709317642, 737478714048380939], case_insensitive=True)
#client.remove_command('help')

server = FifiServer(client)
 
guild_id_error = 'You have no permission to use this bot in your server!' 

newLine = "\n"
 
@client.event
async def on_ready():
    print(f'{client.user} Has Logged In And Is Online!')

@client.event
async def on_guild_join(guild): #To block guilds from joining
  for channel in guild.text_channels:
    try:
      await channel.send("Sorry, this server is not whitelisted.")
      break
    except:
      pass

  await guild.leave()

import aiohttp

client.session = aiohttp.ClientSession()

import discord
from discord.ext import commands
from discord.utils import get

import asyncio
import random
import DiscordUtils

client.DiscordUtilsInviter = DiscordUtils.InviteTracker(client)

os.system("pip install discord-flags")

with open('BadWords.txt', 'r') as f:
    global badwords  # You want to be able to access this throughout the code
    words = f.read()
    badwords = words.split()

@client.event
async def on_message(message):
  #ctx = await client.get_context(message)
  #await client.invoke(ctx)
  with open("database.json", "r") as f:
    db = json.load(f)
  if str(message.author.id) not in db["swear_count"]:  
    db["swear_count"][str(message.author.id)] = 0
  if message.guild is None:
    return
  msg = message.content.lower()
  if message.author.bot:
    return
  for word in badwords:
      if word in msg:
        await message.channel.send("Hello FiFi here, so this dude sweared so he got muted by my friend Carl Bot. Don't be like this dude.")
        if db["swear_count"][str(message.author.id)] == 2:
          top_role = message.author.roles[-1]
          await message.author.remove_roles(top_role)
          await message.reply("You have been demoted due to swearing too many times")
          db["swear_count"][str(message.author.id)] = 0
        else:
          db["swear_count"][str(message.author.id)] += 1
        break
  if client.user.mentioned_in(message):
        await message.channel.send("My prefix is `f.`, Run `f.help` for more info.")  
  with open("database.json", "w") as f:
          json.dump(db, f, indent=4)

  await client.process_commands(message)

#@client.event
#async def on_voice_state_update(member, before, after):
    #if before == None and after is not None:
      #try:
        #role = discord.utils.get(guild.roles, #name=after.name)
        #await member.add_roles(role)
      #except:
        #pass
    #if before is not None and after == None:
      #try:
        #role = discord.utils.get(guild.roles, name=before.name)
        #await member.remove_roles(role)
      #except:
        #pass
    #if before is not None and after is not None:
      #try:
        #role = discord.utils.get(guild.roles, name=after.name)
        #await member.add_roles(role)
      #except:
        #pass
      #try:
        #role = discord.utils.get(guild.roles, name=before.name)
        #await member.add_roles(role)
      #except:
        #pass

@client.event
async def on_raw_reaction_add(payload):
  if payload.message_id == None:
    pass

# ---------------------------- VARS ----------------------------
client.baseURL = "https://fifi.ayomerdeka.com"
client.baseURLwithoutHttps = client.baseURL[8:]

# ---------------------------- MAIN GROUP ----------------------------

@client.group(aliases = ['site', 'sites', 'domains', 'link', 'links'], invoke_without_command = True)
async def domain(ctx):
  if ctx.invoked_subcommand is None:
    return await ctx.reply(f"{client.baseURL}/")

# ---------------------------- MAIN SUBCOMMANDS (FIFI) ----------------------------

@domain.command(name = "status", aliases = ['stats'])
async def __status(ctx):
  await ctx.reply(f"{client.baseURL}/status/")

@domain.command(name = "commands", aliases=['command'])
async def _commands(ctx):
  await ctx.reply(f"{client.baseURL}/commands/")

@domain.command(aliases=['support', 'server'])
async def guild(ctx):
  await ctx.reply(f"{client.baseURL}/support/")

@domain.command(aliases=['invites'])
async def invite(ctx):
  await ctx.reply(f"{client.baseURL}/invite/")

# ---------------------------- RICO ----------------------------

@domain.group(invoke_without_command = True)
async def rico(ctx):
  if ctx.invoked_subcommand is None:
    return await ctx.reply(f"https://rico.{client.baseURLwithoutHttps}/")

@rico.command(name = "status", aliases = ['stats'])
async def _status(ctx):
  await ctx.reply(f"https://rico.{client.baseURLwithoutHttps}/status/")

@rico.command(name = "commands", aliases=['command'])
async def __commands(ctx):
  await ctx.reply(f"https://rico.{client.baseURLwithoutHttps}/commands/")

@rico.command(name = "guild", aliases=['support', 'server'])
async def _guild(ctx):
  await ctx.reply(f"https://rico.{client.baseURLwithoutHttps}/support/")

@rico.command(name = "invite", aliases=['invites'])
async def _invite(ctx):
  await ctx.reply(f"https://rico.{client.baseURLwithoutHttps}/invite/")
  
# ---------------------------- KOKONUTZ ----------------------------

@domain.group(invoke_without_command = True)
async def kokonutz(ctx):
  if ctx.invoked_subcommand is None:
    return await ctx.reply(f"https://kokonutz.{client.baseURLwithoutHttps}/")

@kokonutz.command(name = "status", aliases = ['stats'])
async def _status(ctx):
  await ctx.reply(f"https://kokonutz.{client.baseURLwithoutHttps}/status/")

@kokonutz.command(name = "commands", aliases=['command'])
async def __commands(ctx):
  await ctx.reply(f"https://kokonutz.{client.baseURLwithoutHttps}/commands/")

@kokonutz.command(name = "guild", aliases=['support', 'server'])
async def _guild(ctx):
  await ctx.reply(f"https://kokonutz.{client.baseURLwithoutHttps}/support/")

@kokonutz.command(name = "invite", aliases=['invites'])
async def _invite(ctx):
  await ctx.reply(f"https://kokonutz.{client.baseURLwithoutHttps}/invite/")
  
# ---------------------------- OWO MAN ----------------------------

@domain.group(invoke_without_command = True)
async def owo(ctx):
  if ctx.invoked_subcommand is None:
    return await ctx.reply(f"https://owo.{client.baseURLwithoutHttps}/")

@owo.command(name = "status", aliases = ['stats'])
async def _status(ctx):
  await ctx.reply(f"https://owo.{client.baseURLwithoutHttps}/status/")

@owo.command(name = "commands", aliases=['command'])
async def __commands(ctx):
  await ctx.reply(f"https://owo.{client.baseURLwithoutHttps}/commands/")

@owo.command(name = "guild", aliases=['support', 'server'])
async def _guild(ctx):
  await ctx.reply(f"https://owo.{client.baseURLwithoutHttps}/support/")

@owo.command(name = "invite", aliases=['invites'])
async def _invite(ctx):
  await ctx.reply(f"https://owo.{client.baseURLwithoutHttps}/invite/")

# ---------------------------- 6721 ----------------------------

@domain.group(invoke_without_command = True)
async def 6721(ctx):
  if ctx.invoked_subcommand is None:
    return await ctx.reply(f"https://6721.{client.baseURLwithoutHttps}/")

@6721.command(name = "status", aliases = ['stats'])
async def _status(ctx):
  await ctx.reply(f"https://6721.{client.baseURLwithoutHttps}/status/")

@6721.command(name = "commands", aliases=['command'])
async def __commands(ctx):
  await ctx.reply(f"https://6721.{client.baseURLwithoutHttps}/commands/")

@6721.command(name = "guild", aliases=['support', 'server'])
async def _guild(ctx):
  await ctx.reply(f"https://6721.{client.baseURLwithoutHttps}/support/")

@6721.command(name = "invite", aliases=['invites'])
async def _invite(ctx):
  await ctx.reply(f"https://6721.{client.baseURLwithoutHttps}/invite/")
  


@client.event
async def on_member_join(member):
  if member.guild.id == 720991608425807932:
    channel = client.get_channel(747728526505017424)
    await channel.send(f"<a:ablobjoin:829985443399467018> Oh look, Someone Joined! {member.mention}, Welcome to M.S. Lounge!")
    inviter = await client.DiscordUtilsInviter.fetch_inviter(member=member) #Noice
    with open("wallet.json", "r") as f:
      db = json.load(f)
    if not member.bot: #Isn't this easy whyfai.......
      db["wallet"][str(inviter.id)] += 2000
    with open("wallet.json", "w") as f:
      json.dump(db, f, indent=4)

@client.event
async def on_member_remove(member):
  channel = client.get_channel(747728526505017424)
  await channel.send(f"<a:blobstab:831016560273260604> Breaking News! Member {member.mention} just died by being stabbed, than killed, than burnt while celebrating their birthday with their family. Brutal.")
  inviter = await DiscordUtils.InviteTracker.fetch_inviter(member)
  with open("wallet.json", "r") as f:
    db = json.load(f)
    if not member.bot: #Isn't this easy whyfai.......
      db["wallet"][str(inviter.id)] -= 2000
    with open("wallet.json", "w") as f:
      json.dump(db, f, indent=4)

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    await ctx.send(f'This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds')
  else: #why whyfai
    await ctx.reply("Uh oh. An error occured. If this happens multiple times please contact whyfai for assistance.")
    raise error #why whyfai

from discord.ext import tasks

@tasks.loop(minutes=10)
async def downloadProfile():
  pfp = client.avatar_url.save("profile.png")

@downloadProfile.before_loop
async def before_downloadProfile():
  await client.wait_until_ready()

@client.command()
async def ping(ctx):
    await ctx.reply('Calculating Ping. Please Wait')
    await asyncio.sleep(3)
    await ctx.reply(f'My Ping/Latency to Servers is `{round(client.latency * 1000)}ms`')

@client.command(aliases = ['c', 'purge'])
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = 0):
        if amount == 0:
            await ctx.channel.reply('Please provide a number of which I can purge/clear please (1-2000)')
            return
        elif amount >= 2000:
            await ctx.channel.reply('Please provide a number under 2000 for me to purge/clear. Thank you!')
            return
        else:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f'Cleared {amount} messages.')
            await asyncio.sleep(3)
            await ctx.channel.purge(limit=1)
            return
        return

@client.command(aliases = ['developers','devs','credit'])
async def credits(ctx):
    embed = discord.Embed(title = 'Credits!', description = 'Here are the credits!', color = discord.Color.green())

    embed.add_field(name = 'Creator: ', value = 'whyfai#0777', inline = False)
    embed.add_field(name = 'Assistant Creator', value = 'proguy914629#5419', inline = False)
    embed.add_field(name = 'Server Owner', value = 'DinDin#5525', inline = False)
    embed.set_footer(text = 'Bot Username: fifi#9797')
    await ctx.reply(embed=embed)

#@client.command(aliases = ['h'])
async def help(ctx):
    embed = discord.Embed(title = 'Commands Help', description = 'Here are the Commands for this bot', color = discord.Color.green())

    embed.add_field(name = 'Help', value = 'Shows This Message', inline = False)
    embed.add_field(name = 'Ping', value = 'Shows Ping/latency of the Bot', inline = False)
    embed.add_field(name = 'Clear/Purge', value = 'Clears/purges a specific amount of messages',inline = False)
    embed.add_field(name = 'Credits', value = 'Shows who helped create the bot')
    embed.set_footer(text = 'Hope you enjoy the bot!')
    await ctx.reply(embed=embed) 

allbadges = [{"name":"👑 Heroic Patriot Badge 👑", "description":"Get all the badges"},
             {"name":"💪 Patriot Badge", "description":"Get most of the badges"},
             {"name":"-⚜Classic Badge⚜-", "description":"Be in the server since the first revamp (Spongebob Fans)"},
             {"name":"Mission: Accomplished", "description":"Finish the 150 Member Special (Coming Soon)"},
             {"name":"MS Badge", "description":"Be in the server since Meme Studios V1"},
             {"name":"🎊 Contest Winner 🥳", "description":"Win an event (in <#814013411985063957>)"},
             {"name":"🤺Tournament Win Badge🤺", "description":"Win a Tournament"}]


@client.command(aliases = ['badges','badge'])
async def badgelist(ctx,*,args=None):
    if args == None or 'all':
        embed = discord.Embed(
            title = 'Badges',
            description = 'Here are all the badges in this server!',
            color = discord.Color.green()
        )
        for item in allbadges:
            name = item["name"]
            description = item["description"]
            embed.add_field(name = name, value = f'{description}')

    await ctx.reply(embed = embed)

@client.command()
async def history(ctx):
  embed1 = discord.Embed(color=discord.Color.green(), title="🌉 Meme Studios History 🌉").add_field(name="Before the server: 14 May 2020", value="Gamers Died")
  embed2 = discord.Embed(color=discord.Color.green(), title="🌉 Meme Studios History 🌉").add_field(name="June 12th 2020:", value="The server was borned.")
  embed3 = discord.Embed(color=discord.Color.green(), title='🌉 Meme Studios History 🌉').add_field(name="First Appearance:", value="This server was used to be a Spongebob fan server and it was my first server created. It was rarely used and only has 6 members. But it was the beginning. This was also when one of my best friends teached me using Discord. He left, hopefully he will comeback. I fyou remember Dr.French you're old.")
  embed4 = discord.Embed(color=discord.Color.green(), title='🌉 Meme Studios History 🌉').add_field(name="Second Revamp: Meme Studios V1:", value="The first sucsesful revamp was this appearance. We made a lot of changes and this was also the end of people who got the Classic badge. Sadly most of the OG members are dying but we are happy to see some of you who have been here since the start. The late days of M.S. 1 was the start of lands and lounges. Originnaly we had 5 lounges for diffrent types of music. We would also made the server like a studio so their would be a podcast recording studio and such more.")
  embed5 = discord.Embed(color=discord.Color.green(), title="🌉 Meme Studios History 🌉").add_field(name="Third revamp:", value="The Meme Studios part of the server was a big change and it was divided to 2 revamps. This revamp was when the lounges was a big hit and we made more and there was 5 more lounges. One of them was the GT Lounge. This would also be the time that @whyfai  destroyed the server because his own server got destroyed but that would be a other story. Long story short whyfai started destroying the server a lot of times but he started to became nice and now he became Co-founder. We also made a 2nd server called court. But it was sectryed by whyfai.The irony is HARD. Whyfai was also competing this server with his own server that now is dead. Gamers 1,2,3,4,5, and BotWorld. Bot world was also a parody of our old (deleted) channels called BotWorld. Sadly after this the server started dying.")
  embed6 = discord.Embed(color=discord.Color.green(), title="🌉 Meme Studios History 🌉").add_field(name="Fourth Revamp: GT:", value="Remember when I told you about the original lounges, they consisted of Jazzy. Turtle Lounge, Pop T. Lounge, Rock.T. Lounge, 5 Star hotel, and the trash bin. This was also when another server was created by me called the M.S. Lounge. It was a server that was like a lounge and I changed this server to DownTown GT. It was a roleplay server that I made buildings like barbershops, shopping malls and more. But I realized that why should I do all the work if I can make my members do that! So I made people pay 15k DMC to buy land. This was also the time when I changed the server name to GT. People who changed the server and helped: @whyfai @admin named evan Famous lands: Whyfai centre, dankfrog's lands, TheLaughbale Hotel (it was the first land), MacCafe, and more. And, badges was also released. The first badge was created at Halloween.")
  embed7 = discord.Embed(color=discord.Color.green(), title="🌉 Meme Studios History 🌉").add_field(name="Fifth Revamp: Meme Studios v2:", value="Their wasn't much in M.S.2 because I felt bad because I missed how old M.S. was such a big sucsess so there wasn't  much changes.")
  embed8 = discord.Embed(color=discord.Color.green(), title="🌉 Meme Studios History 🌉").add_field(name="Sixth Revamp: Earth:", value="Earth was a server that me and whyfai created because GT was dying but we kept everyones lands. We changes the land concept to buying countries because it was Earth.  Thank whyfai for the idea of the countries. I took a while so people got bored. There weren't a lot of changes but a lot of dudes who was good at tech stuff add chanell bot and the click me channel. Don't thank me, tech dudes was not me. After the countries got old, whyfai had a good idea to made country landmarks. It didn't last very long because I was in the middle of another revamp.")
  embed9 = discord.Embed(color=discord.Color.green(), title="🌉 Meme Studios History 🌉").add_field(name="Seventh Revamp:", value=" M.S.Lounge was the next revamp. DinDin wanted to made the server a comfartable lounge so people can chat. I decided to made it as less as channel as possible. I realized one of the main problems are people who don't know how to chat. They were confuse where to chat. So I made the server as least as possible.")
  embed10 = discord.Embed(color=discord.Color.green(), title="🌉 Meme Studios History 🌉").add_field(name="Another story.. \nOne day... At 10/2/2021 in 12:00 GMT+7.....", value="@whyfai Was pretty mad at @SANS because of some inappropriate stuff. He was then mad to other innocent people such as @Mas Agus Indihome, and started to have a mental breakdown. Then he raided the server and almost banned innocents. He also banned multiple bots such as @VoiceMaster and @ChannelBot. He got muted, and we kicked his bot, WhyBot. The End. When we are writing this story and SANS is banned. Whyfai has been relaxing for 3 days and his admin will be give him back (story by proguy) \n3/3/2021: WhyFai had another breakdown he massban a lot of ppl and we are still missing somebody until now. COBRAZ CHRIST has been founded.")
  embed11 = discord.Embed(color=discord.Color.green(), title="🌉 Meme Studios History 🌉").add_field(name="3/3/2021:", value=" WhyFai had another breakdown he massban a lot of ppl and we are still missing somebody until now. Edit: COBRAZ CHRIST has been found.")
  embed12 = discord.Embed(color=discord.Color.green(), title="🌉 Meme Studios History 🌉").add_field(name="The week of depression, 20/4/2021:",value="Faith has left. Before this happened sadness has already started to begun. A lot of people are affected by this. Some like Faith herself, Maxiee, Nused, and more. The reason of this is because Max can't open and ######. This was caused because of ########. I'm not sure if I can tell the rest of the story.")
  paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx,auto_footer=True)
  embeds = [embed1, embed2, embed3,embed4,embed5,embed6,embed7,embed8,embed9,embed10,embed11,embed12]
  await paginator.run(embeds)

@client.group(invoke_without_command = True)
async def book(ctx):
  if ctx.invoked_subcommand is None:
    return await ctx.reply("Please use `f.book hotel` to purchase a hotel")

@book.command()
async def hotel(ctx):
  msg = ctx.reply("Do you want to buy a hotel room?")
  confirm = await ctx.confirmWithoutMessage(msg)
  if confirm == True:
    msg = ctx.send("Which hotel room do you want? #️⃣:Normal Hotel (Text Only) \n🔊:Normal Hotel (Voice Only) \n🛏️:Suite (Text and Voice)")
    hotel_choice = await ctx.three_rr(msg)
    if hotel_choice[0] in ["#️⃣","🔊","🛏️"]:
      hotel_type = hotel_choice[0]
      msg = ctx.send("Are you sure you want to buy a room?")
      confirm = await ctx.confirmWithoutMessage(msg)
      if confirm == True:
        await ctx.send("Your request to buy a hotel room is sent!")
        whyfai_user = await client.fetch_user(621266489596444672)
        return await whyfai_user.send(f"{ctx.author} has requested to buy a {hotel_type} hotel!")
      else:
        ctx.reply("Cancelling...")
    else:
      ctx.reply("Cancelling...")
  else:
    ctx.reply("Cancelling...")


@client.command()
async def dm_test(ctx):
  await ctx.author.send("test")

#@client.command()
#async def donate(ctx,length,winners,req,prize,message):
  #await ctx.send(discord.Guild.get_role.mention(761814027663441921))
  #embed = discord.Embed(title = 'Giveaway Donation!', description = f'{ctx.author.mention} wants to donate!', color = discord.Color.purple())

  #embed.add_field(name = '🕘 Length', value ='\u200b',  inline = False)
  #embed.add_field(name = '🥇 Winners', value = winners, inline = False)  
  #embed.add_field(name = '📃 Requirements', value = req, inline = False)
  #embed.add_field(name = 'Credits', value = 'Shows who helped create the bot')
  #embed.set_footer(text = 'Hope you enjoy the bot!')
  #await ctx.reply(embed=embed) 

#@client.event
#async def on_message(message):
    #if client.user.mentioned_in(message):
        #await message.channel.send("My prefix is `f.`, Run `f.help` for more info.")

@client.command(aliases = ['reboot'])
async def restart(ctx):
  if ctx.author.id == 621266489596444672 or ctx.author.id == 699839134709317642 or ctx.author.id == 737478714048380939:
      #channel = ctx.message.channel
      await ctx.reply('Bot is restarting!')
      #discord.Client.change_presence(status=discord.Status.idle, activity=discord.Playing('The Bot is Restarting!'))
      #await asyncio.sleep(5)
      await client.close()
      os.system("python3 main.py")
      await client.wait_until_ready()
      #await channel.reply('Bot has successfully restarted!')
  else:
      await ctx.reply('Only the developers can restart the bot!')

    #from discord.ext import commands

extensions = [
  "cogs.music",
  "cogs.currency",
  "cogs.reddit",
  "cogs.webhook",
  "cogs.wc",
  "cogs.battlefield"
]

import jishaku

if __name__ in "__main__":
    server.start()
    for ext in extensions:
      client.load_extension(ext)
    #yessssss........
    #client.load_extension('cogs.reddit')
    client.load_extension("jishaku")

import asyncpg, os

#try:
  #client.pool = asyncio.get_event_loop().run_until_complete(asyncpg.create_pool(os.getenv("DATABASE-URI")))
#except OSError:
client.pool = asyncio.get_event_loop().run_until_complete(asyncpg.create_pool(host=os.getenv("DATABASE-HOST"), port=os.getenv("DATABASE-PORT"), user=os.getenv("DATABASE-USER"), password=os.getenv("DATABASE-PASS")))

async def create_tables():
  await client.pool.execute("""
  CREATE TABLE IF NOT EXISTS economy (
    user_id TEXT,
    wallet TEXT,
    amt_in_bank TEXT,
    bankspace TEXT,
    passive boolean,
    claimed_daily boolean
  )
  """)

client.loop.create_task(create_tables())

client.run(TOKEN)
