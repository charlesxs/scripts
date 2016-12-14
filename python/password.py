# coding=utf-8
# use in unix

import os
import tty
import sys
import termios
import select
import fcntl
import readline


class Password:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_tty = termios.tcgetattr(self.fd)
    
    def unixstyle_password(self, prompt):
        fd = sys.stdin.fileno()

        # get old tty attribute
        new = termios.tcgetattr(fd)
        # set new tty attribute(no display)
        new[3] = new[3] & ~termios.ECHO
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, new)
            passwd = raw_input(prompt)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, self.old_tty)
        return passwd

    @staticmethod
    def _out(s):
        sys.stdout.write(s)
        sys.stdout.flush()

    def winstyle_password(self, prompt):
        #tty.setraw(self.fd)
        tty.setcbreak(self.fd)
        
        # set nonblock for sys.stdin
        flag = fcntl.fcntl(sys.stdin, fcntl.F_GETFL, 0)
        fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, flag|os.O_NONBLOCK)
        try:
            self._out(prompt)
            pwd = ''
            while True:
                select.select([sys.stdin], [], [])
                data = sys.stdin.read(1024)
                if not data or data in ['\n', '\r\n']:
                    break

                if data in ['\x08', '\b']:
                    if pwd:
                        self._out(data + ' ' + data)
                    pwd = pwd[:-1]
                else:
                    pwd += data
                    self._out('*')
        finally:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_tty)
        return pwd


if __name__ == '__main__':
    pwd = Password()
    p = pwd.winstyle_password('Enter password: ')
    print('\n' + p)

    p2 = pwd.unixstyle_password('Enter password: ')
    print('\n' + p2)
