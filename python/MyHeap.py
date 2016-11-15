#!/usr/bin/python3 
# coding=utf-8
#

from math import floor
from time import sleep

class Heap(object):
	def __init__(self):
		self.__data = []
	
	def myinsert(self, value):
		self.__data.append(value)
		index = len(self.__data) - 1
		if index <= 0: return
		while True:
			parent = floor((index - 1) / 2)
			if self.__data[parent] < value and parent >= 0:
				self.__data[index] = self.__data[parent]
				self.__data[parent] = value
				index = parent
			else:
				break
#		print('h Heap data: %s ' %self.__data)
	
	def insert(self, value):
		self.__data.append(value)
		idx = len(self.__data) - 1
		parent = floor((idx - 1) / 2)
		while parent >= 0 and self.__data[parent] < value:
			self.__data[idx] = self.__data[parent]
			self.__data[parent] = value
			idx = parent
			parent = floor((idx - 1) / 2)
#		print('b Heap data: %s' %self.__data)
	
	def mypop(self):
		if not self.__data:
			raise Exception("Empty")

		top = self.__data[0]
		self.__data[0] = self.__data.pop()
		index = 0

		while True:
			left = 2 * index + 1
			right = 2 * index + 2
			if len(self.__data) > left:
				tmpidx = left

			if len(self.__data) > right and self.__data[right] > self.__data[left]:
				tmpidx = right

			if self.__data[tmpidx] > self.__data[index]:
				self.__data[tmpidx], self.__data[index] = self.__data[index], self.__data[tmpidx]
				index = tmpidx 
			else:
				break
		print('h Heap data from mypop: %s' % self.__data)
		return top
	
	def pop(self):
		if not self.__data:
			raise Exception("Empty")
		ret = self.__data[0]
		value = self.__data.pop()
		self.__data[0] = value
		idx = 0
		left = 2 * idx + 1
		right = 2 * idx + 2
		while len(self.__data) > left:
			tmp_idx = left
			if len(self.__data) > right and self.__data[right] > self.__data[left]:
				tmp_idx = right
			if self.__data[tmp_idx] > value:
				self.__data[idx] = self.__data[tmp_idx]
				self.__data[tmp_idx] = value
			else:
				return ret
			idx = tmp_idx
			left = 2 * idx + 1
			right = 2 * idx + 2
		print('b Heap data from mypop: %s' % self.__data)
		return ret



if __name__ == '__main__':
	from random import randint
	h = Heap()
	b = Heap()

#	for i in range(10):
#		data = randint(5, 20)
#		h.myinsert(data) 
#		b.insert(data)
	h.myinsert(94)
	h.myinsert(54)
	h.myinsert(26)
	h.myinsert(66)
	h.myinsert(10)
	h.myinsert(13)
	h.myinsert(77)

	print(h._Heap__data)
#	h.mypop()
#	b.pop()
	h.mypop()
#	b.pop()


