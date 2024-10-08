import json, sys, os
import discord
from discord.ext import commands
from core import Context
import aiohttp
import time


def updateDB1(guildID, data):
    with open("db/bst.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("db/bst.json", "w") as config:
        config.write(newdata)


def getDB1(guildID):
    with open("db/bst.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "boost": {
                "autodel": 0,
                "channel": [],
                "color": "",
                "embed": False,
                "footer": "",
                "image": "",
                "message": "<<boost.user_mention>> Thank you for boosting <<boost.server_name>>",
                "ping": False,
                "title": "",
                "thumbnail": ""
            },
            "boost1": {
                "role": []
            }
        }
        updateDB1(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateDB(guildID, data):
    with open("db/database1.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("db/database1.json", "w") as config:
        config.write(newdata)


def getDB(guildID):
    with open("db/database1.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "welcome": {
                "autodel": 0,
                "channel": [],
                "color": "",
                "embed": False,
                "footer": "",
                "image": "",
                "message": "<<user.mention>> Welcome To <<server.name>>",
                "ping": False,
                "title": "",
                "thumbnail": ""
            },
            "autorole": {
                "bots": [],
                "humans": []
            },
            "vcrole": {
                "bots": "",
                "humans": ""
            }
        }
        updateDB(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def getConfig(guildID):
    with open("db/config.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "antiSpam": False,
            "antiLink": False,
            "admins": [],
            "extowner": [],
            "adminrole": None,
            "whitelisted": [],
            "punishment": "ban",
            "prefix": "?",
            "staff": None,
            "vip": None,
            "girl": None,
            "guest": None,
            "frnd": None,
            "owner": None,
            "coown": None,
            "headadmin": None,
            "admin": None,
            "mod": None,
            "gmod": None,
            "gadmin": None,
            "headmod": None,
            "wlrole": None,
            "reqrole": None
        }
        updateConfig(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateConfig(guildID, data):
    with open("db/config.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("db/config.json", "w") as config:
        config.write(newdata)


def add_user_to_blacklist(user_id: int) -> None:
    with open("db/blacklist.json", "r") as file:
        file_data = json.load(file)
        if str(user_id) in file_data["ids"]:
            return

        file_data["ids"].append(str(user_id))
    with open("db/blacklist.json", "w") as file:
        json.dump(file_data, file, indent=4)


def remove_user_from_blacklist(user_id: int) -> None:
    with open("db/blacklist.json", "r") as file:
        file_data = json.load(file)
        file_data["ids"].remove(str(user_id))
    with open("db/blacklist.json", "w") as file:
        json.dump(file_data, file, indent=4)


def update_vanity(guild, code):
    with open('db/vanity.json', 'r') as vanity:
        vanity = json.load(vanity)
    vanity[str(guild)] = str(code)
    new = json.dumps(vanity, indent=4, ensure_ascii=False)
    with open('db/vanity.json', 'w') as vanity:
        vanity.write(new)


def blacklist_check():

    def predicate(ctx):
        with open("db/blacklist.json") as f:
            data = json.load(f)
            if str(ctx.author.id) in data["ids"]:
                return False
            return True

    return commands.check(predicate)


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def getbadges(userid):
    with open("db/badges.json", "r") as f:
        data = json.load(f)
    if str(userid) not in data:
        default = []
        makebadges(userid, default)
        return default
    return data[str(userid)]


def makebadges(userid, data):
    with open("db/badges.json", "r") as f:
        badges = json.load(f)
    badges[str(userid)] = data
    new = json.dumps(badges, indent=4, ensure_ascii=False)
    with open("db/badges.json", "w") as w:
        w.write(new)


def getanti(guildid):
    with open("db/anti.json", "r") as config:
        data = json.load(config)
    if str(guildid) not in data["guilds"]:
        default = "off"
        updateanti(guildid, default)
        return default
    return data["guilds"][str(guildid)]


def updateanti(guildid, data):
    with open("db/anti.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildid)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("db/anti.json", "w") as config:
        config.write(newdata)


class Timer:
    __slots__ = ("start_time", "end_time")

    def __init__(self) -> None:
        self.start_time: float | None = None
        self.end_time: float | None = None

    def __enter__(self):
        self.start()
        return self

    async def __aenter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.stop()

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.stop()

    def start(self) -> None:
        self.start_time = time.perf_counter()

    def stop(self) -> None:
        self.end_time = time.perf_counter()

    def __str__(self) -> str:
        return str(self.total_time)

    def __int__(self) -> int:
        return int(self.total_time)

    def __repr__(self) -> str:
        return f"<Timer time={self.total_time}>"

    @property
    def total_time(self) -> float:
        if self.start_time is None:
            raise ValueError("Timer has not been started")
        if self.end_time is None:
            raise ValueError("Timer has not been stopped")
        return self.end_time - self.start_time


def format_seconds(seconds: float, *, friendly: bool = False) -> str:

    seconds = round(seconds)

    minute, second = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)

    days, hours, minutes, seconds = (
        round(day),
        round(hour),
        round(minute),
        round(second),
    )

    if friendly:
        day = f"{days}d " if days != 0 else ""
        hour = f"{hours}h " if hours != 0 or days != 0 else ""
        minsec = f"{minutes}m {seconds}s"
        return f"{day}{hour}{minsec}"
    day = f"{days:02d}:" if days != 0 else ""
    hour = f"{hours:02d}:" if hours != 0 or days != 0 else ""
    minsec = f"{minutes:02d}:{seconds:02d}"
    return f"{day}{hour}{minsec}"





def add_channel_to_ignore(user_id: int) -> None:
    with open("db/ignore.json", "r") as file:
        file_data = json.load(file)
        if str(user_id) in file_data["ids"]:
            return

        file_data["ids"].append(str(user_id))
    with open("db/ignore.json", "w") as file:
        json.dump(file_data, file, indent=4)


def remove_channel_from_ignore(user_id: int) -> None:
    with open("db/ignore.json", "r") as file:
        file_data = json.load(file)
        file_data["ids"].remove(str(user_id))
    with open("db/ignore.json", "w") as file:
        json.dump(file_data, file, indent=4)


def ignore_check():

    def predicate(ctx):
        with open("db/ignore.json") as f:
            data = json.load(f)
            if str(ctx.channel.id) in data["ids"]:
                return False
            return True

    return commands.check(predicate)




def getlogger(guildid):
  with open("db/logs.json", "r") as ok:
    data = json.load(ok)
  if str(guildid) not in data:
    default = {
      "channel": ""
    }
    makelogger(guildid, default)
    return default
  return data[str(guildid)]

    
def makelogger(guildid, data):
  with open("db/logs.json", "r") as f:
    logs = json.load(f)
  logs[str(guildid)] = data
  new = json.dumps(logs, indent=4, ensure_ascii=False)
  with open("db/logs.json", "w") as idk:
    idk.write(new)





def updateHacker(guildID, data):
    with open("db/events.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("db/events.json", "w") as config:
        config.write(newdata)


def getHacker(guildID):
    with open("db/events.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "antinuke": {
                "antirole-delete": True,
                "antirole-create": True,
                "antirole-update": True,
                "antichannel-create": True,
                "antichannel-delete": True,
                "antichannel-update": True,
                "antiban": True,
                "antikick": True,
                "antiwebhook": True,
                "antibot": True,
                "antiserver": True,
                "antiping": True,
                "antiprune": True,
                "antiemoji-delete": True,
                "antiemoji-create": True,
                "antiemoji-update": True
            }
        }
        updateHacker(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]
###

def iuser2(guildID):
    with open("db/ibypass.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "ibypass": []
        }
        iuser3(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def iuser3(guildID, data):
    with open("db/ibypass.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("db/ibypass.json", "w") as config:
        config.write(newdata)

####
def iuser(guildID):
    with open("db/iuser.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "iuser": []
        }
        iuser1(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def iuser1(guildID, data):
    with open("db/iuser.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("db/iuser.json", "w") as config:
        config.write(newdata)

def iuser_check():
    def predicate(ctx):
        with open("db/iuser.json", "r") as file:
            data = json.load(file)
            guild_id = str(ctx.guild.id)
            if guild_id in data["guilds"] and str(ctx.author.id) in data["guilds"][guild_id]["iuser"]:
                return False
            return True

    return commands.check(predicate)
