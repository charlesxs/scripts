#!/usr/bin/env python3
# coding=utf-8
#

class Node:
	def __init__(self, key, value=None):
		self.key = key
		self.value = value
	
	def __eq__(self, other):
		return self.key == other.key
	

class Map:
	def __init__(self, init_size, hashfn=hash):
		self.__slot = [ [] for _ in range(init_size)]
		self.size = init_size
		self.hash = hash

	def put(self, key, value):
		node = Node(key, value)
		address = self.hash(key) % self.size
		self.__slot[address].append(node)

	def get(self, key, default=None):
		address = self.hash(key) % self.size
		for node in self.__slot[address]:
			if node.key == key:
				return node.value
			else:
				return default

	def remove(self, key):
		address = self.hash(key) % self.size
		try:
			return self.__slot[address].remove(Node(key))
		except ValueError:
			pass

if __name__ == '__main__':
	map = Map(16)

	#add map
	map.put('name', 'Carl')
	map.put('age', 23)
	map.put('gender', 'male')

	#remove map
	map.remove('age')

	#get map
	print('name', '-->', map.get('name'))
	print('age', '-->', map.get('age'))
	print('gebder', '-->', map.get('gender'))
	
