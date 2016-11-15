#!/usr/bin/env python3
# coding=utf-8
#

class Node(object):
	def __init__(self, data):
		self.data = data
		self.next = None
	
class MyList(object):
	def __init__(self):
		self.head = None
		self.tail = None
	
	def __len__(self):
		cursor = self.head
		length = 1
		if not self.head:
			return None
		while cursor.next:
			cursor = cursor.next
			length += 1
		return length

	def append(self, data):
		node = Node(data)
		if not self.head:
			self.head = node
			self.tail = node
		else:
			self.tail.next = node
			self.tail = node
	
	def iter(self):
		if not self.head:
			return
		cursor = self.head
		yield cursor.data
		while cursor.next:
			cursor = cursor.next
			yield cursor.data
	
	def insert(self, index, value):
		cursor = self.head
		CurrentIndex = 0

		if not cursor:
			raise Exception('It is a empty list.')

		while CurrentIndex < index - 1:
			cursor = cursor.next
			if not cursor:
				raise Exception('Index is too large.')
			CurrentIndex += 1
		
		node = Node(value)
		node.next = corsor.next
		cursor.next = node
		if node.next is None:
			self.tail = node
	
	def remove(self, value):
		cursor = self.head
		if cursor.data == value:
			self.head = None
			self.tail = None
		elif not cursor:
			raise Exception('It is a empty list.')

		while cursor.next:
			if not cursor.next:
				raise Exception('Not found this value.')
			if cursor.next.data == value:
				cursor.next = cursor.next.next
			else:
				cursor = cursor.next

		if cursor.next is None:
			self.tail = cursor

	def pop(self, index=None):
		cursor = self.head
		curidx = 0
		if not cursor:
			raise Exception('It is a empty list.')

		if index is None:
			idx = len(self) - 1
		else:
			idx = index

		if idx == 0:
			data = self.head.data
			self.head = cursor.next
			return data
		
		while cursor.next:
			if curidx + 1 == idx:
				data = cursor.data
				cursor.next = cursor.next.next
				break
			cursor = cursor.next
			curidx += 1

		if not cursor.next:
			self.tail = cursor
		return data
	
	def extend(self, iteration):
		cursor = self.tail
		if not cursor:
			raise Exception('It is a empty list.')

		for i in iteration:
			node = Node(i)
			cursor.next = node
			cursor, self.tail = cursor.next, cursor.next

				

if __name__ == '__main__':
	linkList = MyList()
	# append
	for i in range(10):
		linkList.append(i)
		print('append %s in linkList.' % i)
	print()

	# remove
#	print("remove value from list")
#	linkList.remove(3)

	# count length
	print("List Lenght: %s" % len(linkList))

    # pop operation
	print("POP operation\n")
	linkList.pop()

	# extend operation
	print('extend opration.')
	linkList.extend(['a', 'b'])

	# see
	for i in linkList.iter():
		print(i, end=" ")
	print()

