import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

#function for starting EC2 Instance
async def start_ec2(ctx,ec2_instance,ec2_status,instance_id):
  #check ec2 state
    if ec2_status == 'stopped':
      try:
        await ctx.respond("Initiating Startup...")
        response = ec2_instance.start()
        ec2_instance.wait_until_running()
        logger.info("Started instance %s.", instance_id)
        await ctx.respond("Instance Successfully Started.")
      except ClientError:
        logger.exception("Instance failed to start. Please have administrator investigate.")
        raise
        await ctx.respond("Instance failed to start. Please have administrator investigate.")
      else:
        return response
        await ctx.respond(response)
    elif ec2_status == 'running':
      await ctx.respond("Instance is already running.")
    elif ec2_status == 'pending':
      await ctx.respond("Couldn't start instance. Instance is in a pending state.")
    elif ec2_status == 'stopping':
      await ctx.respond("Couldn't start instance. Instance is in a stopping state.")
    elif ec2_status == 'shutting-down':
      await ctx.respond("Couldn't start instance. Instance is in a shutting-down state.")
    elif ec2_status == 'terminated':
      await ctx.respond("Couldn't start instance. Instance has been terminiated.")
    else:
      await ctx.respond('An issue has occured. Please contact administrator for further investigation.')



#function for stopping EC2 Instance
async def stop_ec2(ctx,ec2_instance,ec2_status,instance_id):
  #check ec2 state
    if ec2_status == 'running':
      try:
        await ctx.respond("Initiating Stop...")
        response = ec2_instance.stop()
        ec2_instance.wait_until_stopped()
        logger.info("Stop instance %s.", instance_id)
        await ctx.respond("Instance Successfully Stopped.")
      except ClientError:
        logger.exception("Instance failed to stop. Please have administrator investigate.")
        raise
        await ctx.respond("Instance failed to stop. Please have administrator investigate.")
      else:
        return response
        await ctx.respond(response)
    elif ec2_status == 'stopped':
      await ctx.respond("Instance is already stopped.")
    elif ec2_status == 'pending':
      await ctx.respond("Couldn't stop instance. Instance is in a pending state.")
    elif ec2_status == 'stopping':
      await ctx.respond("Couldn't stop instance. Instance is in a stopping state.")
    elif ec2_status == 'shutting-down':
      await ctx.respond("Couldn't stop instance. Instance is in a shutting-down state.")
    elif ec2_status == 'terminated':
      await ctx.respond("Couldn't stop instance. Instance has been terminiated.")
    else:
      await ctx.respond('An issue has occured. Please contact administrator for further investigation.')



#function for rebooting EC2 Instance
      
#function for stopping EC2 Instance
async def reboot_ec2(ctx,ec2_instance,ec2_status,instance_id):
  #check ec2 state
    if ec2_status == 'running':
      try:
        await ctx.respond("Initiating Reboot...")
        response = ec2_instance.reboot()
        ec2_instance.wait_until_running()
        logger.info("Reboot instance %s.", instance_id)
        await ctx.respond("Instance Successfully Rebooted.")
      except ClientError:
        logger.exception("Instance failed to reboot. Please have administrator investigate.")
        raise
        await ctx.respond("Instance failed to reboot. Please have administrator investigate.")
      else:
        return response
        await ctx.respond(response)
    elif ec2_status == 'stopped':
      await ctx.respond("Instance is in stopped state. Please start instance.")
    elif ec2_status == 'pending':
      await ctx.respond("Couldn't reboot instance. Instance is in a pending state.")
    elif ec2_status == 'stopping':
      await ctx.respond("Couldn't reboot instance. Instance is in a stopping state.")
    elif ec2_status == 'shutting-down':
      await ctx.respond("Couldn't reboot instance. Instance is in a shutting-down state.")
    elif ec2_status == 'terminated':
      await ctx.respond("Couldn't reboot instance. Instance has been terminiated.")
    else:
      await ctx.respond('An issue has occured. Please contact administrator for further investigation.')

