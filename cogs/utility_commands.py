import discord
from discord.ext import commands
from functions import View_UI
from variables import global_vars


class utility_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        guild_ids=[global_vars.server_id],
        description=
        "A ping test to make sure the bot is responding as expected.",
    )
    async def ping(self, ctx):
        await ctx.respond(f"pong! latency: {int(self.bot.latency * 1000)} ms")

    ##Guide
    # Help Guide command
    @discord.slash_command(guild_ids=[global_vars.server_id],
                           description="A Guide on how to use the bot.")
    async def guide(self,ctx):
        embed = discord.Embed(
            title="AWS Admin BOT Guide",
            description=
            "This AWS bot is to allow you to start ,stop, and reboot a AWS EC2 Instance.",
            color=discord.Colour.blue(
            ),  # Pycord provides a class with default colors you can choose from
        )

        embed.set_author(
            name="creationsoftre",
            url="https://github.com/creationsoftre/",
            icon_url=
            "https://cdn.discordapp.com/attachments/950967021938556959/966750552757272646/cbktre_logo.png",
        )
        embed.add_field(
            name="Commands",
            value="The commands below is how to manage the aws ec2 instance:",
            inline=False,
        )
        embed.add_field(name="Start EC2 Instance",
                        value="/ec2_start",
                        inline=True)
        embed.add_field(name="Stop EC2 Instance",
                        value="/ec2_stop",
                        inline=True)
        embed.add_field(name="Reboot EC2 Instance",
                        value="/ec2_reboot",
                        inline=True)
        embed.add_field(name="EC2 Instance Status",
                        value="/ec2_status",
                        inline=True)
        embed.set_footer(text="© 2022, creationsoftre")

        view = View_UI(ctx)
        await ctx.respond("Hello! See what commands are used in this bot.",
                          embed=embed,
                          view=view)


def setup(bot):
    bot.add_cog(utility_commands(bot))
