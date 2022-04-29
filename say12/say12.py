import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import asyncio


class Say(commands.Cog):
    """
    Let's you send a message to a designated channel.
    """

    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

        self.banlist = dict()

        bot.loop.create_task(self._set_mod_val())

    async def _update_mod_db(self):
        await self.coll.find_one_and_update(
            {"_id": "mod"}, {"$set": {"banlist": self.banlist}}, upsert=True,
        )

    async def _set_mod_val(self):
        mod = await self.coll.find_one({"_id": "mod"})

        if mod is None:
            return

        self.banlist = mod["banlist"]

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def sg(self, ctx, *, message): # send message in general chat
        if str(ctx.author.id) not in self.banlist:
            async with ctx.channel.typing():
                config = await self.coll.find_one({"_id": "config"})
                if config is None:
                    embed = discord.Embed(
                        title="general channel not set.", color=self.bot.error_color
                    )
                    embed.set_author(name="Error.")
                    embed.set_footer(text="Task failed successfully.")
                    await ctx.send(embed=embed)
                else:
                    suggestion_channel = self.bot.get_channel(
                        int(config["suggestion-channel"]["channel"])
                    )
                    suggestions = await self.coll.find_one({"_id": "suggestions"}) or {}
                    next_id = suggestions.get("next_id", 1)

                    msg = await suggestion_channel.send(message.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere"))
                    await self.coll.find_one_and_update(
                        {"_id": "suggestions"},
                        {
                            "$set": {
                                "next_id": next_id + 1,
                                str(next_id): {"msg_id": msg.id,},
                            }
                        },
                        upsert=True,
                    )

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def gcset(self, ctx, *, channel: discord.TextChannel): # set general chann
        await self.coll.find_one_and_update(
            {"_id": "config"},
            {"$set": {"suggestion-channel": {"channel": str(channel.id)}}},
            upsert=True,
        )

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def sgd(self, ctx, *, message): # send message in server modmail guide
        if str(ctx.author.id) not in self.banlist:
            async with ctx.channel.typing():
                config = await self.coll.find_one({"_id": "config"})
                if config is None:
                    embed = discord.Embed(
                        title="guide channel not set.", color=self.bot.error_color
                    )
                    embed.set_author(name="Error.")
                    embed.set_footer(text="Task failed successfully.")
                    await ctx.send(embed=embed)
                else:
                    guides_channel = self.bot.get_channel(
                        int(config["guide-channel"]["channel"])
                    )
                    suggestions = await self.coll.find_one({"_id": "suggestions"}) or {}
                    next_id = suggestions.get("next_id", 1)

                    msg = await guides_channel.send(message.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere"))
                    await self.coll.find_one_and_update(
                        {"_id": "suggestions"},
                        {
                            "$set": {
                                "next_id": next_id + 1,
                                str(next_id): {"msg_id": msg.id,},
                            }
                        },
                        upsert=True,
                    )

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def gdcset(self, ctx, *, channel: discord.TextChannel): # set guide channel
        await self.coll.find_one_and_update(
            {"_id": "config"},
            {"$set": {"guide-channel": {"channel": str(channel.id)}}},
            upsert=True,
        )

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def smgd(self, ctx, *, message): # send message in minecraft guide channel
        if str(ctx.author.id) not in self.banlist:
            async with ctx.channel.typing():
                config = await self.coll.find_one({"_id": "config"})
                if config is None:
                    embed = discord.Embed(
                        title="general channel not set.", color=self.bot.error_color
                    )
                    embed.set_author(name="Error.")
                    embed.set_footer(text="Task failed successfully.")
                    await ctx.send(embed=embed)
                else:
                    mguide_channel = self.bot.get_channel(
                        int(config["minecraftguide-channel"]["channel"])
                    )
                    suggestions = await self.coll.find_one({"_id": "suggestions"}) or {}
                    next_id = suggestions.get("next_id", 1)

                    msg = await mguide_channel.send(message.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere"))
                    await self.coll.find_one_and_update(
                        {"_id": "suggestions"},
                        {
                            "$set": {
                                "next_id": next_id + 1,
                                str(next_id): {"msg_id": msg.id,},
                            }
                        },
                        upsert=True,
                    )

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def mgdcset(self, ctx, *, channel: discord.TextChannel): # set minecraft guide channel
        await self.coll.find_one_and_update(
            {"_id": "config"},
            {"$set": {"minecraftguide-channel": {"channel": str(channel.id)}}},
            upsert=True,
        )

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def ssc(self, ctx, *, message): # send message in modmail setup channel
        if str(ctx.author.id) not in self.banlist:
            async with ctx.channel.typing():
                config = await self.coll.find_one({"_id": "config"})
                if config is None:
                    embed = discord.Embed(
                        title="general channel not set.", color=self.bot.error_color
                    )
                    embed.set_author(name="Error.")
                    embed.set_footer(text="Task failed successfully.")
                    await ctx.send(embed=embed)
                else:
                    setup_channel = self.bot.get_channel(
                        int(config["setup-channel"]["channel"])
                    )
                    suggestions = await self.coll.find_one({"_id": "suggestions"}) or {}
                    next_id = suggestions.get("next_id", 1)

                    msg = await setup_channel.send(message.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere"))
                    await self.coll.find_one_and_update(
                        {"_id": "suggestions"},
                        {
                            "$set": {
                                "next_id": next_id + 1,
                                str(next_id): {"msg_id": msg.id,},
                            }
                        },
                        upsert=True,
                    )

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def scset(self, ctx, *, channel: discord.TextChannel): # modmail setup channel h.. 
        await self.coll.find_one_and_update(
            {"_id": "config"},
            {"$set": {"setup-channel": {"channel": str(channel.id)}}},
            upsert=True,
        )

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def sml(self, ctx, *, message): # send message in minecraft guide channel
        if str(ctx.author.id) not in self.banlist:
            async with ctx.channel.typing():
                config = await self.coll.find_one({"_id": "config"})
                if config is None:
                    embed = discord.Embed(
                        title="general channel not set.", color=self.bot.error_color
                    )
                    embed.set_author(name="Error.")
                    embed.set_footer(text="Task failed successfully.")
                    await ctx.send(embed=embed)
                else:
                    mlog_channel = self.bot.get_channel(
                        int(config["minecraftlog-channel"]["channel"])
                    )
                    suggestions = await self.coll.find_one({"_id": "suggestions"}) or {}
                    next_id = suggestions.get("next_id", 1)

                    msg = await mguide_channel.send(message.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere"))
                    await self.coll.find_one_and_update(
                        {"_id": "suggestions"},
                        {
                            "$set": {
                                "next_id": next_id + 1,
                                str(next_id): {"msg_id": msg.id,},
                            }
                        },
                        upsert=True,
                    )

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def mlset(self, ctx, *, channel: discord.TextChannel): # set minecraft guide channel
        await self.coll.find_one_and_update(
            {"_id": "config"},
            {"$set": {"minecraftlog-channel": {"channel": str(channel.id)}}},
            upsert=True,
        )
        await ctx.send("Successfully completed the operation") 

def setup(bot):
    bot.add_cog(Say(bot))

