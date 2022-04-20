import logging
import discord
from botocore.exceptions import ClientError
from discord.ui import View

logger = logging.getLogger(__name__)

def get_instance_info(ec2_client,ec2_tag_value):
  #gets' ec2 instance by tag-value
  reservations = ec2_client.describe_instances(Filters=[{"Name": "tag-value","Values": [ec2_tag_value],}]).get("Reservations")
  for reservation in reservations:
    for instance in reservation["Instances"]:
      instance_id = instance["InstanceId"]
      instance_launchtime = instance["LaunchTime"]
      instance_az = instance["Placement"]["AvailabilityZone"]
      instance_state = instance["State"]["Name"]
      instance_name = instance["KeyName"]
      return instance_id, instance_launchtime, instance_az, instance_state, instance_name

def check_instance_state(ec2_client,ec2_tag_value):
  #gets' ec2 instance by tag-value
  reservations = ec2_client.describe_instances(Filters=[{"Name": "tag-value","Values": [ec2_tag_value],}]).get("Reservations")
  for reservation in reservations:
    for instance in reservation["Instances"]:
      check_state = instance["State"]["Name"]
      return check_state
      
     
#function for starting EC2 Instance
async def start_ec2(ctx,ec2_client,instance_state,instance_id):
  #check ec2 state
    if instance_state == 'stopped':
      try:
        await ctx.respond("Initiating Startup...")
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        logger.info("Started instance %s.", instance_id)
        await ctx.respond("Instance Successfully Started.")
      except ClientError:
        logger.exception("Instance failed to start. Please have administrator investigate.")
        raise
        await ctx.respond("Instance failed to start. Please have administrator investigate.")
      else:
        return response
        await ctx.respond(response)
    elif instance_state == 'running':
      await ctx.respond("Instance is already running.")
    elif instance_state == 'pending':
      await ctx.respond("Couldn't start instance. Instance is in a pending state.")
    elif instance_state == 'stopping':
      await ctx.respond("Couldn't start instance. Instance is in a stopping state.")
    elif instance_state == 'shutting-down':
      await ctx.respond("Couldn't start instance. Instance is in a shutting-down state.")
    elif instance_state == 'terminated':
      await ctx.respond("Couldn't start instance. Instance has been terminiated.")
    else:
      await ctx.respond('An issue has occured. Please contact administrator for further investigation.')



#function for stopping EC2 Instance
async def stop_ec2(ctx,ec2_client,instance_state,instance_id):
  #check ec2 state
    if instance_state == 'running':
      try:
        await ctx.respond("Initiating Stop...")
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        logger.info("Stop instance %s.", instance_id)
        await ctx.respond("Instance Successfully Stopped.")
      except ClientError:
        logger.exception("Instance failed to stop. Please have administrator investigate.")
        raise
        await ctx.respond("Instance failed to stop. Please have administrator investigate.")
      else:
        return response
        await ctx.respond(response)
    elif instance_state == 'stopped':
      await ctx.respond("Instance is already stopped.")
    elif instance_state == 'pending':
      await ctx.respond("Couldn't stop instance. Instance is in a pending state.")
    elif instance_state == 'stopping':
      await ctx.respond("Couldn't stop instance. Instance is in a stopping state.")
    elif instance_state == 'shutting-down':
      await ctx.respond("Couldn't stop instance. Instance is in a shutting-down state.")
    elif instance_state == 'terminated':
      await ctx.respond("Couldn't stop instance. Instance has been terminiated.")
    else:
      await ctx.respond('An issue has occured. Please contact administrator for further investigation.')



#function for rebooting EC2 Instance
      
