import discord
from discord.ext import commands
from functions import aws_funcs
from variables import global_vars


class aws_commands(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

      (
        self.instance_id,
        self.instance_launchtime,
        self.instance_az,
        self.instance_state,
        self.instance_name,
      ) = aws_funcs.get_instance_info(global_vars.ec2_client, global_vars.ec2_tag_value)
      

    ## Start EC2 command
    @discord.slash_command(guild_ids=[global_vars.server_id],
                           description="command to start ec2 instance")
    @commands.has_role(global_vars.ec2_role_id)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def ec2_start(self, ctx):
        await aws_funcs.start_ec2(ctx, global_vars.ec2_client,
                                  self.instance_state,
                                  self.instance_id)

    ## Stop EC2 command

    ## EC2 Stop command
    @discord.slash_command(guild_ids=[global_vars.server_id],
                           description="command to stop ec2 instance")
    @commands.has_role(global_vars.ec2_role_id)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def ec2_stop(self, ctx):
        await aws_funcs.stop_ec2(ctx, global_vars.ec2_client,
                                 self.instance_state,
                                 self.instance_id)

    ## Reboot EC2 command

    ## EC2 Reboot Command
    @discord.slash_command(guild_ids=[global_vars.server_id],
                           description="command to reboot ec2 instance")
    @commands.has_role(global_vars.ec2_role_id)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def ec2_reboot(self, ctx):
        await aws_funcs.reboot_ec2(ctx, global_vars.ec2_client,
                                   self.instance_state,
                                   self.instance_id)

    ## Get EC2 status command

    ## EC2 Status Command
    @discord.slash_command(guild_ids=[global_vars.server_id],
                           description="command to to get ec2 instance status")
    @commands.has_role(global_vars.ec2_role_id)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def ec2_status(self, ctx):
      await aws_funcs.send_instance_state(ctx, global_vars.ec2_client,
                                            global_vars.ec2_tag_value,
                                            self.instance_launchtime,
                                            self.instance_az,
                                            self.instance_name)


def setup(bot):
    bot.add_cog(aws_commands(bot))
