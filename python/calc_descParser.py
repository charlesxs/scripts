# coding=utf-8
#
# Descent Parser(下降解析器): 实现算术表达式带优先级的解析. 
#     reference: python3 cookbook, chapter 2, 2.19
#

import re
from collections import namedtuple
# from functools import partial


# define expression pattern
LBRACKET = r'(?P<LBRACKET>\()'
RBRACKET = r'(?P<RBRACKET>\))'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
NUM = r'(?P<NUM>\d+)'
WS = r'(?P<WS>\s+)'

PATTERN = re.compile('|'.join([LBRACKET, RBRACKET, PLUS,
                               MINUS, TIMES, DIVIDE, NUM, WS]))

Token = namedtuple('Token', ['value', 'type'])

FunMap = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y
    }


def tokenize(expr):
    for s in expr:
        m = PATTERN.match(s)
        if not m:
            raise SyntaxError('generate token failed')
        token = Token(m.group(), m.lastgroup)
        if token.type != 'WS':
            yield token
    

class Tree:
    def __init__(self, root):
        self.root = root
        self.left = None
        self.right = None

    def middle_visit(self, fn):
        if self.left:
            self.left.middle_visit(fn)
        fn(self.root)
        if self.right:
            self.right.middle_visit(fn)

    def first_visit(self, fn):
        fn(self.root)
        if self.left:
            self.left.first_visit(fn)
        if self.right:
            self.right.first_visit(fn)


class DescParser:
    def __init__(self):
        self.token = None
        self.nexttoken = None
        self.tok = None

    def parse(self, expr):
        self.tok = tokenize(expr)
        self._advance()
        return self.expr()

    def _advance(self):
        self.token, self.nexttoken = self.nexttoken, next(self.tok, None)

    def _accept(self, tokentype):
        if self.nexttoken and self.nexttoken.type == tokentype:
            self._advance()
            return True
        return False

    def _expect(self, tokentype):
        if not self._accept(tokentype):
            raise SyntaxError('wrong expressions')

    def _make_tree(self, root, left=None, right=None):
        tree = Tree(root)
        tree.left = left
        tree.right = right
        return tree

    def expr(self):
        optree = None
        exprval = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            if optree is None:
                optree = self._make_tree(self.token.value, 
                                         exprval, self.term())
            else:
                optree = self._make_tree(self.token.value, 
                                        optree, self.term())
        if optree is not None:
            return optree
        return exprval

    def term(self):
        optree = None
        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            if optree is None:
                optree = self._make_tree(self.token.value,
                                         termval, self.factor())
            else:
                optree = self._make_tree(self.token.value,
                                         optree, self.factor())
        if optree is not None:
            return optree
        return termval

    def factor(self):
        if self._accept('NUM'):
            return Tree(int(self.token.value))
        elif self._accept('LBRACKET'):
            exprval = self.expr()
            self._expect('RBRACKET')
            return exprval
        else:
            raise SyntaxError('wrong expressions')


def calc(tree):
    if tree.left and tree.right:
        return FunMap[tree.root](calc(tree.left), calc(tree.right))
    return tree.root
    

if __name__ == '__main__':
   # expr = '2 + (3 + 4) * 5'
   # expr = '(3+4) * 5 / ((2+3) *3)'
    expr = '(3 + 4) + 5  / ((2+3) * 3) * 3'
    # alist, blist = list(), list()
    
    parser = DescParser()
    retree = parser.parse(expr)
    # ret.middle_visit(alist.append)
    # ret.first_visit(blist.append)
    # print(alist, blist)
    print(calc(retree))

