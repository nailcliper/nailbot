import socket
from globals import HOST, PORT, NICK, PASS, CHAN, BUF_SIZE

def connect(host, port):
    s = socket.socket()
    s.connect((host,port))
    return s

def recv_all(s):
    data = ''
    while True:
        data += s.recv(BUF_SIZE).decode('utf-8')
        if data[-2:] == '\r\n':
            return data

def send(s, message):
    s.send(bytes(message + '\r\n',"UTF-8"))
    print(message)

def send_message(s, message, channel):
    send(s, "PRIVMSG #" + channel +  ":" + message)
    print(message)

def join_channel(s, channel):
    send(s, "JOIN #" + channel)

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

def processData(input):
    #GLOBALUSERSTATE Provides  data about the current logged-in user
    #PRIVMSG: Send a message to a channel
    
    #JOIN: Join a specified chat room in a channel
    #MODE: Gain/lose moderator status in a channel
    #NAMES: List current chatters in a channel
    #PART: Depart from a channel
    
    #CLEARCHAT: Purgeg a user's message(s), typically after a user is banned from chat or timed out
    #CLEARMSG: Single message removal on a channel. This is triggered via /delete <target-msg-ig> on IRC
    #HOSTTARGET: Channel starts or stops host mode
    #NOTICE: General notices from the server
    #RECONNECT: Rejoin channels after a restart
    #ROOMSTATE: Identifies the channel's chat settings (e.g. slow mode duration)
    #USERNOTICE: Announces Twitch-specific events to the channel (e.g. subscription notification)
    #USERSTATE: Identifies a user's chat settings or properties (e.g. chat color)
    pass
#end def

s = connect(HOST, PORT)
send(s, "PASS " + PASS)
send(s, "NICK " + NICK)
send(s, "CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
join_channel(s, CHAN)

while True:
    lines = recv_all(s).split('\r\n')
    for line in lines:
        if len(line) > 0:
            data = {}
            print(line)
            
            data = parseData(line)
            print("Data: \n",data,'\n\n')
