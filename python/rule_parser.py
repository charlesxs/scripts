#!/usr/bin/env python3
# coding=utf-8
#

# (#abc# & #324#) | (!#def# & #789#)
from stack import Stack
import re

def Matcher(exprs, line, fn):
	stack = Stack()
	is_expr = False
	expr = []
	for c in exprs:
		if c in '(&|!':
			stack.push(c)
		elif c.strip() == '':
			pass
		elif c == ')':
			v = stack.pop()
			if not isinstance(v, bool):
				raise Exception('Wrong expr')
			if stack.top.value == '(':
				stack.pop()
				stack.push(v)
			else:
				raise Exception('Wrong expr')
		else:
			if c == '#':
				if not is_expr:
					is_expr = True
				else:
					is_expr = False
					v = fn(line, ''.join(expr))
					expr = []
					if not stack.top:
						stack.push(v)
						continue
					s = stack.pop()
					if s == '!':
						v = not v
						stack.push(v)
					elif s == '&':
						if isinstance(stack.top.value, bool):
							v = stack.pop() and v
							stack.push(v)
						else:
							raise Exception('Wrong expr')
					elif s == '|':
						if isinstance(stack.top.value, bool):
							v = stack.pop() or v
							stack.push(v)
						else:
							raise Exception('Wrong expr')
					else:
						stack.push(s)
						stack.push(v)
			else:
				if is_expr:
					expr.append(c)
	
	while stack.top:
		v = stack.pop()
		if not isinstance(v, bool):
			raise Exception('Wrong expr')
		try:
			s = stack.pop()
		except AttributeError:
			return v

		if s == '!':
			v = not v
			stack.push(v)
		elif s == '&':
			if isinstance(stack.top.value, bool):
				v = stack.pop() and v
				stack.push(v)
			else:
				raise Exception('Wrong expr')
		elif s == '|':
			if isinstance(stack.top.value, bool):
				v = stack.pop() or v
				stack.push(v)
			else:
				raise Exception('Wrong expr')
		else:
			raise Exception('Wrong expr')


def fn(line, expr):
	return re.match(expr, line) is not None

if __name__ == '__main__':
	line = 'abc 123  def 456 asd 789'
	exprs = '(#abc# & #324# & #aaa#) | (!#def# & #789#)'
#	exprs = '#abc# & !#324#'
	print(Matcher(exprs, line, fn))

