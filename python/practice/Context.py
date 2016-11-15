#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from contextlib import contextmanager
import time

## 1. Context Class for with statement.
class demo1(object):
	def __init__(self, user_list):
		self.userlist = user_list
	
	def __enter__(self):
		print('Entering in demo1.__enter__')
		return self
	
	def __exit__(self, exp_type, exp_value, exp_traceback):
		print('Entering in demo1.__exit__')
	
	def view_user(self):
		return self.userlist

with demo1(['Xiao', 'Carl']) as dobj:
	print(dobj.view_user())
	

## 2. Context Class 
class demo2(object):
	def __init__(self, label):
		self.label = label
	
	def __enter__(self):
		self.start = time.time()
	
	def __exit__(self, *args, **kwargs):
		end = time.time()
		print('%s: %s' %(self.label, end - self.start))

	
with demo2('Counting'):
	time.sleep(2)


## 3. Use contextlib
@contextmanager
def demo3(label):
	try:
		start = time.time()
		yield
	finally:
		end = time.time()
		print('%s: %s' %(label, end - start))

with demo3('Counting'):
	time.sleep(2)
