"""
All User Slash Commands for Astral Admin
"""
import random
import string
import logging
import discord

from discord.ext import commands

from src.logic import firebase_db_connection, rsi_lookup, update_user_roles
from src.logic.slash_logic import SlashCommandsLogic as slash_logic

# Create Logger
logger = logging.getLogger("AA_Logger")


class SlashCommands(commands.Cog):
    """
    Astral Admin Bot Slash Cogs
    """

    def __init__(
        self,
        bot
        ):
        self.bot: commands.Bot = bot

    @commands.slash_command(
        name="ping",
        description="Ping! :)"
      )
    async def ping(
        self,
        ctx
        ):
        """
        Ping! :)
        """ 
        await ctx.respond(await slash_logic.ping(), ephemeral=True)
        logger.info("Ping. Pong. Haha Very Funny")

    # pylint: disable=no-member
    @commands.slash_command(
        name="get-validation-code",
        description="Get the Validation Code to symbolically bind your RSI and Discord Accounts"
    )
    async def get_verification_code(
        self,
        ctx,
        rsi_handle: discord.Option(str)
        ):
        """
        Create a verification code for the user, or remind them if they have one already.
        """
        author_name: str = ctx.author.name
        author_id: int = ctx.author.id
        guild_id: int = ctx.guild.id

        # Defer response
        await ctx.defer(ephemeral=True)

        logger.info("Checking RSI Handle: %s", rsi_handle)

        # Check RSI Username is not empty & exists
        rsi_user_json = rsi_lookup.get_user_info(rsi_handle)
        if rsi_user_json is None:
            await ctx.followup.send(
                "Please input your RSI Handle."
            )
        elif rsi_user_json == "Response Not OK":
            await ctx.followup.send(
                "The API for RSI's User pages is currently down. Please try again later or contact an Admin"
            )
        else:
            # The API has worked, and the RSI Handle is valid
            logger.info("Binding account for Discord User %s & RSI Handle %s", author_name, rsi_handle)
            
            # Generate a verification code for the User
            code = "".join([random.choice(string.ascii_letters) for n in range(10)])

            # Is the User already in the DB?
            result = await slash_logic.check_db_for_user(
                user=rsi_user_json,
                author_id=author_id,
                rsi_handle=rsi_handle,
                guild_id=guild_id,
                bot=self.bot,
                code=code)

            if result == 0:
                # An error or occured, or the user is attempting to use an already bound RSI Handle
                logger.error(
                    "There was an error in the binding of the following Discord and RSI Accounts. " +
                    f"Discord: {author_name}, RSI Handle: {rsi_handle}."
                    )
                ctx.followup.send(
                    "An Error was encountered adding your Discord User to the system. " +
                    "Please try again later, or contact an Admin."
                    )
            elif result == 1:

                # The user is either already in the DB, or has just been added and given a verification code.
                ctx.followup.send(
                    f"Greetings {author_name}, please add the following to your RSI Account's Short Bio: {code}" +
                    "\nYour short bio can be found here: https://robertsspaceindustries.com/account/profile" +
                    "\nOnce you have done this, please run the /validate command."
                )

                # Update the verification step to 1
                await firebase_db_connection.update_user_verification_status(author_id=author_id,
                                                                            user_verification_status=False,
                                                                            user_verification_progress=1
                                                                            )
            
            else:
                ctx.followup.send(
                    f"Greetings {author_name}, you already have a verification code! " +
                    f"\nIf you need a reminder, your code is {result}." +
                    f"\nPlease be sure to put it in your Short Bio, found here " + 
                    "https://robertsspaceindustries.com/account/profile" +
                    "\n\nPlease run the /validate command to continue."
                )

                # No need to update the user verification status.

    @commands.slash_command(
        name="validate",
        description="Continue the validation process. This command checks for your code on your RSI User Page."
    )
    async def validate(
        self,
        ctx
        ):         
        """
        Continuation of the verification process. 
        """
        author_name: str = ctx.author.name
        author_id: int = ctx.author.id
        guild_id: int = ctx.guild.id

        # Defer reponse
        await ctx.defer(ephemeral=True)

        # Get the Users Info from the DB.
        user_db_info = await firebase_db_connection.get_user(author_id=author_id)
        validation_progress = user_db_info["user_verification_progress"]

        # Check User Verification Status
        if user_db_info is None or validation_progress == 0:
            logger.info("User has tried to Validate before receiving a code.")
            ctx.followup.send(f"Greetings {author_name}, you have not received a Validation Code yet. " +
                              "Please run, /get-validation-code first.")
        elif validation_progress == 2:
            logger.debug("An already validates user has run the validate command.")
            await ctx.followup.send(
                            "You have already bound your Discord and RSI Accounts!" +
                            "\nIf you haven't already, sign up for a position at Astral Dynamics!" +
                            "\nhttps://robertsspaceindustries.com/orgs/ASTDYN"
                        )
        elif validation_progress == 1:
            logger.info("Attempting to validate the user %s.", author_name)

            # Valiadate the User
            if slash_logic.validate_user(
                user_db_info,
                author_name,
                author_id,
                guild_id,
                ctx,
                bot=self.bot
                ):
                await ctx.followup.send(
                    f"Thank you {user_db_info['rsi_handle']}, your Discord and RSI Accounts are now symbollically bound."
                    + "\n\nYou will not be able to access any more of the server unless you are a "
                    + "Member or Affiliate of Astral Dynamics. Sign up for membership here:"
                    + "https://robertsspaceindustries.com/orgs/ASTDYN",
                    ephemeral=True
                )
            else:
                await ctx.followup.send(
                    "Please make sure that you have added your verification code to your RSI Short Bio:" +
                    f"\nVerification Code {user_db_info['user_verification_code']}" +
                    "\nEdit your RSI Profile here: https://robertsspaceindustries.com/account/profile" +
                    "\n\nIf the problem persists, pease contact Support."
                )

    @commands.slash_command(
            name="apply-now",
            description="Assistance with applying to the Astral Dynamics Organistation."
    )
    async def apply_now(
        self,
        ctx
        ):
        """
        Send the user instructions on how to apply to Astral Dynamics.
        """
        logger.info("Apply Now Command")
        await ctx.respond(f"Hi there {ctx.author.mention}. To Apply to Astral Dynamics please use this link:"
                    + "\n\nhttps://robertsspaceindustries.com/orgs/ASTDYN"
                    + "\n\nOnce you have done this please @ mention Human Resources.",
                    ephemeral=True)

    @commands.slash_command(
        name="add-guild", description="Add the Discord Guild to the DB."
    )
    @commands.has_permissions(administrator=True)
    async def add_guild(self, ctx, spectrum_id: discord.Option(str)):
        """
        Admin only command to add the guild to the DB
        """
        logger.info("Add Guild")
        if await firebase_db_connection.put_new_guild(
            str(ctx.guild_id), ctx.guild.name, spectrum_id
            ):
            await ctx.respond("This Discord server has been added to the Database.",
                              ephemeral=True)
        else:
            await ctx.respond("The Discord server failed to be added to the Database",
                              ephemeral=True)

    @commands.slash_command(
            name="del-guild", description="Delete the Discord Guild from the DB."
    )
    @commands.has_permissions(administrator=True)
    async def del_guild(self, ctx):
        """
        Admin only command to delete the Discord Guild from the DB
        """
        logger.info("Delete Guild")
        if await firebase_db_connection.del_guild(guild_id=str(ctx.guild_id)):
            await ctx.respond("The Discord server has been removed from the Database",
                                ephemeral=True)
        else:
            ctx.respond("The Discord server failed to be removed from the Database",
                        ephemeral=True)

    @commands.slash_command(
    name="update-roles", description="Update the roles of bound members on the discord."
    )
    @commands.has_permissions(administrator=True)
    async def update_org_roles(self, ctx):
        """
        Admin only command to trigger the update of Discord roles based of the RSI Org page.
        """
        logger.info("Update Org Roles Command Run")
        await ctx.respond("Running roles Update Now")
        guild_ids = await firebase_db_connection.get_guild_ids()
        for guild_id in guild_ids:
            # Get list of verified members in the guild
            guild_members = await firebase_db_connection.get_guild_members(guild_id=guild_id)

            # Get verified member info
            user_list = []
            for member_id in guild_members:
                user_list.append(
                    await firebase_db_connection.get_user(author_id=str(member_id))
                )

            response = await update_user_roles.update_user_roles(user_list, bot=self.bot, guild_id=guild_id)

            await self.bot.get_channel(1233738280118390795).send(response)

def setup(bot):
    """
    Add Cog to Bot
    """
    bot.add_cog(SlashCommands(bot))
    logger.info("Slash Commands Cog Added")
  