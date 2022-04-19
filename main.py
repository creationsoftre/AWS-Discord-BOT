import discord
from discord.ext import commands
import os
import boto3
import functions


# initialize bot commands
bot = commands.Bot()

#### Discord Variables ####
# discord bot token
discord_token = os.environ["aws-BOT_Token"]
# Channel id (Guild)
channel_id = 964627684137271356
# server id (Guild)
server_id = 766533904433545236
# discord role id
ec2_role_id = 965340756330025052

#### AWS Variables: ####
# AWS session
session = boto3.Session(
    aws_access_key_id=os.environ["aws_access_key_id"],
    aws_secret_access_key=os.environ["aws_secret_access_key"],
    region_name="us-east-2",
)
# initialize aws ec2
ec2 = session.resource("ec2")
# EC2 instance with id
instance_id = "i-0df8f3c6a775b5ce7"
# ec2 instance
ec2_instance = ec2.Instance(instance_id)
# get ec2 state (pending/running/stopping/stopped/shutting-down)
ec2_status = ec2_instance.state["Name"]


### bot events ###
@bot.event
async def on_ready():
    print("We Have logged in as {0.user}".format(bot))


### bot commands ###
@bot.slash_command(
    guild_ids=[server_id],
    description="A ping test to make sure the bot is responding as expected.",
)

### Discord Command Cool down ###
# ping response function
async def ping(ctx):
    await ctx.respond(f"pong! latency: {int(bot.latency * 1000)} ms")

## Start EC2 command
@bot.slash_command(guild_ids=[server_id], description="command to start ec2 instance")
### Discord Command Cool down ###
@commands.has_role(ec2_role_id)
@commands.cooldown(1, 60, commands.BucketType.user)
async def ec2_start(ctx):
    await functions.start_ec2(ctx, ec2_instance, ec2_status, instance_id)
## Stop EC2 command
@bot.slash_command(guild_ids=[server_id], description="command to stop ec2 instance")
### Discord Command Cool down ###
@commands.has_role(ec2_role_id)
@commands.cooldown(1, 60, commands.BucketType.user)
async def ec2_stop(ctx):
    await functions.stop_ec2(ctx, ec2_instance, ec2_status, instance_id)

## Reboot EC2 command
@bot.slash_command(guild_ids=[server_id],description="command to reboot ec2 instance")
### Discord Command Cool down ###
@commands.has_role(ec2_role_id)
@commands.cooldown(1, 60, commands.BucketType.user)
async def ec2_reboot(ctx):
    await functions.reboot_ec2(ctx, ec2_instance, ec2_status, instance_id)

## Get EC2 status command
@bot.slash_command(guild_ids=[server_id],description="command to to get ec2 instance status")
### Discord Command Cool down ###
@commands.has_role(ec2_role_id)
@commands.cooldown(1, 15, commands.BucketType.user)
async def ec2_instance_status(ctx,ec2_status):
    embed = discord.Embed(
        title="AWS EC2 Instance Status",
        color=discord.Colour.blue(),  # Pycord provides a class with default colors you can choose from
    )
    embed.set_author(
        name="creationsoftre",
        url="https://github.com/creationsoftre/",
        icon_url="https://github.com/creationsoftre/blob/blob/main/logo.png",
    )
    embed.add_field(name="EC2 Status", value="ec2_status", inline=True)
    embed.set_footer(text="© 2022, creationsoftre")

    await ctx.respond(embed=embed)


# error handling on commands
@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(
            f"You are on cooldown, Retry after {int(error.retry_after)} seconds",
            ephemeral=True,
        )
    elif isinstance(error, commands.MissingRole):
        await ctx.respond(
            "You do not have the role required to run this command.", ephemeral=True
        )
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        raise error

        ##Guide


@bot.slash_command(guild_ids=[server_id], description="A Guide on how to use the bot.")
async def guide(ctx):
    try:
        view = functions.View_UI(ctx)
    except AttributeError as e:
        print(e)

    embed = discord.Embed(
        title="AWS Admin BOT Guide",
        description="This AWS bot is to allow you to start ,stop, and reboot a AWS EC2 Instance.",
        color=discord.Colour.blue(),  # Pycord provides a class with default colors you can choose from
    )

    embed.set_author(
        name="creationsoftre",
        url="https://github.com/creationsoftre/",
        icon_url="https://github.com/creationsoftre/blob/blob/main/logo.png",
    )
    embed.add_field(
        name="Commands",
        value="The commands below is how to manage the aws ec2 instance:",
        inline=False,
    )
    embed.add_field(name="Start EC2 Instance", value="/ec2 start", inline=True)
    embed.add_field(name="Stop EC2 Instance", value="/ec2 stop", inline=True)
    embed.add_field(name="Reboot EC2 Instance", value="/ec2 reboot", inline=True)
    embed.set_footer(text="© 2022, creationsoftre")

    await ctx.respond("Hello! Here's a cool embed.", embed=embed, view=view)


bot.run(discord_token)
