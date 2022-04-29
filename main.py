import discord
from discord.ext import commands
from discord.commands import OptionChoice
import os
import boto3
import functions
from discord.commands import Option
from datetime import datetime
import asyncio

# initialize bot commands
bot = commands.Bot()
#### Discord Variables ####
# discord bot token
discord_token = os.environ["aws-BOT_Token"]
# Channel id (Guild)
com_channel_id = 964627684137271356
log_channel_id = 968527193829429268
# server id (Guild)
server_id = 766533904433545236
# aws discord role id
ec2_role_id = 965340756330025052
# admin discord role
administrator = 766538307940515841
#### AWS Variables: ####
# AWS session passed to get_instance_info method
session = boto3.Session(
    aws_access_key_id=os.environ["aws_access_key_id"],
    aws_secret_access_key=os.environ["aws_secret_access_key"],
    region_name="us-east-2",
)
ec2_client = session.client("ec2")
# tag-value of ec2 instance
ec2_tag_value = "ACServer01"

# Assign return variables in func to local variables
(
    instance_id,
    instance_launchtime,
    instance_az,
    instance_state,
    instance_name,
) = functions.get_instance_info(ec2_client, ec2_tag_value)

# Global Message variable
message = ""
messages = [None]


### bot events ###
@bot.event
async def on_ready():
    print("We Have logged in as {0.user}".format(bot))
    functions.get_instance_info(ec2_client, ec2_tag_value)


### bot commands ###


# Logging - send embed to aws-logs channel when command is executed
@bot.event
async def on_application_command_completion(ctx):
    channel = bot.get_channel(log_channel_id)
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
@bot.event
async def on_application_command(ctx):
    channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(
        description=
        f"Invoked Command: {ctx.command}\nAuthor: {ctx.author.mention}\nLocation: {ctx.channel.mention}",
        timestamp=datetime.now(),
        color=discord.Colour.yellow(),
    )
    embed.set_footer(text=f"User ID: {ctx.author.id}")
    embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar)
    await channel.send(embed=embed)


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(
            f"You are on cooldown, Retry after {int(error.retry_after)} seconds",
            ephemeral=True,
        )
    elif isinstance(error, commands.MissingRole):
        await ctx.respond(
            "You do not have the role required to run this command.",
            ephemeral=True)
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        raise error


@bot.event
async def on_message_delete(msg):
    # call global variable
    global message
    message = msg


@bot.event
async def on_bulk_message_delete(msgs):
    # call global variable
    global messages
    messages = msgs


# ping command
@bot.slash_command(
    guild_ids=[server_id],
    description="A ping test to make sure the bot is responding as expected.",
)
async def ping(ctx):
    await ctx.respond(f"pong! latency: {int(bot.latency * 1000)} ms")


## Start EC2 command
@bot.slash_command(guild_ids=[server_id],
                   description="command to start ec2 instance")
@commands.has_role(ec2_role_id)
@commands.cooldown(1, 60, commands.BucketType.user)
async def ec2_start(ctx):
    await functions.start_ec2(ctx, ec2_client, instance_state, instance_id)


## Stop EC2 command


## EC2 Stop command
@bot.slash_command(guild_ids=[server_id],
                   description="command to stop ec2 instance")
@commands.has_role(ec2_role_id)
@commands.cooldown(1, 60, commands.BucketType.user)
async def ec2_stop(ctx):
    await functions.stop_ec2(ctx, ec2_client, instance_state, instance_id)


## Reboot EC2 command


## EC2 Reboot Command
@bot.slash_command(guild_ids=[server_id],
                   description="command to reboot ec2 instance")
@commands.has_role(ec2_role_id)
@commands.cooldown(1, 60, commands.BucketType.user)
async def ec2_reboot(ctx):
    await functions.reboot_ec2(ctx, ec2_client, instance_state, instance_id)


## Get EC2 status command


## EC2 Status Command
@bot.slash_command(guild_ids=[server_id],
                   description="command to to get ec2 instance status")
@commands.has_role(ec2_role_id)
@commands.cooldown(1, 15, commands.BucketType.user)
async def ec2_status(ctx):
    await functions.send_instance_state(ctx, ec2_client, ec2_tag_value,
                                        instance_launchtime, instance_az,
                                        instance_name)


# error handling on commands

# command error handling


##Guide
# Help Guide command
@bot.slash_command(guild_ids=[server_id],
                   description="A Guide on how to use the bot.")
async def guide(ctx):
    embed = discord.Embed(
        title="AWS Admin BOT Guide",
        description=
        "This AWS bot is to allow you to start ,stop, and reboot a AWS EC2 Instance.",
        color=discord.Colour.blue(
        ),  # Pycord provides a class with default colors you can choose from
    )

    embed.set_author(
        name="creationsoftre",
        url="https://github.com/creationsoftre/",
        icon_url=
        "https://cdn.discordapp.com/attachments/950967021938556959/966750552757272646/cbktre_logo.png",
    )
    embed.add_field(
        name="Commands",
        value="The commands below is how to manage the aws ec2 instance:",
        inline=False,
    )
    embed.add_field(name="Start EC2 Instance", value="/ec2_start", inline=True)
    embed.add_field(name="Stop EC2 Instance", value="/ec2_stop", inline=True)
    embed.add_field(name="Reboot EC2 Instance",
                    value="/ec2_reboot",
                    inline=True)
    embed.add_field(name="EC2 Instance Status",
                    value="/ec2_status",
                    inline=True)
    embed.set_footer(text="© 2022, creationsoftre")

    view = functions.View_UI(ctx)
    await ctx.respond("Hello! See what commands are used in this bot.",
                      embed=embed,
                      view=view)


#Clear command Choices
log_choice = [
    OptionChoice(name="Yes", value="Yes"),
    OptionChoice(name="No", value="No")
]


# Clear Command
@bot.slash_command(guild_ids=[server_id],
                   description="clear messages in chat.")
@commands.has_role(administrator)
async def clear(ctx, amount: Option(
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
    channel = bot.get_channel(log_channel_id)
    if ctx.channel.id == log_channel_id and logging == "Yes":
        # purge with logging
        await functions.purge(ctx, amount, user)
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
@bot.slash_command(guild_ids=[server_id],
                   description="package logs before todays date.")
@commands.has_role(administrator)
async def package(
    ctx,
    amount: Option(
        discord.SlashCommandOptionType.integer,
        description="amount of messages",
        required=True,
    ),
):
    await ctx.response.defer(ephemeral=True)
    channel = bot.get_channel(log_channel_id)
    if ctx.channel.id == log_channel_id:
        messages = await channel.history(limit=amount).flatten()
        await asyncio.sleep(5)
        await functions.package_logging(ctx, channel, amount, messages)
    else:
        await ctx.respond(
            f"/package command can only be ran in {channel.mention}",
            ephermal=True)


bot.run(discord_token)
