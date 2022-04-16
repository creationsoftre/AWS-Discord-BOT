import os
import discord
import boto3

#discord bot token
discord_token = os.environ['aws-BOT_Token']

#initialize discord client
client = discord.Client()

#use aws ec2 
ec2  = boto3.resource('ec2')

@client.event
async def on_ready():
  print('We Have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!aws-ec2-start'):
    await message.channel.send('EC2 is intiating start')

client.run(discord_token)