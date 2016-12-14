#!/usr/bin/env python3
# coding=utf-8
#

from __future__ import division
#from functools import partial

import time

func_map = {
	'+': lambda x,y: x + y,
	'-': lambda x,y: x - y,
	'*': lambda x,y: x * y,
	'/': lambda x,y: x / y,
}


class Token(object):
	LEFT_BRACKET = 'LEFT_BRACKET'
	RIGHT_BRACKET = 'RIGHT_BRACKET'
	MATH_SYMBOL = 'MATH_SYMBOL'
	DIGITAL = 'DIGITAL'
	MATH_SYMBOLS = '+-*/'
	
	def __init__(self, value, type):
		self.value = value
		self.type = type
	
	def __str__(self):
		return '%s<%s>' % (self.value, self.type)
	
	__repr__ = __str__


class Tree(object):
	def __init__(self, node):
		self.root = node
		self.right = None
		self.left = None
	
	def _middle_visit(self, fn):
		if self.left:
			self.left._middle_visit(fn)

		fn(self.root.value)

		if self.right:
			self.right._middle_visit(fn)
	
	def middle_visit(self):
		lst = []	
		self._middle_visit(lst.append)
		return lst


def tokenize(expr):
	exprs = []
	for c in expr:
		if c == '(':
			token = Token(c, Token.LEFT_BRACKET)
		elif c.strip() == '':
			continue	
		elif c in Token.MATH_SYMBOLS:
			token = Token(c, Token.MATH_SYMBOL)
		elif c == ')':
			token = Token(c, Token.RIGHT_BRACKET)
		else:
			token = Token(int(c), Token.DIGITAL)
		exprs.append(token)
	
	return exprs


def make_sub_tree(token, stack):
	if isinstance(token, Tree):
		current = token
	else:
		current = Tree(token)
	
	while stack and stack[-1].root.type != Token.LEFT_BRACKET:
		tree = stack.pop()
		if tree.root.type != Token.MATH_SYMBOL:
			raise Exception('wrong expr, expect math symbol, but %s' % tree.root.value)

		left = stack.pop()
		if left.root.type != Token.MATH_SYMBOL and left.root.type != Token.DIGITAL:
			raise Exception('wrong expr, expect math symbol or digital but %s' %tree.root.value)
		tree.left = left

		tree.right = current
		current = tree
	stack.append(current)
			 

def make_tree(exprs):
	stack = []
	for t in exprs:
		if t.type == Token.LEFT_BRACKET or t.type == Token.MATH_SYMBOL:
			stack.append(Tree(t))
		elif t.type == Token.DIGITAL:
			make_sub_tree(t, stack)
		elif t.type == Token.RIGHT_BRACKET:
			tree = stack.pop()
			if tree.root.type == Token.LEFT_BRACKET:
				raise Exception('parse error.')
			left_bracket = stack.pop()
			if left_bracket.root.type != Token.LEFT_BRACKET:
				raise Exception('parse error.')
			make_sub_tree(tree, stack)
	return stack.pop()


def calc(tree):
	if tree.left and tree.right:
		return func_map[tree.root.value](calc(tree.left),calc(tree.right))
	else:
		return tree.root.value

	
if __name__ == '__main__':
	#expr = '(2 + 3) / 5 / ((3+4) - 2)'
	#expr = '(3 + 4) * 5  / ((2+3) * 3) * 3'
	expr = '(3+4) * 5 / ((2+3) *3)'

	tree = make_tree(tokenize(expr))
	#tree.middle_visit(partial(print, end=" "))
	print(tree.middle_visit())
	print(calc(tree))

