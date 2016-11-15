#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import weakref

class MyProperty(object):
	def __init__(self, fget=None, fset=None, fdel=None):
		self.fget = fget
		self.fset = fset
		self.fdel = fdel
		self.ins = weakref.WeakKeyDictionary()
	
	def __get__(self, instance, cls):
		if self.fget and instance:
			self.ins[instance] = self.fget(instance)
			return self.ins[instance]
		return instance
	
	def __set__(self, instance, value):
		if instance in self.ins:
			self.ins[instance] = self.fset(instance, value)
	
	def __delete__(self, instance):
		if self.fdel:
			self.fdel(instance)
	
	def getter(self, fn):
		self.fget = fn
	
	def setter(self, fn):
		print(fn, self)
		name = fn
		self.fset = name
	
	def deleter(self, fn):
		self.fdel = fn


class demo(object):
	def __init__(self, val):
		self.__val = val
	
	@MyProperty
	def val(self):
		return self.__val
	
	@val.setter
	def v(self, value):
		if value >= 0:
			self.__val = value
		else:
			raise ValueError('Expect the value is greater than 0.')

if __name__ == '__main__':
	a = demo(10)

	print a.val
	a.val = -1
	print a.val

