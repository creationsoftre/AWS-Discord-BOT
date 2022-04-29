import discord
from discord.ext import commands
import functions
from variables import global_vars

class aws_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ## Start EC2 command
    @discord.slash_command(guild_ids=[global_vars.server_id],
                           description="command to start ec2 instance")
    @commands.has_role(global_vars.ec2_role_id)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def ec2_start(self, ctx):
        await functions.start_ec2(ctx, global_vars.ec2_client, global_vars.instance_state, global_vars.instance_id)

    ## Stop EC2 command

    ## EC2 Stop command
    @discord.slash_command(guild_ids=[global_vars.server_id],
                           description="command to stop ec2 instance")
    @commands.has_role(global_vars.ec2_role_id)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def ec2_stop(self, ctx):
        await functions.stop_ec2(ctx, global_vars.ec2_client, global_vars.instance_state, global_vars.instance_id)

    ## Reboot EC2 command

    ## EC2 Reboot Command
    @discord.slash_command(guild_ids=[global_vars.server_id],
                           description="command to reboot ec2 instance")
    @commands.has_role(global_vars.ec2_role_id)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def ec2_reboot(self, ctx):
        await functions.reboot_ec2(ctx, global_vars.ec2_client, global_vars.instance_state,
                                   global_vars.instance_id)

    ## Get EC2 status command

    ## EC2 Status Command
    @discord.slash_command(guild_ids=[global_vars.server_id],
                           description="command to to get ec2 instance status")
    @commands.has_role(global_vars.ec2_role_id)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def ec2_status(self, ctx):
        await functions.send_instance_state(ctx, global_vars.ec2_client, global_vars.ec2_tag_value,
                                            global_vars.instance_launchtime, global_vars.instance_az,
                                            global_vars.instance_name)


def setup(bot):
    bot.add_cog(aws_commands(bot))
