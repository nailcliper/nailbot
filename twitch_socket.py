import socket
import threading
from globals import BUF_SIZE, SEND_QUEUE, RECV_QUEUE

class Socket:
    def __init__(self):
        self.s = socket.socket()
        self.connected = False
        self.receiver = threading.Thread(target=self.recv_all)
        self.receiver.setDaemon(True)
        self.sender = threading.Thread(target=self.send_all)
        self.sender.setDaemon(True)

    def connect(self, host, port):
        self.s.connect((host,port))
        self.receiver.start()
        self.sender.start()

    def recv_all(self):
        while True:
            data = ''
            while data[-2:] != '\r\n':
                data += self.s.recv(BUF_SIZE).decode('utf-8')
            RECV_QUEUE.append(data)
    #end def
    
    def send_all(self):
        while True:
            while len(SEND_QUEUE) > 0:
                message = SEND_QUEUE.pop(0)
                self.s.send(bytes(message + '\r\n',"UTF-8"))
                print("-> " + message + '\n')
    #end def
    
    def send(self, m):
        SEND_QUEUE.append(m)
    
    def send_msg(self, message, channel):
        m = "PRIVMSG #" + channel + " :" + message
        SEND_QUEUE.append(m)

    def join_channel(self,  channel):
        m = "JOIN #" + channel
        SEND_QUEUE.append(m)
#end class

s = Socket()
