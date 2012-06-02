#!/usr/bin/env python

import sys
import socket
import string
import time
import pronsole

HOST="irc.freenode.net"
PORT=6667
NICK="Pronterbot"
IDENT="Pronterbot"
REALNAME="Pronterbot"
CHAN="#SwarmLink"
readbuffer=""
LOUD=1
ADMIN=":Logxen!~Logxen@74.63.228.143"

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send("JOIN %s\r\n" % CHAN)

interp=pronsole.pronsole()
interp.parse_cmdline(sys.argv[1:])

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        line=string.rstrip(line)
        if(LOUD==1):
            print(line)
        line=string.split(line)

        if(line[0]=="PING"):
            message="PONG %s\r\n" % line[1]
            print(message)
            s.send(message)
        if(line[1]=="PRIVMSG"):
            sender = line[0]
            context = line[2]
            if(context==CHAN or context==NICK):
                address = line[3].strip(":").lower()
                if(address=="botsnack"):
                    print("botsnack confirmed!")
                    s.send("PRIVMSG %s :%s\r\n" % (CHAN, ":)"))
                if(address==NICK.lower()):
                    if(sender==ADMIN):
                        command = line[4]
                        args = string.join(line[5:])
                        if(command=="quit"):
                            s.send("QUIT :%s\r\n" % "Pronterbot 0.0.0 Out. Peace.")
                            interp.onecmd("exit")
                            sys.exit("QUIT: Request from %s" % sender)
                        if(command=="send"):
                            print("SEND: '%s' from %s" % (args, sender))
                            s.send("PRIVMSG %s :%s\r\n" % (CHAN, args))
                            interp.onecmd(args)
