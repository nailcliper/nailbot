from globals import channel_info

def handle_PART(s, data):
    username = data['prefix'].split('!')[0]
    channel = data['args'][0]
    if username in channel_info[channel]['users']:
        channel_info[channel]['users'].remove(username)
#end def
