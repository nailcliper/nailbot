from globals import channels

def handle_HOSTTARGET(s, data):
    channel = data['args'][0]
    target = data['message'][0]
    if target == "-":
        channels[channel].hosttarget = None
        channels[channel].subcount = 0
    else:
        channels[channel].hosttarget = target
#end def
