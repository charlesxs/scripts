#coding=utf-8
#

class Demo:
	def __init__(self, name, gender):
		self.name = name
		self.gender = gender
	
	@classmethod
	def demo(cls, kwargs):
		if isinstance(kwargs, dict):
			name, gender = [(k, kwargs[k]) for k in kwargs ][0]
			return cls(name, gender)
		else:
			raise Exceptioin('Arugment error.')


if __name__ == '__main__':
	arg = {'Carl': 'Male'}
	a = Demo.demo(arg)
	print(a.name, a.gender)
