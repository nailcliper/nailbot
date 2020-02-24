from globals import channels

def handle_NAMES(s, data):
    channel = data['args'][2]
    names  = data['tokens']
    for n in names:
        if n not in channels[channel].userlist:
            channels[channel].userlist.add(n)
    #end for
#end def
