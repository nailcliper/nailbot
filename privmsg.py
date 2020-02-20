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

timers = {}
class ChannelTimer():
    timer = None
    set_time = None
    start_time = None
    running = False
#end class

def get_username(data):
    if len(data['tags']['display-name']) > 0:
        return data['tags']['display-name']
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
    badges = data['tags']['badges']
    if username == NICK:
        level = 0
    elif username.lower() in userlevels:
        level = userlevels[username.lower()]
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
    timers[channel].running = False

def handle_PRIVMSG(s, data):
    username = get_username(data)
    userlevel = get_userlevel(username, data)
    channel = data['args'][0]
    command = data['message'][0]
    print(username,":",userlevel)
    
    if "bits" in data:
        if channel == "#chewiemelodies":
            chews = int(data['bits']) * 10
            if username == "ananonymouscheerer":
                winner = random.choice(channels[channel].userlist)
                msg = "!add "+str(chews)+" "+winner
                s.msg(channel,msg)
            else:
                msg = "!add "+str(chews)+" "+username
                s.msg(channel,msg)
    #end if
    
    if "sudoku" in ' '.join(data['message']).lower() and channel == "#chewiemelodies":
        if all (k not in data['tags']['badges'] for k in ("moderator","broadcaster","staff","admin","global_mod")):
            s.msg(channel,"/timeout "+username+" 120")
            s.msg(channel,"! chewieSudoku "+username+" got their guts spilled! chewieSudoku")
        #end if
    
    elif "yuuki mod" in ' '.join(data['message']).lower() and userlevel <= 3:
        s.msg(channel,"WutFace")
    
    if command == "!count" and data['message'][1]:
        key = "count_"+data['message'][1]
        if key in variables:
            msg = variables[key]
            if key == "river":
                msg = "River has flowed "+msg+" times chewieRiver"
            elif key == "nier":
                msg = "The Weight of the World is "+msg+" tons of android bodies chewieHuh"
            s.msg(channel, msg)
    #end  if
    
    elif command == "!countadd" and data['message'][1] and userlevel <= 3:
        key = "count_"+data['message'][1]
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
    
    elif command == "!countsub" and data['message'][1] and userlevel <= 3:
        key = "count_"+data['message'][1]
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
        if channel in timers and timers[channel].running:
            if len(data['message']) >= 2 and data['message'][1] == "stop":
                timers[channel].timer.cancel()
                timers[channel].running = False
                s.msg(channel,"Timer Stopped")
            else:
                elapsed_time = int(timers[channel].set_time - (time.time() - timers[channel].start_time))
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
        elif len(data['message']) >= 2 and data['message'][1].isnumeric() :
            set_time = int(data['message'][1])
            if len(data['message']) >= 3:
                if data['message'][2] == 'm':
                    set_time *= 60
                elif data['message'][2] == 'h':
                    set_time *= 3600
            #end if
            msg = "BongoPenguin Time Up! BongoPenguin"
            timers[channel] = ChannelTimer()
            timers[channel].timer = Timer(set_time,timeup,(s,channel,msg))
            timers[channel].timer.start()
            timers[channel].start_time = time.time()
            timers[channel].set_time = set_time
            timers[channel].running = True
            
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
    
    elif command == "!host" and userlevel <= 5 and channels[channel].hosttarget:
        msg = ''
        if len(data['message']) >= 2 and userlevel <= 3:
            if data['message'][1][0] == '@':
                msg += data['message'][1]
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
    
#end def
