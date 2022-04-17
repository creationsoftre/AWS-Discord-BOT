import os
import discord
from discord.ext import commands, tasks
import boto3
import functions


#initialize discord client
client = discord.Client()

#initialize bot commands
bot = commands.Bot(command_prefix='!')

#AWS session
session = boto3.Session(
  aws_access_key_id = os.environ['aws_access_key_id'],
  aws_secret_access_key = os.environ['aws_secret_access_key'],
  region_name='us-east-2'
)
#initialize aws ec2 
ec2  = session.resource('ec2')

#Variables:
#discord bot token
discord_token = os.environ['aws-BOT_Token']
#EC2 instance with id
instance_id = 'i-0df8f3c6a775b5ce7'
#ec2 instance
ec2_instance = ec2.Instance(instance_id)
#get ec2 state (pending/running/stopping/stopped/shutting-down)
ec2_status = ec2_instance.state['Name']
#Get aws_commands Channel id
channel_id = (964627684137271356)
channel = client.get_channel(channel_id)


@bot.event
async def on_ready():
  print('We Have logged in as {0.user}'.format(bot))
  
@bot.command()
async def aws_ec2_start(ctx):
  await functions.start_ec2(ctx,ec2_instance,ec2_status,instance_id,channel_id)

async def aws_ec2_stop(ctx):
  await functions.stop_ec2(ctx,ec2_instance,ec2_status,instance_id,channel_id)

async def aws_ec2_reboot(ctx):
  await functions.reboot_ec2(ctx,ec2_instance,ec2_status,instance_id,channel_id)

async def help(ctx):
  embed = discord.Embed(
        title="AWS Help Guide",
        description="This AWS bot is to allow you to start,stop, and reboot the AWS EC2 Instance for Assetto Corsa",
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
  embed.add_field(title="Commands", value="Utilize the follwoing commands to manage the EC2 instance. **Please use these commands responsibly!**")

  embed.add_field(title="Start EC2", value="!aws_ec2_start", inline=True)
  embed.add_field(title="Stop EC2", value="!aws_ec2_stop", inline=True)
  embed.add_field(title="Reboot EC2", value="!aws_ec2_reboot", inline=True)
 
  embed.set_footer(text="created by Trevonte Wigfall") # footers can have icons too
  embed.set_author(name="Trevonte Wigfall", icon="https://example.com/link-to-my-image.png")
  embed.set_thumbnail(url="https://example.com/link-to-my-thumbnail.png")
  embed.set_image(url="https://example.com/link-to-my-banner.png")
 
  await ctx.respond("Help is on the way! Check out the commands to get started.", embed=embed) # Send the embed with some text
    
bot.run(discord_token)