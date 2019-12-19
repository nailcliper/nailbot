from twitch_socket import s
from globals import HOST, PORT, NICK, PASS, CHAN, RECV_QUEUE
from notice import handle_NOTICE
from privmsg import handle_PRIVMSG
from usernotice import handle_USERNOTICE

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
    data['message'] = message[2:]
    
    return data
#end def

def processData(data):
    command = data['command']
    if not command:
        pass
    
    #Twitch IRC: Membership
    #JOIN: Join a specified chat room in a channel
    
    #MODE: Gain/lose moderator status in a channel
    
    #NAMES: List current chatters in a channel
    
    #PART: Depart from a channel
    
    #Twitch IRC: Commands:
    #CLEARCHAT: Purgeg a user's message(s), typically after a user is banned from chat or timed out
    
    #CLEARMSG: Single message removal on a channel. This is triggered via /delete <target-msg-ig> on IRC
    
    #HOSTTARGET: Channel starts or stops host mode
   
    #NOTICE: General notices from the server
    elif command == "NOTICE":
        handle_NOTICE(data)
    
    #RECONNECT: Rejoin channels after a restart
    
    #ROOMSTATE: Identifies the channel's chat settings (e.g. slow mode duration)
    
    #USERNOTICE: Announces Twitch-specific events to the channel (e.g. subscription notification)
    elif command == "USERNOTICE":
        handle_USERNOTICE(data)
    
    #USERSTATE: Identifies a user's chat settings or properties (e.g. chat color)
    
    #Twitch IRC: Tags
    #GLOBALUSERSTATE Provides data about the current logged-in user
    
    #PRIVMSG: Send a message to a channel
    elif command == "PRIVMSG":
        handle_PRIVMSG(data)
    
    
    #PING: The server will send you a PING :tmi.twitch.tv. 
    #      To ensure that your connection to the server is not prematurely terminated, reply with PONG :tmi.twitch.tv.
    elif command == "PING":
        s.send("PONG :tmi.twitch.tv")
#end def

s.connect(HOST,PORT)
s.send("PASS " + PASS)
s.send("NICK " + NICK)
s.send("CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
s.join_channel(CHAN)

while True:
    while(len(RECV_QUEUE) > 0):
        lines = RECV_QUEUE.pop().split('\r\n')
        for line in lines:
            if len(line) > 0:
                print("<- " + line)
                data = {}
                data = parseData(line)
                print("Data: \n",data,'\n')
                
                processData(data)
#end while
