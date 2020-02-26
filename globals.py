import urllib.request, json

HOST = "irc.twitch.tv"
PORT = 6667
NICK = ""
PASS = ""
CHAN = [""]

channels = {}
class Channel:
    
    def __init__(self, chan):
        self.channel = chan
        self.hosttarget = None
        self.selfsub = False
        self.subbuffer = 0
        self.subcount = 0
        self.timer = None
    #end __init__
    
    #Groups: "broadcaster", "vips", "moderators", "staff", "admins, "global_mods", "viewers"
    def get_userlist(self):
        userlist = {}
        with urllib.request.urlopen('https://tmi.twitch.tv/group/user/'+self.channel[1:]+'/chatters') as url:
                json_data = json.loads(url.read().decode())
                for group in json_data['chatters']:
                    userlist[group] = []
                    for chatter in json_data['chatters'][group]:
                        userlist[group].append(chatter)
                #end for
            #end url
        return userlist
    #end def
#end class

variables = {}
with open("variables.txt") as f:
    for line in f:
        (key, val) = line.split()
        variables[key] = val
    f.close()
#end open