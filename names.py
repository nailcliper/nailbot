from globals import channel_info

def handle_NAMES(s, data):
    channel = data['args'][2]
    names  = data['message'].split()
    for n in names:
        if n not in channel_info[channel]['users']:
            channel_info[channel]['users'].add(n)
    #end for
#end def
