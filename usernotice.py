from globals import NICK, channels

def get_genericSubMessage(months,m,y):
    msg = ''
    if months > 1:
        if m==0:
            msg = ("bleedPurple " * y)
        else:
            msg = ("bleedPurple " * y) + ("<3 " * m)
    else:
        msg = "bleedPurple bleedPurple bleedPurple"
    return msg
#end def

def get_hafuSubMessage(months,m,y):
    msg = ''
    if months > 1:
        if m == 0:
            msg = "omgParty " + ("omgKirby " * y) + "omgParty"
        else:
            msg = ("omgKirby " * y) + ("omgHello " * m) + "omgHost"
    else:
        msg = "omgHello omgParty omgHost"
    return msg
#end def

def handle_USERNOTICE(s, data):
    channel = data['args'][0]
    
    key = data['tags'].get('msg-id')
    months = int(data['tags'].get('msg-param-cumulative-months',0))
    username = data['tags'].get('login')
    plan = data['tags'].get('msg-param-sub-plan')
    gift = data['tags'].get('msg-param-recipient-user-name')
    giftcount = int(data['tags'].get('msg-param-mass-gift-count',0))
    
    m = months % 12
    y = months // 12
    
    if channel == "#itshafu":
        if key == "submysterygift" and giftcount > 1:
            if channels[channel].subbuffer == 0:
                s.msg(channel, "MetPride DanceBro BongoPenguin MetPride")
            channels[channel].subbuffer += giftcount
        
        elif key == "subgift":
            channels[channel].subcount += 1
            
            if channels[channel].subbuffer > 0:
                channels[channel].subbuffer -= 1
                if (channels[channel].subbuffer == 0):
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
        if key == "submysterygift" and giftcount > 1:
            if channels[channel].subbuffer == 0:
                s.msg(channel, "HyperNeko HyperNeko HyperNeko HyperNeko")
            channels[channel].subbuffer += giftcount
        
        elif key == "subgift":
            channels[channel].subcount += 1
            
            if channels[channel].subbuffer > 0:
                channels[channel].subbuffer -= 1
                if channels[channel].subbuffer == 0:
                    s.msg(channel, "HyperNeko HyperNeko HyperNeko HyperNeko")
            else:
                msg = ''
                if months > 1:
                    chews = (months * 1000) - 15000
                    s.msg("#chewiebot", "!add "+str(chews) + " " + gift)
                    if m == 0:
                        msg = "chewieRem " + ("chewieLove " * y) + "chewieXD"
                    else:
                        msg = ("chewieLove " * y) + ("chewieHype " * m) + "chewieHug"
                else:
                    msg = gift + " was gifted a sub by " + username + "! chewieHype Use these chews at an open raffle using !joinraffle chewieHi"
                s.msg(channel,msg)
            #end if
        
        elif key == "sub" or key == "resub":
            channels[channel].subcount += 1
            
            msg = ''
            if months > 1:
                if m == 0:
                    msg = "chewieRem " + ("chewieLove " * y) + "chewieXD"
                else:
                    msg = ("chewieLove " * y) + ("chewieHype " * m) + "chewieHug"
            else:
                if plan == '2000':
                    s.msg(channel, "!add 20000 "+username)
                elif plan == '3000':
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
