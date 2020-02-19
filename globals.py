HOST = "irc.twitch.tv"
PORT = 6667
NICK = ""
PASS = ""
CHAN = [""]

channel_info = {}
variables = {}
with open("variables.txt") as f:
    for line in f:
        (key, val) = line.split()
        variables[key] = val
    f.close()
#end open