#function for stopping EC2 Instance
async def reboot_ec2(ctx,ec2_client,instance_state,instance_id):
  #check ec2 state
    if instance_state == 'running':
      try:
        await ctx.respond("Initiating Reboot...")
        response = ec2_client.reboot_instances(InstanceIds=[instance_id])
        logger.info("Reboot instance %s.", instance_id)
        await ctx.respond("Instance Successfully Rebooted.")
      except ClientError:
        logger.exception("Instance failed to reboot. Please have administrator investigate.")
        raise
        await ctx.respond("Instance failed to reboot. Please have administrator investigate.")
      else:
        return response
        await ctx.respond(response)
    elif instance_state == 'stopped':
      await ctx.respond("Instance is in stopped state. Please start instance.")
    elif instance_state == 'pending':
      await ctx.respond("Couldn't reboot instance. Instance is in a pending state.")
    elif instance_state == 'stopping':
      await ctx.respond("Couldn't reboot instance. Instance is in a stopping state.")
    elif instance_state == 'shutting-down':
      await ctx.respond("Couldn't reboot instance. Instance is in a shutting-down state.")
    elif instance_state == 'terminated':
      await ctx.respond("Couldn't reboot instance. Instance has been terminiated.")
    else:
      await ctx.respond('An issue has occured. Please contact administrator for further investigation.')

### GUIDE ###


async def send_instance_state(ctx,ec2_client,ec2_tag_value,instance_launchtime,instance_az,instance_name):
  #check instance state
  check_state = None
  check_state = check_instance_state(ec2_client,ec2_tag_value)
  embed = discord.Embed(
    title="AWS EC2 Instance Status",
    color=discord.Colour.blue(),  # Pycord provides a class with default colors you can choose from
  )
  embed.set_author(
    name="creationsoftre",
    url="https://github.com/creationsoftre/",
    icon_url="https://github.com/creationsoftre/blob/blob/main/logo.png",
  )
  red_circle = "\U0001f534"
  green_circle = "\U0001f7e2"
  yellow_circle = "\U0001f7e1"
  blue_circle = "	\U0001f535"

  embed.add_field(name="Server Name:", value=f"{blue_circle} {instance_name}", inline=True)
  
  if check_state == "stopped" or check_state == "terminated":
    embed.add_field(name="Status:", value=f"{red_circle} {check_state}", inline=True)
  
  if check_state == "running":
    embed.add_field(name="Status:", value=f"{green_circle} {check_state}", inline=True)
  
  if check_state == "pending" or check_state == "stopping" or check_state == "shutting-down":
    embed.add_field(name="Status:", value=f"{yellow_circle} {check_state}", inline=True)
  
  if check_state == "rebooting":
    embed.add_field(name="Status:", value=f"{blue_circle} {check_state}", inline=True)
    
  #Info embeds
  embed.add_field(name="Launch Time:", value=f"{blue_circle} {instance_launchtime}", inline=True)
  embed.add_field(name="Availability Zone:", value=f"{blue_circle} {instance_az}", inline=True)
  embed.set_footer(text="© 2022, creationsoftre")
  await ctx.respond(embed=embed)
class View_UI(View):
  def __init__(self,ctx):
    super().__init__(timeout=30)
    self.ctx = ctx
    
  @discord.ui.select(
    placeholder="Select a command",
      options=[
      discord.SelectOption(label="Start EC2", value='start', description="Command to start an EC2 Instance."),
      discord.SelectOption(label="Stop EC2", value='stop', description="Command to stop an EC2 Instance."),
      discord.SelectOption(label="Reboot EC2", value='reboot', description="Command to reboot an EC2 Instance.")
      ],)
  async def select_callback(self, select, interaction):
      select.disabled=True
      if select.values[0] == "Start EC2":
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("/ec2 start")
        #await start_ec2(ctx,ec2_client,instance_state,instance_id)
      elif select.values[0] == "Stop EC2":
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"Command commenced: {select.values}")
        #await stop_ec2(ctx,ec2_client,instance_state,instance_id)
      elif select.values[0] == "Reboot EC2":
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"Command commenced: {select.values}")
        #await reboot_ec2(ctx, ec2_client, instance_state, instance_id)
      else:
        await interaction.response.send_message("Error occured. Please contact an Administrator.")

  async def on_timeout(self):
    for child in self.children:
      child.disabled = True 
      child.placeholder ='Disabled Due to Timeout'
      await self.ctx.edit(content='Timeout Reached. Please try again.', view=self)


