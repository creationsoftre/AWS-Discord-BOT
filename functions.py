import os
import discord
from botocore.exceptions import ClientError
from variables import global_vars
from discord.ui import View
from datetime import datetime
import uuid


class aws_funcs():
  def get_instance_info(ec2_client, ec2_tag_value):
        #gets' ec2 instance by tag-value
        reservations = ec2_client.describe_instances(
            Filters=[{
                "Name": "tag-value",
                "Values": [ec2_tag_value],
            }]).get("Reservations")
        for reservation in reservations:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                instance_launchtime = instance["LaunchTime"].strftime("%m-%d-%Y %H:%M:%S")
                instance_az = instance["Placement"]["AvailabilityZone"]
                instance_state = instance["State"]["Name"]
                for tags in instance["Tags"]:
                  if tags["Key"] == 'Name':
                    instance_name = tags["Value"]
                return instance_id, instance_launchtime, instance_az, instance_state, instance_name


  # Assign return variables in func to local variables
  
  def check_instance_state(ec2_client, ec2_tag_value):
        #gets' ec2 instance by tag-value
        reservations = ec2_client.describe_instances(
            Filters=[{
                "Name": "tag-value",
                "Values": [ec2_tag_value],
            }]).get("Reservations")
        for reservation in reservations:
            for instance in reservation["Instances"]:
                check_state = instance["State"]["Name"]
                return check_state

    #function for starting EC2 Instance
  
  async def start_ec2(ctx, ec2_client, instance_state, instance_id):
        #check ec2 state
        if instance_state == 'stopped':
            try:
                await ctx.response.defer(ephemeral=True)
                response = ec2_client.start_instances(InstanceIds=[instance_id])
                global_vars.logger.info("Started instance %s.", instance_id)
                await ctx.respond("Instance Successfully Started.")
            except ClientError:
                global_vars.logger.exception(
                    "Instance failed to start. Please have administrator investigate."
                )
                raise
                await ctx.respond(
                    "Instance failed to start. Please have administrator investigate."
                )
            else:
                return response
                await ctx.respond(response)
        elif instance_state == 'running':
            await ctx.respond("Instance is already running.")
        elif instance_state == 'pending':
            await ctx.respond(
                "Couldn't start instance. Instance is in a pending state.")
        elif instance_state == 'stopping':
            await ctx.respond(
                "Couldn't start instance. Instance is in a stopping state.")
        elif instance_state == 'shutting-down':
            await ctx.respond(
                "Couldn't start instance. Instance is in a shutting-down state."
            )
        elif instance_state == 'terminated':
            await ctx.respond(
                "Couldn't start instance. Instance has been terminiated.")
        else:
            await ctx.respond(
                'An issue has occured. Please contact administrator for further investigation.'
            )

    #function for stopping EC2 Instance
  async def stop_ec2(ctx, ec2_client, instance_state, instance_id):
        #check ec2 state
        if instance_state == 'running':
            try:
                await ctx.response.defer(ephemeral=True)
                response = ec2_client.stop_instances(InstanceIds=[instance_id])
                print("outside function called")
                global_vars.logger.info("Stop instance %s.", instance_id)
                await ctx.respond("Instance Successfully Stopped.")
            except ClientError:
                global_vars.logger.exception(
                    "Instance failed to stop. Please have administrator investigate."
                )
                raise
                await ctx.respond(
                    "Instance failed to stop. Please have administrator investigate."
                )
            else:
                return response
                await ctx.respond(response)
        elif instance_state == 'stopped':
            await ctx.respond("Instance is already stopped.")
        elif instance_state == 'pending':
            await ctx.respond(
                "Couldn't stop instance. Instance is in a pending state.")
        elif instance_state == 'stopping':
            await ctx.respond(
                "Couldn't stop instance. Instance is in a stopping state.")
        elif instance_state == 'shutting-down':
            await ctx.respond(
                "Couldn't stop instance. Instance is in a shutting-down state."
            )
        elif instance_state == 'terminated':
            await ctx.respond(
                "Couldn't stop instance. Instance has been terminiated.")
        else:
            await ctx.respond(
                'An issue has occured. Please contact administrator for further investigation.'
            )

    #function for rebooting EC2 Instance
  async def reboot_ec2(ctx, ec2_client, instance_state, instance_id):
        #check ec2 state
        if instance_state == 'running':
            try:
                await ctx.response.defer(ephemeral=True)
                response = ec2_client.reboot_instances(InstanceIds=[instance_id])
                global_vars.logger.info("Reboot instance %s.", instance_id)
                await ctx.respond("Instance Successfully Rebooted.")
            except ClientError:
                global_vars.logger.exception(
                    "Instance failed to reboot. Please have administrator investigate."
                )
                raise
                await ctx.respond(
                    "Instance failed to reboot. Please have administrator investigate."
                )
            else:
                return response
                await ctx.respond(response)
        elif instance_state == 'stopped':
            await ctx.respond(
                "Instance is in stopped state. Please start instance.")
        elif instance_state == 'pending':
            await ctx.respond(
                "Couldn't reboot instance. Instance is in a pending state.")
        elif instance_state == 'stopping':
            await ctx.respond(
                "Couldn't reboot instance. Instance is in a stopping state.")
        elif instance_state == 'shutting-down':
            await ctx.respond(
                "Couldn't reboot instance. Instance is in a shutting-down state."
            )
        elif instance_state == 'terminated':
            await ctx.respond(
                "Couldn't reboot instance. Instance has been terminiated.")
        else:
            await ctx.respond(
                'An issue has occured. Please contact administrator for further investigation.'
            )

  async def send_instance_state(ctx, ec2_client, ec2_tag_value,instance_launchtime, instance_az,instance_name):
        #check instance state
        check_state = None
        check_state = aws_funcs.check_instance_state(ec2_client, ec2_tag_value)
        embed = discord.Embed(
            title="EC2 Instance Status",
            color=discord.Colour.blue(
            ),  # Pycord provides a class with default colors you can choose from
        )
        embed.set_author(
            name="creationsoftre",
            url="https://github.com/creationsoftre/",
            icon_url=
            "https://cdn.discordapp.com/attachments/950967021938556959/966750552757272646/cbktre_logo.png",
        )
        red_circle = "\U0001f534"
        green_circle = "\U0001f7e2"
        yellow_circle = "\U0001f7e1"
        blue_circle = "\U0001f535"
        launch = "\U0001F680"
        map = "\U0001F5FA"
        server = "\U0001F5A5"

        embed.add_field(name="Server Name:",
                        value=f"{server} {instance_name}",
                        inline=False)

        if check_state == "stopped" or check_state == "terminated":
            embed.add_field(name="Status:",
                            value=f"{red_circle} {check_state}",
                            inline=False)

        if check_state == "running":
            embed.add_field(name="Status:",
                            value=f"{green_circle} {check_state}",
                            inline=False)

        if check_state == "pending" or check_state == "stopping" or check_state == "shutting-down":
            embed.add_field(name="Status:",
                            value=f"{yellow_circle} {check_state}",
                            inline=False)

        if check_state == "rebooting":
            embed.add_field(name="Status:",
                            value=f"{blue_circle} {check_state}",
                            inline=False)

        #Info embeds
        embed.add_field(name="Launch Time:",
                        value=f"{launch} {instance_launchtime}",
                        inline=True)
        embed.add_field(name="Availability Zone:",
                        value=f"{map} {instance_az}",
                        inline=True)
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/attachments/950967021938556959/966729383203176458/aws_bot_logo.png'
        )
        embed.set_footer(text="© 2022, creationsoftre")
        await ctx.respond(embed=embed)



