#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from functools import wraps

## 1. The Decorator with no arguments.
def deco1(func):
	@wraps(func)
	def inner(*args, **kwargs):
		print('In inner.deco1')
		return func(*args, **kwargs)
	return inner
	
@deco1
def demo1(args):
	print(args)

## 2. The Decorator with arguments.
def deco2(UserList):
	def inner(func):
		@wraps(func)
		def _wrap(user, *args, **kwargs):
			if user in UserList:
				ret = func(user, *args, **kwargs)
			else:
				print('This user no permit.')
				return
			return ret
		return _wrap
	return inner

@deco2(['Carl', 'Xiao'])
def demo2(user):
	print('Welcome to Real World, %s.' % user)


## 3. The Class Decorator.
class deco3(object):
	def __init__(self, UserList):
		self.userList = UserList
	
	def __call__(self, func):
		@wraps(func)
		def inner(user, *args, **kwargs):
			if user in self.userList:
				ret = func(user, *args, **kwargs)
			else:
				print('This user no permit.')
				return
			return
		return inner
			
@deco3(['Carl', 'Xiao'])
def demo3(user):
	print('Welcom, %s' % user)

## 4. The Class Decoration Class.
class deco4(object):
	def __init__(self, cls):
		self.cls = cls
	def __call__(self, *args, **kwargs):
		print('deco4.__call__')
		return self.cls(*args, **kwargs)

@deco4
class demo4(object):
	def __init__(self, name):
		self.name = name

if __name__ == '__main__':
#	demo1('Carl')
#	demo2('Xiao')
#	demo3('Xiao')
	a = demo4('Xiao')
	print(a.name)
