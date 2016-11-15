#!/usr/bin/env python3
#coding=utf-8
#

#单实例, 使用 __new__ 方法
#class Single(object):
#	def __new__(cls, *args, **kwargs):
#		try:
#			ins = getattr(cls, '__ins')
#		except AttributeError:
#			ins = object.__new__(cls)
#			setattr(cls, '__ins', ins)
#		return ins
		
#		if '_inst' not in vars(cls):
#			cls._inst = super(Single, cls).__new__(cls, *args, **kwargs)
#		return cls._inst
	


#使用类装饰器 跟上面的有区别，上面的依然会执行 __init__方法
class Single:
	__instance = None

	def __init__(self, cls):
		self.cls = cls
	
	def __call__(self, *args, **kwargs):
		if not self.__instance:
			self.__instance = self.cls(*args, **kwargs)
		return self.__instance


@Single
#class Grok(Single):
class Grok:
	def __init__(self, name):
		self.name = name


if __name__ == '__main__':
	a = Grok('Carl')
	print(id(a), a.name)

	b = Grok('Xiao')
	print(id(b), b.name)
	print(id(a), a.name)
