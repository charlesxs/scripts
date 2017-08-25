#!/usr/bin/env python
# coding=utf-8
#

import threading
import subprocess
import multiprocessing
import logging
import urllib2
import urllib
from time import asctime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(threadName)s [%(levelname)s]  %(message)s')

# 微信报警账户名
ADMINS = ('xxxx', )

# port 白名单
SAFE_PORTS = ('80', '8080', '443')

# IP 白名单(在白名单里的不扫描)
WHITE_IP = ('1.1.1.1',
            '2.2.2.2'
            )


class PortScan(object):
    def __init__(self, ip_list, size=10):
        self.ip_list = ip_list
        self.size = size

    @staticmethod
    def data_filter(data):
        data_list = data.split('\n')
        data_list.pop()
        return [d.split()[3] for d in data_list]

    def _scan(self, ip, start_port, stop_port):
        child = subprocess.Popen(['/usr/bin/nc', '-zv', '-w', '1', ip, '{0}-{1}'.format(start_port, stop_port)],
                                 stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        info = child.communicate()
        res = self.data_filter(info[0].decode())
        ScanHandler.alarm_filter(ip, res)

    def scan(self, ip):
        threads = []
        print('[{0}] {1} start scan {2}'.format(asctime(), multiprocessing.current_process().name, ip))
        for i in range(1, 101):
            t = threading.Thread(target=self._scan, args=(
                ip, (i - 1) * 200 + 1, i * 200
            ))
            t.start()
            threads.append(t)
        [t.join() for t in threads]
        print('[{0}] {1} scan over {2}'.format(asctime(), multiprocessing.current_process().name, ip))

    def start(self):
        num, processes = 0, []
        while self.ip_list:
            if num >= self.size:
                [p.join() for p in processes]
                num, processes = 0, []
                continue

            ip, num = self.ip_list.pop(), num + 1
            p = multiprocessing.Process(target=self.scan, args=(ip, ))
            p.start()
            processes.append(p)


class ScanHandler(object):
    WECHAT = 'http://sms.xxx.com/weixin.php?%s'

    @staticmethod
    def alarm(message):
        for admin in ADMINS:
            data = {
                'user': admin,
                'info': message,
            }
            data = urllib.urlencode(data)
            urllib2.urlopen(ScanHandler.WECHAT % data)

    @classmethod
    def alarm_filter(cls, ip, data):
        for p in data:
            if p in SAFE_PORTS:
                continue
            message = 'Host %s is in danger, unsafe port %s is opening' % (ip, p)
            logging.info(message)
            ScanHandler.alarm(message)


class GetIPList(object):
    ip_range = {
        "9.151.73": (2, 30),
        "9.151.119": (130, 142),
        "2.151.172": (98, 126)
    }

    def __init__(self):
        self.semaphore = threading.BoundedSemaphore(30)

    @staticmethod
    def probe_addr(sema, ip, ip_list):
        with sema:
            res = subprocess.Popen('ping -c 1 -w 3 %s' % ip, shell=True,
                                   stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
            data = res.communicate()
            if data[1]:
                logging.error('ping error, %s' % ip)
                return False
            ip_list.append(ip)

    def get_addr(self):
        ip_list, threads = [], []
        for prefix, length in GetIPList.ip_range.items():
            start, stop = length
            for i in range(start, stop+1):
                ip = '.'.join([prefix, str(i)])
                if ip not in WHITE_IP:
                    t = threading.Thread(target=self.probe_addr, args=(self.semaphore, ip, ip_list),
                                         name="checkaddr-{0}".format(ip))
                    threads.append(t)
                    t.start()

        [t.join() for t in threads]
        return ip_list


if __name__ == '__main__':
    addrs = GetIPList().get_addr()
    print("%s\n%s" % (addrs, len(addrs)))
    scanner = PortScan(addrs, 10)
    scanner.start()
