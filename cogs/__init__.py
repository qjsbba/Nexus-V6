from __future__ import annotations
from core import Astroz
from colorama import Fore
import pyfiglet


#____________ Commands ___________

#####################3
from .commands.help import Help
from .commands.youtube import Youtube
from .commands.encryption import Encryption
from .commands.general import General
from .commands.react import react
from .commands.music import Music
from .commands.autorole import AutoRole
from .commands.Profile import Profile
from .commands.moderation import Moderation
from .commands.anti import Security
from .commands.Waifu import Waifu
from .commands.alt import AntiAlt
from .commands.stats import Stats
from .commands.raidmode import Raidmode
from .commands.welcome import Welcomer
from .commands.fun import Fun
from .commands.extra import Extra
from .commands.owner import Owner
from .commands.vcroles import Voice
from .commands.role import Server

from .commands.ignore import Ignore
from .commands.vanityroles import Vanityroles
from .commands.vcrole import Invcrole
from .commands.pfps import pfps
from .commands.verification import Verification
from .commands.Afk import AFK
from .commands.media import Media
from .commands.serverinfo import Info
from .commands.extra2 import Reminder
from .commands.star import Starboard
from .commands.guildbl import bl
from .commands.boost import boost
from .commands.giveaway import giveaway
from .commands.ticket import Ticket
#from .commands.Autorole import cool908
from .commands.jsk import Jsk
from .commands.j2c import voice
from .commands.reactionrole import void
from .commands.message import Message
from .commands.activityrole import ActivityRole
from .commands.sticky import Sticky
#____________ Events _____________
from .events.antiban import antiban
from .events.antichannel import antichannel
from .events.antiguild import antiguild
from .events.antirole import antirole
from .events.antibot import antibot
from .events.antikick import antikick
from .events.antiprune import antiprune
from .events.antiwebhook import antiwebhook
from .events.antiping import antipinginv
from .events.antiemoji import antiemoji
from .events.antintegration import antintegration
from .events.antispam import AntiSpam
from .events.autoblacklist import AutoBlacklist
from .events.Errors import Errors
from .events.on_guild import Guild
from .events.greet2 import greet
from .events.voiceupdate import Vcroles2
from .events.member_update import member_update
from .events.join import Join
from .events.boost2 import bst
from .events.boost3 import Boost3

##############33cogs#############
from .commands.anti1 import hacker1
from .commands.extra1 import hacker11
from .commands.general1 import hacker111
from .commands.giveaway1 import gw1
from .commands.raidmode1 import hacker1111
from .commands.mod2 import hacker111111
from .commands.star1 import velo
from .commands.boost1 import velo1
from .commands.music1 import hacker1111111 

from .commands.voice import hacker1111111111111 
from .commands.verification1 import ver1
from .commands.welcome1 import hacker11111111111111 
from .commands.ticket1 import cool16
from .commands.vanityroles1 import hacker111111111111
#from .commands.autorole1 import cool908
from .commands.pfps1 import cool191
from .commands.jsk1 import jsk1


author = "cosmic team"
ravan = pyfiglet.figlet_format("Nexuss")
made_by = f"[ Made By {author} ]"
centered_made_by = made_by.center(len(ravan))
console_width = 120
centered_ascii_art = "\n".join(line.center(console_width) for line in ravan.split("\n"))
output = centered_ascii_art + f"{centered_made_by}\n"
menu = f"""{Fore.RED} {output}{Fore.GREEN}\n"""
print(menu)

async def setup(bot: Astroz):
  await bot.add_cog(Help(bot))
  print(Fore.RED+'Help Command Loaded')
  await bot.add_cog(General(bot))
  print('General Command Loaded')
  await bot.add_cog(Music(bot))
  print('Music Command Loaded')
  await bot.add_cog(Encryption(bot))
  print('Encryption Command Loaded')
  await bot.add_cog(react(bot))
  print('React Command Loaded')
  await bot.add_cog(Youtube(bot))
  print('Youtube Command Loaded')
  await bot.add_cog(Moderation(bot))
  print('Moderation Command Loaded')
  await bot.add_cog(Security(bot))
  print('Security Command Loaded')
  await bot.add_cog(Raidmode(bot))
  print('Raidmode Command Loaded')
  await bot.add_cog(Welcomer(bot))
  print('Welcomer Command Loaded')
  await bot.add_cog(Fun(bot))
  print('Fun Command Loaded')
  await bot.add_cog(Extra(bot))
  print('Extra Command Loaded')
  await bot.add_cog(Voice(bot))
  print('Voice Command Loaded')
  await bot.add_cog(Owner(bot))
  print('Owner Command Loaded')
  await bot.add_cog(Server(bot))
  print('Server Command Loaded')
  await bot.add_cog(Vanityroles(bot))
  print('VanityRoles Command Loaded')
  await bot.add_cog(Ignore(bot))
  print('Ignore Command Loaded')
  await bot.add_cog(Invcrole(bot))
  print('Invcrole Command Loaded')
  await bot.add_cog(pfps(bot))
  print('Pfps Command Loaded')
  await bot.add_cog(Verification(bot))
  print('Verification Command Loaded')
  await bot.add_cog(AFK(bot))
  print('Afk Command Loaded')
  await bot.add_cog(Media(bot))
  print('Media Command Loaded')
  await bot.add_cog(Info(bot))
  print('Info Command Loaded')
  await bot.add_cog(Reminder(bot))
  print('Reminder Command Loaded')
  await bot.add_cog(Starboard(bot))
  print('Starboard Command Loaded')
  await bot.add_cog(bl(bot))
  print('Bl Command Loaded')
  await bot.add_cog(boost(bot))
  print('Boost Command Loaded')
  await bot.add_cog(giveaway(bot))
  print('Giveaway Command Loaded')
