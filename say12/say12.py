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
    async def say12(self, ctx, *, message):
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
                    generalchannel = self.bot.get_channel(
                        int(config["general-channel"]["channel"])
                    )

                    msg = await generalchannel.send(message.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere"))
          
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def gcset(self, ctx, *, channel: discord.TextChannel):
        await self.coll.find_one_and_update(
            {"_id": "config"},
            {"$set": {"general-channel": {"channel": str(channel.id)}}},
            upsert=True,
        )

def setup(bot):
    bot.add_cog(Say(bot))
