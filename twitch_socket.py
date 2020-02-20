import socket
import threading
from globals import NICK, PASS, CHAN, channels, Channel

class Socket:
    def __init__(self):
        self.s = socket.socket()
        self.BUF_SIZE = 4096
        self.RECV_QUEUE = []
        self.SEND_QUEUE = []
        self.connected = False
        self.receiver = threading.Thread(target=self.recv_all)
        self.receiver.setDaemon(True)
        self.sender = threading.Thread(target=self.send_all)
        self.sender.setDaemon(True)
    #end def

    def connect(self, host="irc.twitch.tv", port=6667):
        self.s.connect((host,port))
        self.connected = True
        self.RECV_QUEUE = []
        self.SEND_QUEUE = []
        self.receiver.start()
        self.sender.start()
        self.send("PASS " + PASS)
        self.send("NICK " + NICK)
        self.send("CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
        for chan in CHAN:
            s.join_channel(chan)
    #end def
    
    def reconnect(self, host='irc.twitch.tv',port=6667):
        self.backoff_count = 0
        while not self.connected:
            self.s.settimeout(pow(2,self.backoff_count))
            print("Reconnecting: Timeout in",pow(2,self.backoff_count))
            self.backoff_count += 1
            self.connect()
        self.s.settimeout(0)
    #end def
    
    def recv_all(self):
        while True:
            try:
                data = ''
                while data[-2:] != '\r\n':
                    data += self.s.recv(self.BUF_SIZE).decode('utf-8')
                self.RECV_QUEUE.append(data)
            except self.s.error:
                self.connected = False
                self.reconnect()
    #end def
    
    def send_all(self):
        while True:
            try:
                while len(self.SEND_QUEUE) > 0:
                    message = self.SEND_QUEUE.pop(0)
                    self.s.send(bytes(message + '\r\n',"UTF-8"))
                    print("-> " + message + '\n')
            except self.s.error:
                self.connected = False
                self.reconnect()
    #end def
    
    def send(self, m):
        self.SEND_QUEUE.append(m)
    
    def msg(self, channel, message):
        m = "PRIVMSG " + channel + " :" + message
        self.SEND_QUEUE.append(m)

    def join_channel(self, channel):
        m = "JOIN " + channel
        channels[channel] = Channel()
        self.SEND_QUEUE.append(m)
#end class

s = Socket()