#  await bot.add_cog(Ticket(bot))
 # print('Ticket Command Loaded')
 # await bot.add_cog(autorole(bot))
  await bot.add_cog(Jsk(bot))
  print('Jsk Command Loaded')
  await bot.add_cog(Profile(bot))
  print('Profile Command Loaded')
  await bot.add_cog(AntiAlt(bot))
  print('Antialt Command Loaded')
  await bot.add_cog(AutoRole(bot))
  print('Autorole Command Loaded')
  await bot.add_cog(Waifu(bot))
  print('Waifu Command Loaded')
  await bot.add_cog(Stats(bot))
  print('Stats Command Loaded')
  await bot.add_cog(void(bot))
  print("ReactionRole Command Loaded")
  await bot.add_cog(voice(bot))
  print("J2c Command Loaded")
  await bot.add_cog(Message(bot))
  print("Message Command Loaded")
  await bot.add_cog(ActivityRole(bot))
  print("Activity Role Command Loaded")  
  await bot.add_cog(Sticky(bot))
  print("Sticky Command Loaded")
####################

  await bot.add_cog(hacker1(bot))
  await bot.add_cog(hacker11(bot))
  await bot.add_cog(hacker111(bot))
  await bot.add_cog(gw1(bot))
  await bot.add_cog(hacker1111(bot))
  await bot.add_cog(hacker111111(bot))
  await bot.add_cog(velo(bot))
  await bot.add_cog(velo1(bot))
  await bot.add_cog(hacker1111111(bot)) 
  await bot.add_cog(hacker1111111111111(bot))
  await bot.add_cog(hacker11111111111111(bot))
  await bot.add_cog(cool16(bot))
  await bot.add_cog(ver1(bot))
  await bot.add_cog(hacker111111111111(bot))
#  await bot.add_cog(cool908(bot))
  await bot.add_cog(cool191(bot))
  await bot.add_cog(jsk1(bot))


###########################events################3
  
  await bot.add_cog(antiban(bot))
  print(Fore.BLUE+'Antiban Events Loaded')
  await bot.add_cog(antichannel(bot))
  print('Antichannel Events Loaded')
  await bot.add_cog(antiguild(bot))
  print('Antiguild Events Loaded')    
  await bot.add_cog(antirole(bot))
  print('Antirole Events Loaded')
  await bot.add_cog(antibot(bot))
  print('Antibot Events Loaded')
  await bot.add_cog(antikick(bot))
  print('Antikick Events Loaded')
  await bot.add_cog(antiprune(bot))
  print('Antiprune Events Loaded')
  await bot.add_cog(antiwebhook(bot))
  print('Antiwebhook Events Loaded')
  await bot.add_cog(antipinginv(bot))
  print('Antipinginv Events Loaded')
  await bot.add_cog(antiemoji(bot))
  print('Antiemostick Events Loaded')    
  await bot.add_cog(antintegration(bot))
  print('Antintegration Events Loaded')  
  await bot.add_cog(AntiSpam(bot))
  print('AntiSpam Events Loaded')
  await bot.add_cog(AutoBlacklist(bot))
  print('AutoBlacklist Events Loaded')
  await bot.add_cog(Guild(bot))
  print('Guild Events Loaded')
  await bot.add_cog(Errors(bot))
  print('Errors Events Loaded')
  await bot.add_cog(greet(bot))
  print('Greet Events Loaded')
  await bot.add_cog(Vcroles2(bot))
  print('Vcroles2 Events Loaded')
  await bot.add_cog(member_update(bot))
  print('Member_update Events Loaded')
  await bot.add_cog(Join(bot))
  print('Join Events Loaded')
  await bot.add_cog(bst(bot))
  print('Bst Events Loaded')
  await bot.add_cog(Boost3(bot))
  print('Boost3 Events Loaded')