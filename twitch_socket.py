import socket
from globals import BUF_SIZE

class Socket:
    def __init__(self):
        self.s = socket.socket()

    def connect(self, host, port):
        self.s.connect((host,port))

    def recv_all(self):
        data = ''
        while True:
            data += self.s.recv(BUF_SIZE).decode('utf-8')
            if data[-2:] == '\r\n':
                return data
    #end def
    
    def send(self, message):
        self.s.send(bytes(message + '\r\n',"UTF-8"))
        print("-> " + message + '\n')

    def send_msg(self, message, channel):
        self.send("PRIVMSG #" + channel +  ":" + message)

    def join_channel(self,  channel):
        self.send("JOIN #" + channel)
#end class

s = Socket()

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
    command = input['command']
    if not command:
        pass
    
    #GLOBALUSERSTATE Provides data about the current logged-in user
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
    
    #PING: The server will send you a PING :tmi.twitch.tv. 
    #      To ensure that your connection to the server is not prematurely terminated, reply with PONG :tmi.twitch.tv.
    elif command == "PING":
        s.send("PONG :tmi.twitch.tv")
    
    pass
#end def