#!/usr/bin/env python3
# coding=utf-8
#

class Node(object):
	def __init__(self, value):
		self.value = value
		self.pointer = None


class Stack(object):
	def __init__(self):
		self.top = None
	
	def push(self, data):
		node = Node(data)
		node.pointer = self.top
		self.top = node
	
	def pop(self):
		data = self.top.value
		self.top = self.top.pointer
		return data

if __name__ == '__main__':
	def test():
		stack = Stack()
		for i in range(10):
			print('pushing data %s in stack.' % i )
			stack.push(i)
		print('push over ... \n')
	
		while stack.top:
			data = stack.pop()
			print('poping data %s from stack.' % data)
		print('pop over ...')

	test()

