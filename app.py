from twitch_socket import s, parseData, processData
from globals import HOST, PORT, NICK, PASS, CHAN

s.connect(HOST,PORT)
s.send("PASS " + PASS)
s.send("NICK " + NICK)
s.send("CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
s.join_channel(CHAN)

while True:
    lines = s.recv_all().split('\r\n')
    for line in lines:
        if len(line) > 0:
            data = {}
            print("<- " + line)
            
            data = parseData(line)
            print("Data: \n",data,'\n')
            
            processData(data)
