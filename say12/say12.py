import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import asyncio


class Suggest(commands.Cog):
    """
    Let's you send a suggestion to a designated channel.
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
    @commands.cooldown(1, 20, commands.BucketType.member)
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def say12(self, ctx, *, suggestion):
        """
        Suggest something!

        **Usage**:
        [p]suggest more plugins!
        """
            if str(ctx.author.id) not in self.banlist:
            async with ctx.channel.typing():
                config = await self.coll.find_one({"_id": "config"})
                if config is None:
                    embed = discord.Embed(
                        title="Suggestion channel not set.", color=self.bot.error_color
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

                    message = await suggestion_channel.send(value=suggestion)
                    await self.coll.find_one_and_update(
                        {"_id": "suggestions"},
                        {
                            "$set": {
                                "next_id": next_id + 1,
                                str(next_id): {"message_id": message.id,},
                            }
                        },
                        upsert=True,
                    )
                    
   
def setup(bot):
    bot.add_cog(Suggest(bot))
