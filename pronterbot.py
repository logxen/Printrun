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
            print("PONG %s\r\n" % line[1])
            s.send("PONG %s\r\n" % line[1])
        if(line[1]=="PRIVMSG"):
            if(line[2]==CHAN or line[2]==NICK):
                if(line[3]==":botsnack"):
                    print("botsnack confirmed!")
                    s.send("PRIVMSG %s :%s\r\n" % (CHAN, ":)"))
                if(line[3]==":%s:" % NICK):
                    if(line[0]==ADMIN):
                        if(line[4]=="quit"):
                            s.send("QUIT :%s\r\n" % "Pronterbot 0.0.0 Out. Peace.")
                            sys.exit("QUIT: Request from %s" % line[0])
                        if(line[4]=="send"):
                            print("sending command: %s" % string.join(line[5:]))
                            s.send("PRIVMSG %s :%s\r\n" % (CHAN, string.join(line[5:])))
                            interp.onecmd(string.join(line[5:]))
