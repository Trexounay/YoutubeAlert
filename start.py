import os
import json
import sys
import disnake
import bot

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = disnake.Intents.default()
#intents.dm_messages = True
#intents.presences = True
intents.members = True
intents.reactions = True

instance = bot.Bot(command_prefix=config["prefix"], intents=intents)

if __name__ == "__main__":
    instance.load_cogs("task")

instance.run(config["token"])
