from globals import channel_info

def handle_HOSTTARGET(s, data):
    channel = data['args'][0]
    target = data['message'][0]
    if target == "-":
        channel_info[channel]['hosttarget'] = None
    else:
        channel_info[channel]['hosttarget'] = target
#end def
