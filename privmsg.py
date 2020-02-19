from globals import NICK, channel_info
import random

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
with open("userlevels.txt") as f:
    for line in f:
        (key, val) = line.split()
        userlevels[key] = val
    f.close()
#end open

def get_userlevel(username, data):
    badges = data['tags']['badges']
    if username == NICK:
        level = 0
    elif username in userlevels:
        level = userlevels[username]
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

def handle_PRIVMSG(s, data):
    username = get_username(data)
    userlevel = get_userlevel(username, data)
    channel = data['args'][0]
    print(username,":",userlevel)
    
    if "bits" in data:
        if channel == "#chewiemelodies":
            chews = int(data['bits']) * 10
            if username == "ananonymouscheerer":
                winner = random.choice(channel_info["#chewiemelodies"]['users'])
                msg = "!add "+str(chews)+" "+winner
                s.msg(channel,msg)
            else:
                msg = "!add "+str(chews)+" "+username
                s.msg(channel,msg)
    #end if
    
    if "sudoku" in data['message'] and channel == "#chewiemelodies":
        if 'moderator' not in data['tags']['badges'] and 'broadcaster' not in data['tags']['badges']:
            pass
            
    elif "yuuki mod" in data['message'] and userlevel <= 3:
        s.msg(channel,"WutFace")
    
#end def
