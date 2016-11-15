#coding=utf-8
#

import time
import logging
import threading

logging.basicConfig(level=logging.INFO,
					format="%(asctime)s %(threadName)-10s [%(levelname)s]: %(message)s")

def producer(con, dlist):
	for i in range(10):
		dlist.append(i)
		logging.info('Product message %s' % i)
		time.sleep(0.5)
	with con:
		con.notify_all()
	
	
def consumer(e, dlist):
	while not e.is_set():
		if dlist:
			data = dlist.pop(0)
			logging.info('Consume message %s' % data)
			time.sleep(1)


def controll(con, e, dlist):
	with con:	
		con.wait()
		while True:
			if not dlist:
				e.set()
				break
			time.sleep(0.5)

	


if __name__ == '__main__':
	dlist = []
	event = threading.Event()
	condition = threading.Condition()
	
	pro = threading.Thread(target=producer, args=(condition, dlist), name='producer')
	pro.start()

	con1 = threading.Thread(target=consumer, args=(event, dlist), name='consumer1')
	con1.start()

	con2 = threading.Thread(target=consumer, args=(event, dlist), name='consumer2')
	con2.start()

	controller = threading.Thread(target=controll, args=(condition, event, dlist), name='controller')
	controller.daemon = True
	controller.start()

