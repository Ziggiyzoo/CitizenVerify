"""
Module to update a users discord roles.
"""
import discord

from src.logic import rsi_lookup

async def update_user_roles(self, user_list, bot: discord.bot, ctx):
    """
    Update the discord members roles based on the RSI site.
    """
    membership_list = ["Astral Dynamics Member",
                        "Astral Dynamics Affiliate"
                    ]
    rank_list = [
                "Affiliate",
                "Junior",
                "Senior",
                "Managers",
                "Directors",
                "Board Members"
                ]
    # Check members RSI info
    for user in user_list:
        self.user_handle = user["user_rsi_handle"]
        membership_status = await rsi_lookup.get_user_membership_info(rsi_handle=self.user_handle)
        if membership_status["main_member"] is not None:
            if membership_status["main_member"]:
                membership_index = 0
            else:
                membership_index = 1

            rank_index = int(membership_status["member_rank"])

            # Update Discord user roles
            try:
                guild = bot.get_guild(ctx.guild_id)
                user = guild.get_member(int(user["user_id"]))

                # Add Membership state
                await user.add_roles(
                    *[
                        discord.utils.get(
                            guild.roles, name=membership_list[membership_index]
                        ),
                        discord.utils.get(guild.roles, name=rank_list[rank_index]),
                    ]
                )
                await user.remove_roles(
                    discord.utils.get(
                        guild.roles, name=membership_list[membership_index - 1]
                    )
                )
                for i in [1, 2, 3, 4, 5]:
                    await user.remove_roles(
                        discord.utils.get(
                            guild.roles, name=rank_list[rank_index - i]
                        )
                    )
            except AttributeError as exc:
                # Uh Oh
                await ctx.respond("Failed to update role for User: " + self.user_handle + ". Error: " + exc,
                            ephemeral=True )

            except discord.DiscordException as exc:
                # Uh Oh
                await ctx.respond("Failed to update role for User: " + str(self.user_handle) + ". Error: " + str(exc),
                            ephemeral=True )
