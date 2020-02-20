HOST = "irc.twitch.tv"
PORT = 6667
NICK = ""
PASS = ""
CHAN = [""]

channels = {}
class Channel:
    hosttarget = None
    selfsub = False
    subbuffer = 0
    subcount = 0
    userlist = set()
#end class

variables = {}
with open("variables.txt") as f:
    for line in f:
        (key, val) = line.split()
        variables[key] = val
    f.close()
#end open