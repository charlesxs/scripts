# coding=utf-8
#

import threading
import Queue
import time
import logging 

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(threadName)s [%(levelname)s] %(message)s')


class Demo:
    def __init__(self, queue, filename):
        self.queue = queue
        self.fd = open(filename, 'a')
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.product = False
    
    def consumer(self):
        while not self.event.is_set():
            with self.lock:
                try:
                    data = self.queue.get_nowait()
                    logging.debug('consume data: ' + data.strip())
                    self.fd.write(data)
                except Queue.Empty:
                    logging.warn('no data')
            self.event.wait(0.5)
    
    def producer(self):
        for i in range(30):
            data = 'data{0}\n'.format(str(i))
            self.queue.put(data)
            logging.debug('product data: ' + data.strip())
            time.sleep(0.2)
        self.product = True

    def controller(self):
        try:
            while True:
                if not self.product:
                    continue
                if self.queue.empty():
                    self.event.set()
                    break
                time.sleep(0.3)
        finally:
            self.fd.close()


if __name__ == '__main__':
    queue = Queue.Queue()
    demo = Demo(queue, './data')

    threading.Thread(target=demo.controller, name='controller').start()
    threading.Thread(target=demo.producer, name='producer').start()
    for i in range(4):
        threading.Thread(target=demo.consumer, name='consumer-{0}'.format(str(i))).start()

