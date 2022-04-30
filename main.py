import discord
from discord.ext import commands
import os
from variables import global_vars
from functions import aws_funcs

intents = discord.Intents.default()
intents.members = True

#object of global vars class
bot = global_vars.bot
discord_token = global_vars.discord_token


### Global bot events ###
@bot.event
async def on_ready():
  print("We Have logged in as {0.user}".format(bot))
  aws_funcs.get_instance_info(global_vars.ec2_client, global_vars.ec2_tag_value)

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

#Create array of Cog files
initial_extensions = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

#load cogs
for extension in initial_extensions:
    bot.load_extension(extension)

bot.run(discord_token)
