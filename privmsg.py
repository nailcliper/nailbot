#data['tags']:
#badge-Info:    Metadata related to the chat badges in the 'badges' tag.
#               Currently only used for 'subscriber' to indicate the exact number of months the user has been a subscriber

#badges:        Comma separated list of chat badges and the version of each badge in the format <badge>/<version>
#               Common badges: admin, bits, broadcaster, global_mod, moderator, subscriber, staff, turbo, founder

#bits:          The amount of bits employed by the user.
#               All instances of these regular expressions /(^\|\s)<emote-name>\d+(\s\|$)/ 

#color:         Hexadecimal RGB color code; the empty string if never set

#display-name:  The user's display name, escaped and described in IRCv3 spec. This is empty if never set.

#emotes:        Information to replace text in the message with emote images

#id:            A unique ID for the message

#mod:           1 if the user has a moderator badge, otherise 0

#room-id:       The channel ID

#subscriber:    (Depriciated, use 'badges' instead) 1 if the user has a subscriber badge, otherwise 0

#tmi-send-st:   Timestamp when the server received the message

#turbo:         (Depriciated, use 'badges' instead) 1 if the user has a subscriber badge, otherwise 0

#user-id:       The user's ID

#user-type:     (Depriciated, use 'badges' insteadd) The user's type
#               Valid values: mod, global_mod, admin, staff. If the broadcaster is not any of these types, the field is empty

#data['prefix']:    <username>!<username>@<username>.tmi.twitch.tv

#data['command']:   PRIVMSG

#data['args'][0]:   #<channel>

#data['message']:   <message>

from globals import NICK, channels, variables
import random
import threading
from threading import Timer
import time
import re

regex = re.compile('[W_]+')
regex_bonus = re.compile('bonus[0-9]+')

timers = {}
class ChannelTimer():
    timer = None
    set_time = None
    start_time = None
#end class

def get_username(data):
    if len(data['tags'].get('display-name')) > 0:
        return data['tags'].get('display-name')
    else:
        return data['prefix'].split('!')[0]
#end def

#0 - Me
#1 - Broadcaster
#2 - Mods
#3 - Subs/VIPS
#4 - Users
#5 - Restricted
#6 - Banned
userlevels = {}
with open("userlevels.txt",'r') as f:
    for line in f:
        (key, val) = line.split()
        userlevels[key] = val
    f.close()
#end open

def get_userlevel(username, data):
    badges = data['tags'].get('badges')
    if username == NICK:
        level = 0
    elif username.lower() in userlevels:
        level = int(userlevels[username.lower()])
    elif 'broadcaster' in badges:
        level = 1
    elif 'moderator' in badges:
        level = 2
    elif 'vip' in badges or 'subscriber' in badges:
        level = 3
    else:
        level = 4
    return level
#end def

def timeup(s,channel,message):
    s.msg(channel,message)
    channels[channel].timer = None

