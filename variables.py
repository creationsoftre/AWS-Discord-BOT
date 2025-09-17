from discord.ext import commands
import os
import boto3
import logging


class global_vars():
    #Logging
    logger = logging.getLogger(__name__)
    # initialize bot commands
    bot = commands.Bot()
    #### Discord Variables ####
    # discord bot token
    discord_token = os.environ["aws-BOT_Token"]
    # Command Channel id (Guild)
    com_channel_id = 964627684137271356
    # Log Channel id (Guild)
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
        region_name="us-east-1",
    )
    ec2_client = session.client("ec2")
    # tag-value of ec2 instance
    ec2_tag_value = "assetto_instance"
    
    # Global Message variable
    message = ""
    messages = [None]
    messages_count = ""
