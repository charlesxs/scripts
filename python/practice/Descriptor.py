#coding=utf-8
#

#控制类属性, 限制实例访问类属性.

class Demo:
	def demo(self):
		return 'Demo.demo'


class Descriptor:
	def __init__(self):
		self.demo = Demo()
	
	def __get__(self, instance, cls):
		if isinstance(instance, cls):
			raise AttributeError('Demo is not accessible via Foo instance.')
		return self.demo
	
	def __set__(self, instance, value):
		raise AttributeError('Demo is not overwrite.')
	

class Foo:
	objects = Descriptor()

	def __init__(self):
		pass


if __name__ == '__main__':
	print(Foo.objects.demo())
	print()

	f = Foo()
	print(f.objects.demo())
