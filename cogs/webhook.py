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
import aiohttp
import asyncio
import shlex
import re
import argparse
import sys
from discord.ext import commands
from discord.ext import flags
from discord.ext.flags import FlagCommand, _parser


class SFlagCommand(FlagCommand):
    async def _parse_flag_arguments(self, ctx):
        if not hasattr(self.callback, '_def_parser'):
            return
        arg = ctx.view.read_rest()
        arguments = shlex.split(arg)
        if hasattr(self.callback._def_parser, "optional"):
            for x, y in enumerate(arguments):
                if "--" in y and "--" in arguments[min(len(arguments) - 1, x+1)]:
                    for p, q in self.callback._def_parser.optional:
                        y = y.replace(p, q)
                    arguments[x] = y
        namespace = self.callback._def_parser.parse_args(arguments, ctx=ctx)
        flags = vars(namespace)

        async def do_convertion(value):
            # Would only call if a value is from _get_value else it is already a value.
            if type(value) is _parser.ParserResult:
                try:
                    value = await discord.utils.maybe_coroutine(value.result)

                # ArgumentTypeErrors indicate errors
                except argparse.ArgumentTypeError:
                    msg = str(sys.exc_info()[1])
                    raise argparse.ArgumentError(value.action, msg)

                # TypeErrors or ValueErrors also indicate errors
                except (TypeError, ValueError):
                    name = getattr(value.action.type, '__name__', repr(value.action.type))
                    args = {'type': name, 'value': value.arg_string}
                    msg = 'invalid %(type)s value: %(value)r'
                    raise argparse.ArgumentError(value.action, msg % args)
            return value

        for flag, value in flags.items():
            # iterate if value is a list, this happens when nargs = '+'
            if type(value) is list:
                values = [await do_convertion(v) for v in value]
                value = " ".join(values) if all(isinstance(v, str) for v in values) else values
            else:
                value = await do_convertion(value)
            flags.update({flag: value})

        for x in flags.copy():
            if hasattr(self.callback._def_parser, "optional"):
                for val, y in self.callback._def_parser.optional:
                    y = re.sub("-", "", y)
                    if y == x and flags[y]:
                        flags.update({re.sub("-", "", val): True})
        ctx.kwargs.update(flags)

    @property
    def signature(self):
        return self.old_signature


class SFlagGroup(SFlagCommand, commands.Group):
    pass


def add_flag(*flag_names, **kwargs):
    def inner(func):
        if isinstance(func, commands.Command):
            nfunc = func.callback
        else:
            nfunc = func

        if any("_OPTIONAL" in flag for flag in flag_names):
            raise Exception("Flag with '_OPTIONAL' as it's name is not allowed.")

        if not hasattr(nfunc, '_def_parser'):
            nfunc._def_parser = _parser.DontExitArgumentParser()
            nfunc._def_parser.optional = []

        if all(x in kwargs for x in ("type", "action")):
            _without = kwargs.copy()
            if _type := _without.pop("type"):
                if _type is not bool:
                    raise Exception(f"Combination of type and action must be a bool not {type(_type)}")
            kwargs.pop("action")
            optional = [f'{x}_OPTIONAL' for x in flag_names]
            nfunc._def_parser.optional += [(x, f'{x}_OPTIONAL') for x in flag_names]
            nfunc._def_parser.add_argument(*optional, **_without)

        nfunc._def_parser.add_argument(*flag_names, **kwargs)
        return func
    return inner

async def delete_quietly(ctx: commands.Context):
    if ctx.channel.permissions_for(ctx.me).manage_messages:
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

class InvalidWebhook(Exception):
    pass

async def delete_quietly(ctx: commands.Context):
    if ctx.channel.permissions_for(ctx.me).manage_messages:
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

class FakeResponse:
    def __init__(self):
        self.status = 403
        self.reason = "Forbidden"



