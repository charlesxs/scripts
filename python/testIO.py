#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import os
import threading
import argparse
from time import time
from random import randint

class MyThread(threading.Thread):
    def __init__(self,func,args=(),name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name
    def run(self):
        self.__time = time()
        apply(self.func,self.args)
        print '%s Spend time: %s seconds' %(self.name,round(time() - self.__time,2))

def writer(startdir,enddir,fnum,basedir):
    for dir in range(startdir,enddir):
        fulldir = os.path.join(basedir,str(dir))
        if os.path.isdir(fulldir):
            # os.system('/bin/rm -rf %s' %fulldir)
            raise OSError,'Directory has not empty, thread exiting...'
        os.mkdir(fulldir)
        for file in range(fnum):
            fullfile = os.path.join(fulldir,str(file))
            rand = randint(1,1024)
            os.system('/bin/dd if=/dev/zero of=%s bs=1k count=%d conv=fdatasync 2>/dev/null' %(fullfile,rand))

def multi_mode(dlevel,core,fnum,basedir):
    threadlist = []
    if dlevel > core:
        for c in range(1,core+1):
            foundation,ends=divmod(dlevel,core)
            if c+1 == core+1:
                threadlist.append(MyThread(name='thread_%s' %c,func=writer,args=((c-1)*foundation,(c*foundation)+ends,fnum,basedir)))
            else:
                threadlist.append(MyThread(name='thread_%s' %c,func=writer,args=((c-1)*foundation,(c*foundation),fnum,basedir)))
    else:
        for d in range(1,dlevel+1):
            threadlist.append(MyThread(name='thread_%s' %d,func=writer,args=(d,d+1,fnum,basedir)))

    for thread in threadlist:
        thread.start()

def define_args(help=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',help='test directory.',metavar='dirname',type=str,default='/tmp')
    parser.add_argument('-dlevel',help='special the number of subdirs,in multi thread mode the best is cpu cores * 2',type=int,dest='dlevel',metavar='N')
    parser.add_argument('-fn','--filenumber',help='generate the number of files in each sub directory',type=int,metavar='N',dest='fn')
    parser.add_argument('-m',help='Multi threading',action='store_true',default=False)
    parser.add_argument('--core',help='Cpu cores',type=int,dest='core',metavar='N')
    args = parser.parse_args()
    if help:
        return  parser.parse_args(['-h'])
    else:
        return args

def main():
    args = define_args()
    try:
        if args.d and args.dlevel and args.fn and not args.m:
            stime = time()
            print 'Single Thread mode: Start test ...'
            writer(1,args.dlevel+1,args.fn,args.d)
            print 'Process spend time %s seconds' %(round(time() - stime,2))
        elif args.d and args.dlevel and args.fn and args.m and args.core:
            print 'Multi Thread mode: Start test ...'
            multi_mode(args.dlevel,args.core,args.fn,args.d)
        else:
            print define_args(True)
    except (AttributeError,TypeError,OSError),e:
        if __debug__:
            print 'Error:',e
            print 'Program exiting ...'
        else:
            print define_args(True)
    except KeyboardInterrupt:
        print 'Exiting ...'
        exit(3)

if __name__ == '__main__':
    main()
