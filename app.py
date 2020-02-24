import traceback
from twitch_socket import s
from globals import NICK, PASS, CHAN
from notice import handle_NOTICE
from privmsg import handle_PRIVMSG
from usernotice import handle_USERNOTICE
from join import handle_JOIN
from part import handle_PART
from names import handle_NAMES
from hosttarget import handle_HOSTTARGET

def parseData(line):
    data = {}
    lines = line.split(' ')
    #Parse Tags
    tags = {}
    if lines[0][0] == '@':
        temp = lines.pop(0)
        temp = temp[1:].split(";")
        for tag in temp:
            kv = tag.split('=')
            tags[kv[0]] = kv[1]
            if (kv[0] == 'badge-info' or kv[0] == 'badges') and kv[1]:
                badges = {}
                infos = kv[1].split(',')
                for info in infos:
                    badge_kv = info.split('/')
                    badges[badge_kv[0]] = badge_kv[1]
                tags[kv[0]] = badges
            #end if
        #end for
    #end if
    data['tags'] = tags
    
    #Parse prefix
    data['prefix'] = ''
    if  lines[0][0] == ':':
        data['prefix'] = lines.pop(0)[1:]
    #end if
    
    #Parse Command and Args
    data['command'] = lines.pop(0)
    data['args'] = []
    while lines:
        if lines[0][0] != ':':
            data['args'].append(lines.pop(0))
        else:
            break
    
    #Parse Message
    message = ''
    while lines:
        message += ' ' + lines.pop(0)
    message = message[2:]
    if message[:7] == "ACTION":
        message = message[7:-1]
    data['message'] = message.split()
    
    return data
#end def

def processData(data):
    command = data['command']
    if not command:
        pass
    
    #Twitch IRC: Membership
    #JOIN: Join a specified chat room in a channel
    elif command == "JOIN":
        handle_JOIN(s, data)
    
    #MODE: Gain/lose moderator status in a channel
    
    #NAMES: List current chatters in a channel
    elif command == "353":
        handle_NAMES(s,data)
    
    #PART: Depart from a channel
    elif command == "PART":
        handle_PART(s,data)
    
    #Twitch IRC: Commands:
    #CLEARCHAT: Purges a user's message(s), typically after a user is banned from chat or timed out
    
    #CLEARMSG: Single message removal on a channel. This is triggered via /delete <target-msg-ig> on IRC
    
    #HOSTTARGET: Channel starts or stops host mode
    elif command == "HOSTTARGET":
        handle_HOSTTARGET(s, data)
    #NOTICE: General notices from the server
    elif command == "NOTICE":
        handle_NOTICE(s, data)
    
    #RECONNECT: Rejoin channels after a restart
    
    #ROOMSTATE: Identifies the channel's chat settings (e.g. slow mode duration)
    
    #USERNOTICE: Announces Twitch-specific events to the channel (e.g. subscription notification)
    elif command == "USERNOTICE":
        handle_USERNOTICE(s, data)
    
    #USERSTATE: Identifies a user's chat settings or properties (e.g. chat color)
    
    #Twitch IRC: Tags
    #GLOBALUSERSTATE Provides data about the current logged-in user
    
    #PRIVMSG: Send a message to a channel
    elif command == "PRIVMSG":
        handle_PRIVMSG(s, data)
    
    
    #PING: The server will send you a PING :tmi.twitch.tv. 
    #      To ensure that your connection to the server is not prematurely terminated, reply with PONG :tmi.twitch.tv.
    elif command == "PING":
        s.send_front("PONG :tmi.twitch.tv")

#end def

s.connect()

while True:
    try:
        while(len(s.RECV_QUEUE) > 0):
            lines = s.RECV_QUEUE.pop().split('\r\n')
            for line in lines:
                if len(line) > 0:
                    data = {}
                    data = parseData(line)
                    print("<- " + line)
                    print("Data: \n",data,'\n')
                    
                    processData(data)
    except Exception as e:
        with open("traceback.txt",'a') as f:
            err = traceback.format_exc()
            print(err)
            f.write(err+'\n\n','a')
            f.close()
        #end open
#end while
