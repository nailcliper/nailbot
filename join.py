from globals import NICK, channel_info

def handle_JOIN(s, data):
    username = data['prefix'].split('!')[0]
    channel = data['args'][0]
    if username not in channel_info[channel]['users']:
        channel_info[channel]['users'].add(username)
#end def
