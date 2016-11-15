#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

class foo(object):
	def __new__(cls,*args,**kwargs):
		if '_inst' not in cls.__dict__:
			cls._inst = object.__new__(cls,*args,**kwargs)
		print cls.__dict__
		return cls._inst



class C(foo):
	def __init__(self,name):
		self.name = name

class T1(object):
	def __new__(cls,*args,**kwargs):
		print 'This is new'
	def __init__(self):
		print 'This in init.'


if __name__ == '__main__':
	t1 = C('Carl')
	print id(t1),t1.__dict__
	t2 = C('Xiao')
	print id(t2),t2.__dict__
	
#	T1()
