#!/usr/bin/env python

import sys
import socket
import string
import pronsole

HOST="ssh.ovx.cc"
PORT=42001
NICK="Pronterbot-RPi"
IDENT="Swarm"
PASS="mc5401"
REALNAME="Pronterbot"
CHAN="#SwarmLink"
readbuffer=""
LOUD=1
LOCALECHO=0
ADMIN=":Logxen!~Logxen@premiumus.xshellz.com"

sys.__stdout__.write("Attempting to connect to %s on channel %s as %s...\r\n"%(HOST, CHAN, NICK))
s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("PASS %s:%s\r\n" % (IDENT, PASS))
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send("JOIN %s\r\n" % CHAN)

class pronterbot:
#    def __init__(self):
    def write(self, msg):
        if(LOCALECHO):
            sys.__stdout__.write(msg)
        msg = msg.strip()
        if(len(msg) > 0):
            s.send("PRIVMSG %s :<%s> %s\r\n" % (CHAN, NICK, msg))

bot = pronterbot()
sys.stdout = bot
interp=pronsole.pronsole(None, None, bot)
interp.parse_cmdline(sys.argv[1:])

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        line=string.rstrip(line)
        if(LOUD):
            sys.__stdout__.write("%s\r\n"%line)
        line=string.split(line)

        if(line[0]=="PING"):
            message="PONG %s\r\n" % line[1]
            if(LOUD):
                sys.__stdout__.write(message)
            s.send(message)
        elif(line[1]=="JOIN" and line[2]==CHAN):
            sys.__stdout__.write("Connected.\r\n")
        elif(line[1]=="PRIVMSG"):
            sender = line[0]
            context = line[2]
            if(context==CHAN or context==NICK):
                address = line[3].strip(":").lower()
                if(address=="botsnack"):
                    sys.__stdout__.write("botsnack confirmed!\r\n")
                    s.send("PRIVMSG %s :<%s> %s\r\n" % (CHAN, NICK, ":)"))
                elif(address==NICK.lower()):
                    command = line[4]
                    args = string.join(line[5:])
                    if(sender==ADMIN):
                        if(command=="exit"):
                            interp.onecmd("exit")
                            s.send("QUIT :%s\r\n" % "Pronterbot 0.0.0 out. Peace.")
                            sys.exit("QUIT: Request from %s" % sender)
                        else:
                            sys.__stdout__.write("%s: %s %s\r\n" % (sender, command, args))
                            #s.send("PRIVMSG %s :%s %s\r\n" % (CHAN, command, args))
                            interp.onecmd("%s %s" % (command, args))
