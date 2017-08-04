#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#

#打破单实例限制，允许多个实例，但是多个实例共享状态和行为方式.

class Borg(object):
	_shared_state = {}
	def __new__(cls,*args,**kwargs):
		obj = object.__new__(cls,*args,**kwargs)
		obj.__dict__ = cls._shared_state
		return obj


if __name__ == '__main__':
	class Example(Borg):
		name = None
		def __init__(self,name=None):
			if name is not None: self.name = name
		def __str__(self): return 'name --> %s' %self.name

	a = Example('Lara')
	b = Example()
	print a,b

	c = Example('Seven')
	print a,b,c
	print id(a),id(b),id(c)