class Webhook(commands.Cog):
    """Webhook Utility Commands"""

    __author__ = "proguy914629"

    def __init__(self, bot):
        self.bot = bot
        self.cache = {}
        self.session = aiohttp.ClientSession()

    async def get_webhook(
        self,
        *,
        channel: discord.TextChannel = None,
        me: discord.Member = None,
        author: discord.Member = None,
        reason: str = None,
        ctx: commands.Context = None,
    ) -> discord.Webhook:
        if ctx:
            channel = channel or ctx.channel
            me = me or ctx.me
            author = author or ctx.author
            reason = (reason or f"For the {ctx.command.qualified_name} command",)

        if webhook := self.cache.get(channel.id):
            return webhook
        if me and not channel.permissions_for(me).manage_webhooks:
            raise discord.Forbidden(
                FakeResponse(),
                f"I need permissions to `manage_webhooks` in #{channel.name}.",
            )
        chan_hooks = await channel.webhooks()
        webhook_list = [w for w in chan_hooks if w.type == discord.WebhookType.incoming]
        if webhook_list:
            webhook = webhook_list[0]
        else:
            creation_reason = f"Webhook creation requested by {author} ({author.id})"
            if reason:
                creation_reason += f" Reason: {reason}"
            if len(chan_hooks) == 10:
                await chan_hooks[-1].delete()
            webhook = await channel.create_webhook(
                name=f"{me.name} Webhook",
                reason=creation_reason,
                avatar=await me.avatar_url.read(),
            )
        self.cache[channel.id] = webhook
        return webhook

    async def webhook_link_send(
        self,
        link: str,
        username: str,
        avatar_url: str,
        *,
        allowed_mentions: discord.AllowedMentions = discord.AllowedMentions(
            users=False, everyone=False, roles=False
        ),
        **kwargs,
    ):
        try:
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(
                    link, adapter=discord.AsyncWebhookAdapter(session)
                )
                await webhook.send(
                    username=username,
                    avatar_url=avatar_url,
                    allowed_mentions=allowed_mentions,
                    **kwargs,
                )
                return True
        except (discord.InvalidArgument, discord.NotFound):
            raise InvalidWebhook("You need to provide a valid webhook link.")

    async def send_to_channel(
        self,
        channel: discord.TextChannel,
        me: discord.Member,
        author: discord.Member,
        *,
        reason: str = None,
        ctx: commands.Context = None,
        allowed_mentions: discord.AllowedMentions = discord.AllowedMentions(
            users=False, everyone=False, roles=False
        ),
        **kwargs,
    ):
        """Cog function that other cogs can implement using `bot.get_cog("Webhook")`
        for ease of use when using webhooks and quicker invokes with caching."""
        while True:
            webhook = await self.get_webhook(
                channel=channel, me=me, author=author, reason=reason, ctx=ctx
            )
            try:
                await webhook.send(allowed_mentions=allowed_mentions, **kwargs)
            except (discord.InvalidArgument, discord.NotFound):
                del self.cache[channel.id]
            else:
                return True

    async def edit_webhook_message(self, link: str, message_id: int, json: dict):
        async with self.session.patch(
            f"{link}/messages/{message_id}",
            json=json,
            headers={"Content-Type": "application/json"},
        ) as response:
            response = await response.json()
            return response

    @commands.group()
    @commands.guild_only()
    async def webhook(self, ctx : commands.Context):
        """Webhook Related Commands."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help("Webhook")

    @webhook.command()
    @commands.bot_has_guild_permissions(manage_webhooks=True)
    @commands.has_guild_permissions(manage_webhooks=True)
    async def create(self, ctx : commands.Context, channel : discord.TextChannel = None, name : str = None):
        """
        Creates a webhook in the channel specified with the name specified. If no channel is specified then it will default to the current channel.
        """
        
        channel = channel or ctx.channel
        name = name or f"{ctx.bot.user.name} Webhook"
        creation_reason = f"Webhook creation requested by {ctx.author} ({ctx.author.id})"
        webhook = await channel.create_webhook(name=name, reason=creation_reason)
        await ctx.message.add_reaction("✅")
        embed = discord.Embed()
        embed.title = "Webhook Sucsessfully Created in {}!".format(ctx.guild.name)
        embed.add_field(name = "Name:", value = webhook.name)
        embed.add_field(name = "URL:", value = f"{str(webhook.url)}")
        embed.add_field(name = "Token:", value = f"{str(webhook.token)}")
        embed.add_field(name = "For Channel:", value = f"{webhook.channel.mention} - {webhook.channel.name}")
        embed.add_field(name = "Created At:", value = f"{webhook.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
        await ctx.author.send(embed=embed)

    @webhook.command()
    @commands.has_guild_permissions(manage_webhooks=True)
    async def send(self, ctx : commands.Context, webhook_link : str, *, message : str):
        """Sends a message to the specified webhook using your avatar and display name."""
        await delete_quietly(ctx)
        try:
            await self.webhook_link_send(
                webhook_link, ctx.author.display_name, ctx.author.avatar_url, content=message
            )
        except InvalidWebhook:
            await ctx.send("You need to provide a valid webhook link.")

    @webhook.command()
    @commands.bot_has_guild_permissions(manage_webhooks=True)
    async def say(self, ctx : commands.Context, *, message : str):
        """Sends a message to the specified webhook using your avatar and display name."""
        await delete_quietly(ctx)
        await self.send_to_channel(
            ctx.channel,
            ctx.me,
            ctx.author,
            ctx=ctx,
            content=message,
            avatar_url=ctx.author.avatar_url,
            username=ctx.author.display_name,
        )

    @webhook.command()
    #@commands.has_guild_permissions(manage_webhooks=True)
    #@commands.bot_has_guild_permissions(manage_webhooks=True)
    async def sudo(self, ctx : commands.Context, member : discord.Member, *, message : str):
        """Sends a message to the channel as a webhook with the specified member's avatar and display name."""
        await delete_quietly(ctx)
        await self.send_to_channel(
            ctx.channel,
            ctx.me,
            ctx.author,
            ctx=ctx,
            content=message,
            avatar_url=member.avatar_url,
            username=member.display_name,
        )

    @webhook.command()
    @commands.has_guild_permissions(manage_webhooks=True, manage_guild=True)
    @commands.bot_has_guild_permissions(manage_webhooks=True)
    async def loudsudo(self, ctx : commands.Context, member : discord.Member, *, message : str):
        """Sends a message to the channel as a webhook with the specified member's avatar and display name."""
        await self.send_to_channel(
            ctx.channel,
            ctx.me,
            ctx.author,
            ctx=ctx,
            content=message,
            avatar_url=member.avatar_url,
            username=member.display_name,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True),
        )

    @webhook.command()
    @commands.has_guild_permissions(manage_webhooks=True, manage_guild=True)
    @commands.bot_has_guild_permissions(manage_webhooks=True)
    async def clyde(self, ctx: commands.Context, *, message: str):
        """Sends a message to the channel as a webhook with Clyde's avatar and name."""
        await delete_quietly(ctx)
        await self.send_to_channel(
            ctx.channel,
            ctx.me,
            ctx.author,
            ctx=ctx,
            content=message,
            avatar_url="https://discordapp.com/assets/f78426a064bc9dd24847519259bc42af.png",
            username="C​I​​​​​​y​d​e",
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True),
        )

    @webhook.command(aliases = ['del', 'delete'])
    @commands.has_guild_permissions(manage_webhooks=True)
    @commands.bot_has_guild_permissions(manage_webhooks=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def clear(self, ctx, channel : discord.TextChannel = None):
        """Delete all webhooks in the server. If `channel` is None, it deletes all the webhooks in the guild."""
        if channel == None:
            webhooks = await channel.webhooks()
            if not webhooks:
                await ctx.send("There are no webhooks in {}!".format(channel.mention))
                return

            msg = await ctx.send(
                f"This will delete all webhooks in {channel.mention}. Are you sure you want to do this?"
            )
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message == msg

            try:
                response = await self.bot.wait_for("reaction_add", check = check, timeout = 60.0)
            except asyncio.TimeoutError:
                await ctx.send("Action Cancelled. Reason: Took to long.")
                return

            if response.emoji == "❌":
                return await ctx.send("Action Cancelled.")
            
            msg = await ctx.send("Deleting Webhooks..")
            count = 0
            async with ctx.typing():
                for webhook in webhooks:
                    try:
                        await webhook.delete(
                            reason=f"Guild Webhook Deletion requested by {ctx.author} ({ctx.author.id})"
                        )
                    except discord.InvalidArgument:
                        pass
                    else:
                        count += 1
            try:
                await msg.edit(content=f"{count} Webhooks Deleted.")
            except discord.NotFound:
                await ctx.send(f"{count} Webhooks Deleted.")
            return

        webhooks = await ctx.guild.webhooks()
        if not webhooks:
            await ctx.send("There are no webhooks in this server!")
            return

        msg = await ctx.send(
            "This will delete all webhooks in the server. Are you sure you want to do this?"
        )
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check2(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message == msg

        try:
            response = await self.bot.wait_for("reaction_add", check = check2, timeout = 60.0)
        except asyncio.TimeoutError:
            await ctx.send("Action Cancelled. Reason: Took to long.")
            return

        if response.emoji == "❌":
            return await ctx.send("Action Cancelled.")
        
        msg = await ctx.send("Deleting Webhooks..")
        count = 0
        async with ctx.typing():
            for webhook in webhooks:
                try:
                    await webhook.delete(
                        reason=f"Guild Webhook Deletion requested by {ctx.author} ({ctx.author.id})"
                    )
                except discord.InvalidArgument:
                    pass
                else:
                    count += 1
        try:
            await msg.edit(content=f"{count} Webhooks Deleted.")
        except discord.NotFound:
            await ctx.send(f"{count} Webhooks Deleted.")

    @webhook.command(aliases = ['perms', 'perm', 'permission'], cls=SFlagCommand)
    @add_flag("--role", type=bool, action="store_true", default=False, help = "Shows the roles with the `Manage Webhooks` permissions instead of the users. Accepts True or False, defaults to False if not stated.")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def permissions(self, ctx : commands.Context, **flags):
        """Show all members in the server that have `manage webhook` permissions."""
        await ctx.trigger_typing()
        members = []
        strings = []
        roles = []
        for role in ctx.guild.roles:
            if role.permissions.is_superset(
                discord.Permissions(536870912)
            ) or role.permissions.is_superset(discord.Permissions(8)):
                roles.append(role)
                for member in role.members:
                    if member not in members:
                        members.append(member)
                        string = (
                            f"{member.mention}"
                        )
                        strings.append(string)
        if not members:
            await ctx.send("No one here has `manage webhook` permissions other than the owner.")

        users = flags.pop("role", False)
        if users == False:
            strings = "\n".join(strings)
            l = strings.split()
            n = 100
            contents = ['\n'.join(l[x:x+n]) for x in range(0, len(l), n)]
            pages = len(contents)
            cur_page = 1
            embed = discord.Embed(
                color=ctx.color,
                title="Users with \"Manage Webhook\" Permissions:",
                description=f"{contents[cur_page-1]}",
                timestamp = ctx.message.created_at
            )
            embed.set_author(
                name = "Page {}/{}:".format(cur_page, pages)
            )
            msg = await ctx.send(embed=embed)
            def checkuser(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['<a:facing_left_arrow:799579706688667669>', '<a:facing_right_arrow:799579865296535583>', '⏹️'] and reaction.message == msg

            await msg.add_reaction("<a:facing_left_arrow:799579706688667669>")
            await msg.add_reaction("<a:facing_right_arrow:799579865296535583>")
            await msg.add_reaction("⏹️")

            while True:
                try:
                    reaction, user = await ctx.bot.wait_for("reaction_add", timeout = 60.0, check=checkuser)

                    if str(reaction.emoji) == "<a:facing_right_arrow:799579865296535583>" and cur_page != pages:
                        cur_page += 1
                        await msg.remove_reaction(reaction, user)
                        embed = discord.Embed(
                            color=ctx.color,
                            title="Users with \"Manage Webhook\" Permissions:",
                            description=f"{contents[cur_page-1]}",
                            timestamp = ctx.message.created_at
                        )
                        embed.set_author(
                            name = "Page {}/{}:".format(cur_page, pages)
                        )
                        await msg.edit(embed=embed)
                    elif str(reaction.emoji) == "<a:facing_left_arrow:799579706688667669>" and cur_page > 1:
                        cur_page -= 1
                        await msg.remove_reaction(reaction, user)
                        embed = discord.Embed(
                            color=ctx.color,
                            title="Users with \"Manage Webhook\" Permissions:",
                            description=f"{contents[cur_page-1]}",
                            timestamp = ctx.message.created_at
                        )
                        embed.set_author(
                            name = "Page {}/{}:".format(cur_page, pages)
                        )
                        await msg.edit(embed=embed)
                    elif str(reaction.emoji) == "⏹️":
                        await msg.delete()
                        try:
                            await ctx.message.add_reaction("<a:TickGif:802378817325760593>")
                        except:
                            pass
                    else:
                        await msg.remove_reaction(reaction, user)
                        await ctx.send("You can't do that {}!".format(ctx.author.mention), delete_after=10.0)
                except asyncio.TimeoutError:
                    try:
                        await msg.delete()
                    except discord.NotFound:
                        pass
                    try:
                        await ctx.message.add_reaction("<a:TickGif:802378817325760593>")
                    except:
                        pass
                    break
        else:
            if roles:
                strings = '\n'.join([role.mention for role in roles])
                l = strings.split()
                n = 100
                contents = ['\n'.join(l[x:x+n]) for x in range(0, len(l), n)]
                pages = len(contents)
                cur_page = 1
                embed = discord.Embed(
                    title="Roles with \"Manage Webhook\" Permissions:",
                    description = f"{contents[cur_page-1]}",
                    color=ctx.color,
                    timestamp = ctx.message.created_at
                )
                embed.set_author(
                    name = "Page {}/{}:".format(cur_page, pages)
                )
                msg = await ctx.send(embed=embed)
                def checkrole(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ['<a:facing_left_arrow:799579706688667669>', '<a:facing_right_arrow:799579865296535583>', '⏹️'] and reaction.message == msg

                await msg.add_reaction("<a:facing_left_arrow:799579706688667669>")
                await msg.add_reaction("<a:facing_right_arrow:799579865296535583>")
                await msg.add_reaction("⏹️")

                while True:
                    try:
                        reaction, user = await ctx.bot.wait_for("reaction_add", timeout = 60.0, check=checkrole)

                        if str(reaction.emoji) == "<a:facing_right_arrow:799579865296535583>" and cur_page != pages:
                            cur_page += 1
                            await msg.remove_reaction(reaction, user)
                            embed = discord.Embed(
                                color=ctx.color,
                                title="Roles with \"Manage Webhook\" Permissions:",
                                description=f"{contents[cur_page-1]}",
                                timestamp = ctx.message.created_at
                            )
                            embed.set_author(
                                name = "Page {}/{}:".format(cur_page, pages)
                            )
                            await msg.edit(embed=embed)
                        elif str(reaction.emoji) == "<a:facing_left_arrow:799579706688667669>" and cur_page > 1:
                            cur_page -= 1
                            await msg.remove_reaction(reaction, user)
                            embed = discord.Embed(
                                color=ctx.color,
                                title="Roles with \"Manage Webhook\" Permissions:",
                                description=f"{contents[cur_page-1]}",
                                timestamp = ctx.message.created_at
                            )
                            embed.set_author(
                                name = "Page {}/{}:".format(cur_page, pages)
                            )
                            await msg.edit(embed=embed)
                        elif str(reaction.emoji) == "⏹️":
                            await msg.delete()
                            try:
                                await ctx.message.add_reaction("<a:TickGif:802378817325760593>")
                            except:
                                pass
                        else:
                            await msg.remove_reaction(reaction, user)
                            await ctx.send("You can't do that {}!".format(ctx.author.mention), delete_after=10.0)
                    except asyncio.TimeoutError:
                        try:
                            await msg.delete()
                        except discord.NotFound:
                            pass
                        try:
                            await ctx.message.add_reaction("<a:TickGif:802378817325760593>")
                        except:
                            pass
                        break
            else:
                return await ctx.send("There is no roles with the `Manage Webhook` permission in this guild!")
        
        await ctx.send(embed=embed)

    @webhook.command(aliases = ['sess'])
    @commands.has_guild_permissions(manage_webhooks=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def session(self, ctx : commands.Context, webhook_link : str):
        """Initiate a session within this channel sending messages to a specified webhook link."""
        if ctx.channel.permissions_for(ctx.me).manage_messages:
            try:
                await ctx.message.delete()
            except discord.NotFound:
                pass
        e = discord.Embed(
            color=0x49FC95,
            title="Webhook Session Initiated",
            description=f"Session Created by `{ctx.author}`.",
        )
        initial_result = await self.webhook_link_send(
            webhook_link, "Webhook Session", "https://imgur.com/BMeddyn.png", embed=e
        )
        if initial_result is not True:
            return await ctx.send(initial_result)
        await ctx.send(
            "I will send all messages in this channel to the webhook until "
            "the session is closed by saying 'close' or there are 2 minutes of inactivity.",
            embed=e,
        )
        while True:
            try:
                result = await self.bot.wait_for(
                    "message_without_command",
                    check=lambda x: x.channel == ctx.channel and not x.author.bot and x.content,
                    timeout=120,
                )
            except asyncio.TimeoutError:
                return await ctx.send("Session closed.")
            if result.content.lower() == "close" and result.author == ctx.author:
                return await ctx.send("Session closed.")
            send_result = await self.webhook_link_send(
                webhook_link,
                result.author.display_name,
                result.author.avatar_url,
                content=result.content,
            )
            if send_result is not True:
                return await ctx.send("The webhook was deleted so this session has been closed.")

def setup(bot):
    bot.add_cog(Webhook(bot))
    print("Webhook Cog Is Ready!")
