#!/usr/bin/env python3
# coding=utf-8
#

class Node(object):
	def __init__(self, data):
		self.data = data
		self.next = None

class Queue(object):
	def __init__(self, maxlen=None):
		self.head = None
		self.tail = None
		self.maxlen = maxlen
	
	def put(self, data):
		node = Node(data)
		if self.head is None:
			self.head = node
			self.tail = node
		else:
			cursor = self.head
			counter = 1
			while cursor:
				if counter == self.maxlen:
					raise Exception('Full')
				cursor = cursor.next
				counter += 1
			self.tail.next = node
			self.tail = node
	
	def get(self):
		if self.head is None:
			return

		data = self.head.data
		self.head = self.head.next
		return data
	
	@property
	def full(self):
		cursor = self.head
		if cursor is not None:
			counter = 1
			while cursor:
				if counter == self.maxlen:
					return True
				cursor = cursor.next
				counter += 1
		return False
	
	@full.setter
	def full(self, value):
		raise Exception('Read only.')
	
	@property
	def empty(self):
		if self.head is None:
			return True
		return False
	
	@empty.setter
	def empty(self, value):
		raise Exception('Read only.')


if __name__ == '__main__':
	def test():
		q = Queue(10)
		# 
		print(q.empty, q.full)

		#
		for i in range(11):
			q.put(i)
			print('putting data %s in queue.' %i)

		#
		print(q.empty, q.full)

		# 
		while not q.empty:
			data = q.get()
			print('getting data %s from queue.' %data)

	test()
