"""
All User Slash Commands for Astral Admin
"""
import discord
import random
import string

from discord.ext import commands

from src.logic import firebase_db_connection, rsi_lookup

class SlashCommands(commands.Cog):
    """
    Helldivers Update Bot Slash Cogs
    """

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.slash_command(
        name="ping", description="Ping! :)"
      )
    async def ping(self, ctx):
        """
        Ping! :)
        """
        await ctx.respond("Pong!")
    
    @commands.slash_command(
        name="bind-rsi-account", description="Bind your Discord and RSI Accounts"
    )
    async def bind_rsi_account(self, ctx, rsi_handle: discord.Option(str)):
        author_name: str = ctx.author.name
        author_id: int = ctx.author.id
        guild_id: int = ctx.guild.id

        await ctx.defer()

        if rsi_handle == None:
            await ctx.followup.send(
                "Please input your RSI Handle.",
                ephemeral=True,
            )
        elif not rsi_lookup.check_rsi_handle(rsi_handle=rsi_handle):
            await ctx.followup.send(
                "That RSI Handle is invalid. Please imput a correct Value",
                ephemeral=True,
            )
        else:
            # Check if the user exists
            user_info = await firebase_db_connection.get_user(author_id=author_id)
            if user_info is None:
                # The did not exist. Create them.
                code = "".join([random.choice(string.ascii_letters) for n in range(10)])
                await firebase_db_connection.put_new_user(
                    author_id=str(author_id),
                    guild_id=str(guild_id),
                    rsi_handle=rsi_handle,
                    user_verification_code=code
                )

                # Tell then user to put the code in their RSI Bio

                await ctx.followup.send(
                    f"Greetings {author_name}" +
                    f", please add the following to your RSI Account's Short Bio: {code}" +
                    "\nThis can be found here: https://robertsspaceindustries.com/account/profile" +
                    "\n\nAfter you have done this please re run this command.",
                    ephemeral=True
                )

                # Update the user verification step to 1
                await firebase_db_connection.update_user_verification_status(author_id=author_id, user_verification_status=False, user_verification_progress=1)
                print("User Create")
            
            else:
                if user_info["user_verification_progress"] == 0:

                if user_info["user_verification_progress"] == 1:                     
                    # The user has begun the process and needs verification
                    if rsi_lookup.verify_rsi_handle(rsi_handle=user_info["user_rsi_handle"], verification_code=user_info["user_verification_code"]):
                        await firebase_db_connection.update_user_verification_status(2, True)
                        await ctx.followup.send(
                            f"Thank you {rsi_handle}, your Discord and RSI Accounts are now symbollically bound.",
                            ephemeral=True
                        )
                    
                    else:
                        await ctx.followup.send(
                            "Please make sure that you have added your verification code to your RSI Short Bio:" +
                            f"\nVerification Code {user_info['user_verification_code']}" +
                            "\nEdit your RSI Profile here: https://robertsspaceindustries.com/account/profile",
                            ephemeral=True
                        )


                if user_info["user_verification_progress"] == 2:
                    await ctx.followup.send(
                        "You have already bound your Discord and RSI Accounts!" +
                        "\nIf you haven't already, sign up for a position at Astral Dynamics!" +
                        "\nhttps://robertsspaceindustries.com/orgs/ASTDYN",
                        ephemeral=True
                    )



def setup(bot):
    """
    Add cog to bot
    """
    bot.add_cog(SlashCommands(bot))
    