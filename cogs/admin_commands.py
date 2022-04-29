import discord
from discord.ext import commands
import functions
from discord.commands import Option
from datetime import datetime
import asyncio
from discord.commands import OptionChoice
from variables import global_vars

class admin_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_completion(self, ctx):
        
        channel = self.bot.get_channel(global_vars.log_channel_id)
        embed = discord.Embed(
            description=
            f"Executed Command: {ctx.command}\nAuthor: {ctx.author.mention}\nLocation: {ctx.channel.mention}",
            timestamp=datetime.now(),
            color=discord.Colour.green(),
        )
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar)
        await channel.send(embed=embed)

# Logging - send embed to aws-logs channel when command is invoked whether failed or successful

    @commands.Cog.listener()
    async def on_application_command(self, ctx):
        channel = self.bot.get_channel(global_vars.log_channel_id)
        embed = discord.Embed(
            description=
            f"Invoked Command: {ctx.command}\nAuthor: {ctx.author.mention}\nLocation: {ctx.channel.mention}",
            timestamp=datetime.now(),
            color=discord.Colour.yellow(),
        )
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        # call global variable
        global_vars.message
        message = msg
        return message

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, msgs):
        # call global variable
        global_vars.messages
        messages = msgs
        return messages

    # Clear Command
    log_choice = [
        OptionChoice(name="Yes", value="Yes"),
        OptionChoice(name="No", value="No")
    ]
  
    @discord.slash_command(guild_ids=[global_vars.server_id],
                           description="clear messages in chat.")
    @commands.has_role(global_vars.administrator)
    async def clear(self, ctx, amount: Option(
        discord.SlashCommandOptionType.integer,
        description="amount of messages",
        required=True,
    ), user: Option(
        discord.SlashCommandOptionType.user,
        description="purge messages from user",
        required=False,
        default=None,
    ), logging: Option(discord.SlashCommandOptionType.string,
                       description="enable or disable logging",
                       required=False,
                       default=None,
                       choices=log_choice)):
        await ctx.response.defer(ephemeral=True)
        channel = self.bot.get_channel(global_vars.log_channel_id)
        if ctx.channel.id == global_vars.log_channel_id and logging == "Yes":
            # purge with logging
            await functions.purge(ctx, amount, user)
            message = admin_commands().on_message_delete()
            messages = admin_commands().on_bulk_message_delete()
            if amount == 1:
                # call purge-logging
                await asyncio.sleep(5)
                await functions.purge_logging(ctx, channel, amount, message)
            else:
                # call purge-logging
                await asyncio.sleep(5)
                await functions.purge_logging(ctx, channel, amount, messages)
        else:
            # purge without logging in other channels
            await functions.purge(ctx, amount, user)

    # Package Command
    @discord.slash_command(guild_ids=[global_vars.server_id],
                           description="package logs before todays date.")
    @commands.has_role(global_vars.administrator)
    async def package(
        self,
        ctx,
        amount: Option(
            discord.SlashCommandOptionType.integer,
            description="amount of messages",
            required=True,
        ),
    ):
        await ctx.response.defer(ephemeral=True)
        channel = self.bot.get_channel(global_vars.log_channel_id)
        if ctx.channel.id == global_vars.log_channel_id:
            messages = await channel.history(limit=amount).flatten()
            await asyncio.sleep(5)
            await functions.package_logging(ctx, channel, amount, messages)
        else:
            await ctx.respond(
                f"/package command can only be ran in {channel.mention}",
                ephermal=True)


def setup(bot):
    bot.add_cog(admin_commands(bot))
