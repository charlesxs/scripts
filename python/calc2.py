#!/usr/bin/env python
# coding=utf-8
#

from __future__ import division
from stack import Stack

func_map = {
	'+': lambda x,y: x + y,
	'*': lambda x,y: x * y,
	'-': lambda x,y: x - y,
	'/': lambda x,y: x / y,
}


def calc(expr):
	stack = Stack()
	for c in expr:
		if c in '(+-*/':
			stack.push(c)
		elif c.strip() == '':
			continue
		else:
			if c != ')':
				c = int(c)
				if stack.top.value != '(':
					e = stack.pop()
					if not isinstance(stack.top.value, int):
						raise Exception('wrong expr.')
					v = func_map[e](stack.pop(), c)
					stack.push(v)
				else:
					stack.push(c)
			elif c == ')':
				if not isinstance(stack.top.value, int):
					raise Exception('wrong expr.')
				v = stack.pop()
				if stack.top.value != '(':
					raise Exception('wrong expr.')
				stack.pop()
				stack.push(v)
				
	while stack.top:
		if str(stack.top.value) in '+-/*':
			e = stack.pop()
			if not isinstance(stack.top.value, (int, float)):
				raise Exception('wrong expr')
			tmp = stack.pop()
			print("formula: %s %s %s" %(tmp,e, v))
			v = func_map[e](tmp, v)
			#print("after division: %s" %v)
			stack.push(v)
		else:
			v = stack.pop()
	return v


if __name__ == '__main__':
	#expr = '(2 + 3) / 5 / ((3+4) - 2)'
	#expr = '(3 + 4) * 5  / ((2+3) * 3) * 3'
	expr = '(3+4) * 5 / ((2+3) *3)'
	print(calc(expr))
	