def handle_PRIVMSG(s, data):
    username = get_username(data)
    userlevel = get_userlevel(username, data)
    channel = data['args'][0]
    tokens = data['tokens']
    command = tokens[0]

    if "bits" in data['tags']:
        if channel == "#chewiemelodies":
            chews = int(data['tags'].get('bits')) * 10
            userlist = channels[channel].get_userlist()
            chatters = list({x for v in userlist.values() for x in v})
            winner = random.choice(chatters)
            
            if username == "ananonymouscheerer":
                msg = "!add "+str(chews)+" "+winner
                s.msg(channel,msg)
            
            else:
                msg = "!add "+str(chews)+" "+username
                s.msg("#chewiebot",msg)
            #end if
            
            bonus = re.findall(regex_bonus, data['message'])
            #print("bonus:",bonus)
            if bonus:
                bonus_bits = int(bonus[0][5:])
                msg = "!add "+str(bonus_bits)+" "+winner
                s.msg(channel,msg)
            #end if
            
            #print('\n\n',chatters,'\n\n')
    #end if
    
    if username == "rallyboss" and tokens[1] == "Boss" and tokens[2] == "defeated!" and channel == "#chewiemelodies":
        s.msg(channel, "!add 5000 "+tokens[18])
    
    text = re.sub(regex,'',data['message'].lower())
    if "sudoku" in text and channel == "#chewiemelodies":
        if all (k not in data['tags'].get('badges') for k in ("moderator","broadcaster","staff","admin","global_mod")):
            timeout = Timer(0.1,s.msg,(channel,"/timeout "+username+" 120"))
            timeout.start()
            #s.msg(channel,"/timeout "+username+" 120")
            s.msg(channel,"! chewieSudoku "+username+" got their guts spilled! chewieSudoku")
    #end if
    
    elif ("yuuki mod" in data['message'].lower() or "yuukihatsu mod" in data['message'].lower()) and userlevel <= 3:
        s.msg(channel,"WutFace")
    
    if command == "!count" and tokens[1]:
        key = "count_"+tokens[1]
        if key in variables:
            msg = variables[key]
            if key == "river":
                msg = "River has flowed "+msg+" times chewieRiver"
            elif key == "nier":
                msg = "The Weight of the World is "+msg+" tons of android bodies chewieHuh"
            s.msg(channel, msg)
    #end  if
    
    elif command == "!countadd" and len(tokens) > 1 and userlevel <= 3:
        key = "count_"+tokens[1]
        if key in variables:
            variables[key] = str(int(variables[key])+1)
        else:
            variables[key] = "1"
        with open("variables.txt",'w') as f:
            for v in variables:
                f.write(v+" "+variables[v]+'\n')
            f.close()
        #end open
        msg = variables[key]
        if key == "river":
            msg += " chewieRiver"
        elif key == "nier":
            msg += " chewieHuh"
        s.msg(channel, variables[key])
    #end if
    
    elif command == "!countsub" and len(tokens) > 1 and userlevel <= 3:
        key = "count_"+tokens[1]
        if key in variables:
            variables[key] = str(int(variables[key])-1)
            with open("variables.txt",'w') as f:
                for v in variables:
                    f.write(v+" "+variables[v]+'\n')
                f.close()
            #end open
            s.msg(channel, variables[key])
    #end if
    
    elif command == "!timer" and userlevel <= 2:
        if channels[channel].timer:
            timer = channels[channel].timer
            if len(tokens) >= 2 and tokens[1] == "stop":
                timer.cancel()
                channels[channel].timer = None
                s.msg(channel,"Timer Stopped")
            else:
                elapsed_time = int(timer.set_time - (time.time() - timer.start_time))
                seconds = elapsed_time % 60
                elapsed_time = elapsed_time // 60
                minutes = elapsed_time % 60
                hours = elapsed_time // 60
                
                msg = "Remaining Time: "
                if(hours):
                    msg += str(hours)+"h "+str(minutes)+"m "+str(seconds)+"s"
                elif(minutes):
                    msg += str(minutes)+"m "+str(seconds)+"s"
                else:
                    msg += str(seconds)+"s"
                s.msg(channel, msg)
            #end if
        elif len(tokens) >= 2 and tokens[1].isnumeric() :
            set_time = int(tokens[1])
            if len(tokens) >= 3:
                if tokens[2] == 'm':
                    set_time *= 60
                elif tokens[2] == 'h':
                    set_time *= 3600
            #end if
            msg = "BongoPenguin Time Up! BongoPenguin"
            timer = ChannelTimer()
            timer = Timer(set_time,timeup,(s,channel,msg))
            timer.start()
            timer.start_time = time.time()
            timer.set_time = set_time
            channels[channel].timer = timer
            
            seconds = set_time % 60
            set_time = set_time // 60
            minutes = set_time % 60
            hours = set_time // 60
            
            msg = "Timer started for: "
            if(hours):
                msg += str(hours)+"h "+str(minutes)+"m "+str(seconds)+"s"
            elif(minutes):
                msg += str(minutes)+"m "+str(seconds)+"s"
            else:
                msg += str(seconds)+"s"
            s.msg(channel, msg)
        #end if
    #end if
    
    elif command == "!host" and userlevel < 5 and channels[channel].hosttarget:
        msg = ''
        for token in tokens:
            if token[0] == '@':
                msg += token + ' '
        #end if
        if channel == "#itshafu":
            msg += "This is still Hafu's chat, to talk to " + channels[channel].hosttarget + " please visit twitch.tv/" + channels[channel].hosttarget + " omgLurk"
        elif channel == "#chewiemelodies":
            msg += "This is still Chewie's chat, to talk to " + channels[channel].hosttarget + " please visit twitch.tv/" + channels[channel].hosttarget + " chewieLove"
        else:
            msg = ''
        #end if
        if msg:
            s.msg(channel, msg)
    #end if
    
    elif command == "!subcount" and userlevel <= 2:
        subcount = channels[channel].subcount
        if channel == "#itshafu":
            msg = "Today's Pingus: " + str(subcount)
            if subcount >= 100:
                msg += " MetPride"
            elif subcount == 69:
                msg += " ( ͡° ͜ʖ ͡°)"
            elif subcount >= 1:
                msg += " omgHost"
            else:
                msg += " FeelsBadMan"
            s.msg(channel, msg)
        #end if
    #end def
    
    elif command == "!abrasive":
        s.msg(channel, "ABRASIVE - PepePls puu.sh/F2ADg/dbbae5e308.mp3 PepePls")
    
    elif command == "!mimic" or command == "!nico":
        nicos = ["https://i.imgur.com/V514bG3.jpg PunOko", 
             "https://i.redd.it/5al3htpvlus01.gif PunOko 👉🚪",
             "Reeeeeee  NICO Reeeeeee  NICO Reeeeeee  NO Reeeeeee",
             "https://i.imgur.com/Db6wX1G.mp4 PunOko",
             "https://youtu.be/PPRox5ExxHQ 🏎️"
            ]
        s.msg(channel, random.choice(nicos))
    
    elif command == "!yuuki":
        s.msg(channel, "BabyRage")
    
    elif command == "!seppuku":
        s.msg(channel, "/timeout "+username+" 1")
        s.msg(channel, "chewieSudoku")
    
    elif command == "!brenda":
        s.msg(channel, "BRENDA -- http://imgur.com/9KYqgvS")
    
    elif command == "!omgHost":
        s.msg(channel, "omgSide https://i.imgur.com/mW0XwxA.png omgHost")
        
    #elif command == "!summondan" and (userlevel <=  2 or username == "YuukiHatsu"):
    #    userlist = channels[channel].get_userlist()
    #    if "yuukihatsu" not in userlist['moderators']:
    #        s.msg(channel, "ヽ༼ຈل͜ຈ༽ﾉ Goose plucked and Yuuki ban, with this chant, I summon Dan ヽ༼ຈل͜ຈ༽ﾉ")
    #        s.msg(channel, "/ban YuukiHatsu")
    #        s.msg(channel, "/unban YuukiHatsu")
    
    elif command == "!berkut":
        s.msg(channel, "is a butt BabyRage")
    
    elif command == "!ethy":
        s.msg(channel, "ethy show cake BabyRage")
        
    elif command == "!meeb":
        s.msg(channel, "oe omgBunny")
    elif command == "!weeb":
        s.msg(channel, "oe omgAyaya")
    
    elif command == "!nail" or command == "!nailcliper":
        s.msg(channel, "nailclLikeThis ")
    
    elif command == "!nobody":
        s.msg(channel, "nobody loves you FeelsBirthdayMan")
        
    elif command == "dreyer1" and username == "ayedannydre":
        s.msg(channel, "/timeout "+username+" 1")
    
    elif (command == "!gloomy" or command == "!glooby") and userlevel <= 3 and channel == "#itshafu":
        if channels[channel].hosttarget or username == "gloomy___" or userlevel <= 2 or username == "mrabbod":
            s.msg(channel, "omgSax omgSax omgSax")
            s.msg(channel, "omgSax pepeD omgSax")
            s.msg(channel, "omgSax omgSax omgSax")
        else:
            s.msg(channel, "omgSax pepeDHaw omgSax")
    
    elif command == "!zap":
        s.msg(channel, "https://i.imgur.com/FkcUOwx.png omgAyaya")
#end def
