from globals import channels

def handle_PART(s, data):
    username = data['prefix'].split('!')[0]
    channel = data['args'][0]
    if username in channels[channel].userlist:
        channels[channel].userlist.remove(username)
#end def
