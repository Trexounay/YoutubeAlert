import os
import disnake
from disnake.ext import tasks, commands
from disnake import ApplicationCommandInteraction

from helpers import checks
from helpers.save import get_save

import googleapiclient.discovery
import json
import datetime

DEVELOPER_KEY = "AIzaSyB5B2VNlTBH39T346ZFH4C5Y4F-eqVbYgY"
api_service_name = "youtube"
api_version = "v3"

class YoutubeCom(commands.Cog, name=__name__):
    def __init__(self, bot):
        self.bot = bot
        self.check_task.start()

    def cog_unload(self):
        self.check_task.cancel()

    @commands.slash_command(
        name="youtubeadd",
        description="Add a youtube channel to the alert list",
        guild_ids=[797183317115142196, 715201231252881428],
    )
    @checks.not_blacklisted()
    @commands.has_permissions(manage_messages=True)
    async def youtubeadd(self, inter: ApplicationCommandInteraction, youtube_channel_id: str, discord_channel: disnake.abc.GuildChannel = None):
        save = get_save(inter.guild_id, __name__)
        if not save["USERS_ID"]:
            save["USERS_ID"] = []
        if not discord_channel:
            discord_channel = inter.channel
        save["USERS_ID"].append(youtube_channel_id)
        save["CHANNEL_ID"] = discord_channel.id
        save.save()
        await inter.response.send_message(f"added user {youtube_channel_id}")
        await self.check_channel(save, youtube_channel_id, discord_channel.id)
        #self.check_task.restart()

    @commands.slash_command(
        name="emojiadd",
        description="Add a youtube channel to the alert list",
        guild_ids=[797183317115142196, 715201231252881428],
    )
    @checks.not_blacklisted()
    @commands.has_permissions(manage_messages=True)
    async def emojiadd(self, inter: ApplicationCommandInteraction, emoji: str, channel: disnake.abc.GuildChannel):
        save = get_save(inter.guild_id, __name__)
        if not save["REACTIONS"]:
            save["REACTIONS"] = {}
        save["REACTIONS"][emoji] = channel.id
        save.save()
        await inter.response.send_message(f"added reaction {emoji}")

    async def check_channel(self, save = None, user_id = 0, channel_id = 0, post_message=True):
        cached_runs = {}
        emojis = {}
        if save:
            cached_runs = save['CACHED_RUNS'] or {}
            emojis = save["REACTIONS"] or {}
        if not user_id:
            print("no user")
            return
        channel = self.bot.get_channel(channel_id)
        if not channel:
            print("no channel")
            return
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
        request = youtube.activities().list(
            part="snippet,contentDetails",
            channelId=user_id,
            maxResults=3
        )
        response = request.execute()
        for i in response["items"]:
            if i["snippet"]["type"] == "upload":
                id = i["contentDetails"]["upload"]["videoId"]
                if id not in cached_runs:
                    if not post_message:
                        cached_runs[id] = -1
                        continue
                    time = datetime.datetime.fromisoformat(i["snippet"]["publishedAt"])
                    if save["LAST_TIME"] and datetime.datetime.fromisoformat(save["LAST_TIME"]) > time:
                        continue
                    title = i["snippet"]["title"]
                    user = i["snippet"]["channelTitle"]
                    description = i["snippet"]["description"]
                    thumb = i["snippet"]["thumbnails"]["medium"]["url"]
                    link = f"http://youtube.com/watch?v={id}"

                    e = disnake.Embed(
                        title=f"**{title} ({user})**",
                        url=f"{link}",
                    )
                    e.set_thumbnail(url=thumb)
                    message = await channel.send(content=f"**{user}** *({time.time()})*", embed=e)
                    for e in emojis:
                        await message.add_reaction(e)
                    cached_runs[id] = message.id
        if save:
            save['CACHED_RUNS'] = cached_runs
            save.save()

    @tasks.loop(minutes=5.0)
    async def check_task(self) -> None:
        print("checking Youtube")
        for guild in self.bot.guilds:
            save = get_save(guild.id, __name__)
            users = save['USERS_ID'] or []
            for user in users:
                await self.check_channel(save, user_id=user, channel_id=save['CHANNEL_ID'])
            save["LAST_TIME"] = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

    @check_task.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload : disnake.RawReactionActionEvent) -> None:
        guild_id = payload.guild_id
        if payload.user_id == self.bot.user.id:
            return
        save = get_save(guild_id, __name__)
        if not save:
            return
        if save["CACHED_RUNS"] and save["REACTIONS"] and payload.message_id in save["CACHED_RUNS"].values() and payload.emoji.name in save["REACTIONS"]:
            try:
                src_channel = self.bot.get_channel(payload.channel_id)
                dst_channel = self.bot.get_channel(save["REACTIONS"][payload.emoji.name])
                message = await src_channel.fetch_message(payload.message_id)
                await dst_channel.send(content=message.content, embed=message.embeds[0])
            except Exception as e:
                print(e)

def setup(bot):
    s = YoutubeCom(bot)
    bot.add_cog(s)
