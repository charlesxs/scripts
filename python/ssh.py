# coding=utf-8
#

import paramiko
import select
import os
import sys
import fcntl
import readline
import tty
import termios


ssh = paramiko.client.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname='172.16.8.250',
           port=22,
           username='root',
           password='123')

channel = ssh.invoke_shell(term='xterm', width=100, height=100)
channel.settimeout(0.0)


# save old tty and set new tty
old_tty = termios.tcgetattr(sys.stdin.fileno())
tty.setraw(sys.stdin.fileno())
#tty.setcbreak(sys.stdin.fileno())

# set sys.stdin nonblock
flag = fcntl.fcntl(sys.stdin, fcntl.F_GETFL, 0)
fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, flag|os.O_NONBLOCK)
try:
    while True:
        r, w, e = select.select([sys.stdin, channel], [], [])

        if channel in r:
            data = channel.recv(10240)
            if not data:
                break
            #print('server: ' + data,)
            sys.stdout.write(data)
            sys.stdout.flush()

        if sys.stdin in r:
            data = sys.stdin.read(10240)
            if not data:
                break
            channel.send(data)
finally:
   termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_tty) 
