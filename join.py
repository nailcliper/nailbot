from globals import NICK, channels

def handle_JOIN(s, data):
    username = data['prefix'].split('!')[0]
    channel = data['args'][0]
    if username not in channels[channel].userlist:
        channels[channel].userlist.add(username)
#end def