class admin_funcs():
  async def purge(ctx, amount, user):
        def valid_user(msg):
            return msg.author.id == user.id

        #if only amount or amount and user is being used execute the following
        if amount > 0 and user == None:
            try:
                await ctx.channel.purge(limit=amount)
            except:
                await ctx.respond(
                    "Error occured, Contact Administrator for assistance.")
        elif amount > 0 and user != None:
            #if only amount and user are being used execute the following
            try:
                await ctx.channel.purge(limit=amount, check=valid_user)
            except:
                await ctx.respond(
                    "Error occured, Contact Administrator for assistance.")
        else:
            await ctx.respond(
                "You need to provide how many messages to purge.",
                delete_after=1)

  async def purge_logging(ctx, channel, amount, messages):
        unique_id = uuid.uuid4().hex
        file_name = f"{unique_id}_{ctx.channel.name}.txt"
        try:
            try:
                #write to file
                logfile = open(file_name, "a")
                if type(messages) == list:
                    for message in messages:
                        if message.embeds:
                            logfile.write("\n" + "Description: " +
                                          str(message.embeds[0].description) +
                                          "| Author: " +
                                          str(message.embeds[0].author) +
                                          "| Timestamp: " +
                                          str(message.embeds[0].timestamp) +
                                          ">")
                        else:
                            logfile.write("\n" + "< Content: " +
                                          str(message.content) + "| User: " +
                                          str(message.author) + "| User ID: " +
                                          str(message.author.id) +
                                          "| Date Created: " +
                                          str(message.created_at) + ">")
                else:
                    message = messages
                    if message.embeds:
                        logfile.write("\n" + "Description: " +
                                      str(message.embeds[0].description) +
                                      "| Author: " +
                                      str(message.embeds[0].author) +
                                      "| Timestamp: " +
                                      str(message.embeds[0].timestamp) + ">")
                    else:
                        logfile.write("\n" + "< Content: " +
                                      str(message.content) + "| User: " +
                                      str(message.author) + "| User ID: " +
                                      str(message.author.id) +
                                      "| Date Created: " +
                                      str(message.created_at) + ">")
                logfile.close()
            except RuntimeError:
                raise RuntimeError

            try:
                #send file to Discord in message
                with open(file_name, "rb") as file:
                    await ctx.channel.send(file=discord.File(file, file_name))
            except RuntimeError:
                raise RuntimeError

            #remove file once sent to discord
            os.remove(f"{unique_id}_{ctx.channel.name}.txt")
        except RuntimeError:
            await ctx.channel.send(
                "Unable to execute log shipping. Please contact an Administrator."
            )
            raise RuntimeError

        if amount == 1:
            embed = discord.Embed(
                description=
                f"{amount} Message was deleted in {ctx.channel.mention}",
                timestamp=datetime.now(),
                color=discord.Colour.red())
        elif amount > 1:
            embed = discord.Embed(
                description=
                f"{global_vars.messages_count} Messages were deleted in {ctx.channel.mention}",
                timestamp=datetime.now(),
                color=discord.Colour.red())
        await channel.send(embed=embed)

  async def package_logging(ctx, channel, amount, messages):
        unique_id = uuid.uuid4().hex
        file_name = f"{unique_id}_{ctx.channel.name}.txt"
        try:
            try:
                #write to file
                logfile = open(file_name, "a")
                if type(messages) == list:
                    for message in messages:
                        if message.embeds:
                            logfile.write("\n" + "Description: " +
                                          str(message.embeds[0].description) +
                                          "| Author: " +
                                          str(message.embeds[0].author) +
                                          "| Timestamp: " +
                                          str(message.embeds[0].timestamp) +
                                          ">")
                        else:
                            logfile.write("\n" + "< Content: " +
                                          str(message.content) + "| User: " +
                                          str(message.author) + "| User ID: " +
                                          str(message.author.id) +
                                          "| Date Created: " +
                                          str(message.created_at) + ">")
                else:
                    message = messages
                    logfile.write("\n" + "< Content: " + str(message.content) +
                                  "| User: " + str(message.author) +
                                  "| User ID: " + str(message.author.id) +
                                  str(message.created_at) + ">")
                logfile.close()
            except RuntimeError:
                raise RuntimeError

            try:
                #send file to Discord in message
                with open(file_name, "rb") as file:
                    await ctx.channel.send(file=discord.File(file, file_name))
            except RuntimeError:
                raise RuntimeError

            #remove file once sent to discord
            os.remove(f"{unique_id}_{ctx.channel.name}.txt")
        except RuntimeError:
            await ctx.channel.send(
                "Unable to execute log shipping. Please contact an Administrator."
            )
            raise RuntimeError

        if amount == 1:
            embed = discord.Embed(
                description=
                f"{amount} Message was packaged in {ctx.channel.mention}",
                timestamp=datetime.now(),
                color=discord.Colour.red())
        elif amount > 1:
            embed = discord.Embed(
                description=
                f"{global_vars.messages_count} Messages were packaged in {ctx.channel.mention}",
                timestamp=datetime.now(),
                color=discord.Colour.red())
        await channel.send(embed=embed)


