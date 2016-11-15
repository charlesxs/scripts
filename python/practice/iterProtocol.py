#coding=utf-8
#

class Demo:
	def __init__(self, v1, v2, v3):
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3
		self.__vars = locals()
		self.__vars.pop('self')
		self.__values = list(self.__vars.values())
	
	def __iter__(self):
		return self
	
	def __next__(self):
		if not self.__values:
			raise StopIteration
		else:
			return self.__values.pop()

#	def next(self):
#		if not self.__values:
#			raise StopIteration
#		else:
#			return self.__values.pop()


if __name__ == '__main__':
	a = Demo(1, 2, 3)
	b = iter(a)
	for i in b:
		print(i)
