""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""
import os
import platform
import exceptions

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot, Context


class Bot(disnake.ext.commands.Bot):
    def load_cogs(self, command_type: str) -> None:
        for file in os.listdir(f"./cogs/{command_type}"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    self.load_extension(f"cogs.{command_type}.{extension}")
                    print(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n{exception}")

    async def on_ready(self) -> None:
        """
        The code in this even is executed when the bot is ready
        """
        print(f"Logged in as {self.user.name}")
        print(f"disnake API version: {disnake.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        print("-------------------")
        await self.change_presence(activity=disnake.Game("Lurking PoE's Youtubers"))

    async def on_message(self, message: disnake.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix
        :param message: The message that was sent.
        """
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

    async def on_slash_command(self, interaction: ApplicationCommandInteraction) -> None:
        """
        The code in this event is executed every time a slash command has been *successfully* executed
        :param interaction: The slash command that has been executed.
        """
        print(
            f"Executed {interaction.data.name} command in {interaction.guild.name} (ID: {interaction.guild.id}) by {interaction.author} (ID: {interaction.author.id})")

    async def on_slash_command_error(self, interaction: ApplicationCommandInteraction, error: Exception) -> None:
        """
        The code in this event is executed every time a valid slash command catches an error
        :param interaction: The slash command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, exceptions.UserBlacklisted):
            """
            The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
            the @checks.is_owner() check in your command, or you can raise the error by yourself.
            
            'hidden=True' will make so that only the user who execute the command can see the message
            """
            embed = disnake.Embed(
                title="Error!",
                description="You are blacklisted from using the self.",
                color=0xE02B2B
            )
            print("A blacklisted user tried to execute a command.")
            return await interaction.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = disnake.Embed(
                title="Error!",
                description="You are missing the permission(s) `" + ", ".join(
                    error.missing_permissions) + "` to execute this command!",
                color=0xE02B2B
            )
            print("A blacklisted user tried to execute a command.")
            return await interaction.send(embed=embed, ephemeral=True)
        raise error

    async def on_command_completion(self, context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed
        :param context: The context of the command that has been executed.
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        print(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.message.guild.id}) by {context.message.author} (ID: {context.message.author.id})")

    async def on_command_error(self, context: Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error
        :param context: The normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = disnake.Embed(
                title="Hey, please slow down!",
                description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(
                title="Error!",
                description="You are missing the permission(s) `" + ", ".join(
                    error.missing_permissions) + "` to execute this command!",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = disnake.Embed(
                title="Error!",
                description=str(error).capitalize(),
                # We need to capitalize because the command arguments have no capital letter in the code.
                color=0xE02B2B
            )
            await context.send(embed=embed)
        raise error
