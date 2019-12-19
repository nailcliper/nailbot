#data['tags']:
#badge-Info:    Metadata related to the chat badges in the 'badges' tag.
#               Currently only used for 'subscriber' to indicate the exact number of months the user has been a subscriber

#badges:        Comma separated list of chat badges and the version of each badge in the format <badge>/<version>
#               Common badges: admin, bits, broadcaster, global_mod, moderator, subscriber, staff, turbo

#bits:          The amount of bits employed by the user.
#               All instances of these regular expressions /(^\|\s)<emote-name>\d+(\s\|$)/ 

#color:         Hexadecimal RGB color code; the empty string if never set

#display-name:  The user's display name, escaped and described in IRCv3 spec. This is empty if never set.

#eomtes:        Information to replace text in the message with emote images

#id:            A unique ID for the message

#mod:           1 if the user has a moderator badge, otherise 0

#room-id:       The channel ID

#subscriber:    (Depriciated, use 'badges' instead) 1 if the user has a subscriber badge, otherwise 0

#tmi-send-st:   Timestamp when the server received the message

#turbo:         (Depriciated, use 'badges' instead) 1 if the user has a subscriber badge, otherwise 0

#user-id:       The user's ID

#user-type:     (Depriciated, use 'badges' insteadd) The user's type
#               Valid values: mod, global_mod, admin, staff. If the broadcaster is not any of these types, the field is empty

#data['message']: The message

from twitch_socket import s
from firebaseAuth import fb

db = fb.database()

def handle_PRIVMSG(data):
    in_message = data['message'].split(' ')
    if in_message[0] == "!chews":
        username = data['tags']['display-name']
        channel = data['args'][0][1:]
        fb_user = db.child(channel).child('users').child(username).get()
        if(fb_user.val()):
            points = fb_user.val()['points']
            hours = fb_user.val()['hours']
            minutes = fb_user.val()['minutes']
            out_message = "/me Chews: [" + str(hours) + ":" + str(minutes) + "] - " + str(points)
            s.send_msg(out_message, channel)
    pass
#end def