class View_UI(View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx

    @discord.ui.select(
        placeholder="Select a command",
        options=[
            discord.SelectOption(
                label="Start EC2",
                description="Command to start an EC2 Instance."),
            discord.SelectOption(
                label="Stop EC2",
                description="Command to stop an EC2 Instance."),
            discord.SelectOption(
                label="Reboot EC2",
                description="Command to reboot an EC2 Instance."),
            discord.SelectOption(
                label="EC2 Status",
                description=
                "Command that provides details about the EC2 Instance.")
        ],
    )
    async def select_callback(self, select, interaction):
        select.disabled = True

        if select.values[0] == "Start EC2":
            await interaction.response.edit_message(view=self)
            await interaction.followup.send("Type in the command: /ec2_start",
                                            ephemeral=True)
            self.stop()
        elif select.values[0] == "Stop EC2":
            await interaction.response.edit_message(view=self)
            await interaction.followup.send("Type in the command: /ec2_stop",
                                            ephemeral=True)
            self.stop()
        elif select.values[0] == "Reboot EC2":
            await interaction.response.edit_message(view=self)
            await interaction.followup.send("Type in the command: /ec2_reboot",
                                            ephemeral=True)
            self.stop()
        elif select.values[0] == "EC2 Status":
            await interaction.response.edit_message(view=self)
            await interaction.followup.send("Type in the command: /ec2_status",
                                            ephemeral=True)
            self.stop()
        else:
            await interaction.response.edit_message(view=self)
            await interaction.followup.send_message(
                "Error occured. Please contact an Administrator.",
                ephemeral=True)
            self.stop()

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            child.placeholder = 'Disabled Due to Timeout'
            await self.ctx.edit(content='Timeout Reached. Please try again.',
                                view=self)
