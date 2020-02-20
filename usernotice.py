from globals import NICK, channels

def get_genericSubMessage(months,m,y):
    msg = ''
    if months > 1:
        if m==0:
            msg = "bleedPurple "*y
        else:
            msg = "bleedPurple "*y + "<3 "*m
    else:
        msg = "bleedPurple bleedPurple bleedPurple"
    return msg
#end def

def get_hafuSubMessage(months,m,y):
    msg = ''
    if months > 1:
        if m == 0:
            msg = "omgParty " + "omgKirby "*y + "omgParty"
        else:
            msg = "omgKirby "*y + "omgHello "*m + "omgHost"
    else:
        msg = "omgHello omgParty omgHost"
    return msg
#end def

def get_chewieSubMessage(months,m,y):
    msg = ''
    if months > 1:
        if m == 0:
            msg = "chewieRem " + "chewieLove "*y + "chewieXD"
        else:
            msg = "chewieLove "*y + "chewieHype "*m + "chewieHug"
    else:
        msg = ''
#end def

def handle_USERNOTICE(s, data):
    channel = data['channel']
    
    key = data['tags']['msg-id']
    months = data['tags']['msg-param-cumulative-months']
    username = data['tags']['login']
    plan = data['tags']['msg-param-sub-plan']
    gift = data['tags']['msg-param-recipient-user-name'] if 'msg-param-recipient-user-name' in data['tags'] else None
    giftcount = data['tags']['msg-param-mass-gift-count'] if 'msg-param-mass-gift-count' in data['tags'] else None
    
    m = months % 12
    y = months // 12
    
    if channel == "#itshafu":
        if key == "submysterygift" and giftcount:
            if channels[channel].subbuffer > 0:
                s.msg(channel, "MetPride DanceBro BongoPenguin MetPride")
            channels[channel].subbuffer += giftcount
        
        elif key == "subgift":
            channels[channel].subcount += 1
            
            if channels[channel].subbuffer > 0:
                channels[channel].subbuffer -= 1
                if (channels[channel] == 0):
                    s.msg(channel, "MetPride DanceBro BongoPenguin MetPride")
            else:
                msg = get_hafuSubMessage(months,m,y)
                s.msg(channel,msg)
            #end if
        
        elif key == "sub" or key == "resub":
            channels[channel].subcount += 1
            
            msg = get_hafuSubMessage(months,m,y)
            s.msg(channel,msg)
        #end if
        
    elif channel == "#chewiemelodies":
        if key == "submysterygift" and giftcount:
            if channels[channel].subbuffer > 0:
                s.msg(channel, "HyperNeko HyperNeko HyperNeko HyperNeko")
            channels[channel].subbuffer += giftcount
        
        elif key == "subgift":
            channels[channel].subcount += 1
            
            if channels[channel].subbuffer > 0:
                channels[channel].subbuffer -= 1
                if channels[channel] == 0:
                    s.msg(channel, "HyperNeko HyperNeko HyperNeko HyperNeko")
            else:
                msg = ''
                if months > 1:
                    chews = (months * 1000) - 15000
                    s.msg("#chewiebot", "!add "+str(chews) + " gift")
                    if m == 0:
                        msg = "chewieRem " + "chewieLove "*y + "chewieXD"
                    else:
                        msg = "chewieLove "*y + "chewieHype "*m + "chewieHug"
                else:
                    msg = gift + " was gifted a sub! chewieHype Use these chews at an open raffle using !joinraffle chewieHi"
                s.msg(channel,msg)
            #end if
        
        elif key == "sub" or key == "resub":
            channels[channel].subount += 1
            
            if months > 1:
                if m == 0:
                    msg = "chewieRem " + "chewieLove "*y + "chewieXD"
                else:
                        msg = "chewieLove "*y + "chewieHype "*m + "chewieHug"
            else:
                if plan == 2000:
                    s.msg(channel, "!add 20000 "+username)
                elif plan == 3000:
                    s.msg(channel, "!add 40000 "+username)
                else:
                    s.msg(channel, "!add 15000 "+username)
                msg = "Thanks for subscribing! " + username + " chewieHype Use these chews at an open raffle using !joinraffle chewieHi"
                s.msg(channel,msg)
            #end if
        #end if
    #end if
    if username == NICK or gift == NICK:
        channels[channel].selfsub = True
#end def
