#!/usr/bin/env python3
# coding=utf-8
#

from MyStack import Stack
from queue import Queue
from functools import partial


class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Tree(object):
    def __init__(self, node):
        self.root = node

    def add_left(self, tree):
        self.root.left = tree

    def add_right(self, tree):
        self.root.right = tree

    @property
    def left(self):
        return self.root.left

    @property
    def right(self):
        return self.root.right

    def visit_first(self, fn):
        fn(self.root.value)
        if self.left:
            self.left.visit_first(fn)

        if self.right:
            self.right.visit_first(fn)

    def visit_first_norecur(self, fn):
        stack = Stack()
        stack.push(self)
        while stack.top:
            tree = stack.pop()
            fn(tree.root.value)
            if tree.right:
                stack.push(tree.right)
            if tree.left:
                stack.push(tree.left)

    def visit_middle(self, fn):
        if self.left:
            self.left.visit_middle(fn)
        fn(self.root.value)
        if self.right:
            self.right.visit_middle(fn)

    def visit_middle_norecur(self, fn):
        q = []
        q.append(self)

        while True:
            count = 0
            for key, tree in enumerate(q):
                tmpq = []
                if isinstance(tree, Tree):
                    count += 1
                    tree = q.pop(key)
                    tmpq.append(tree.root.value)
                    if tree.left:
                        tmpq.insert(0, tree.left)
                    if tree.right:
                        tmpq.append(tree.right)
                    tmpq.reverse()
                [q.insert(key, i) for i in tmpq]
            if count == 0:
                [fn(i) for i in q]
                break

    def visit_last(self, fn):
        if self.left:
            self.left.visit_last(fn)
        if self.right:
            self.right.visit_last(fn)
        fn(self.root.value)

    def visit_last_norecur(self, fn):
        stack1 = Stack()
        stack2 = Stack()
        stack1.push(self)
        while stack1.top:
            tree = stack1.pop()
            stack2.push(tree)
            if tree.left:
                stack1.push(tree.left)
            if tree.right:
                stack1.push(tree.right)

        while stack2.top:
            tree = stack2.pop()
            fn(tree.root.value)

    def visit_level(self, fn):
        q = Queue()
        q.put(self)
        while not q.empty():
            tree = q.get()
            fn(tree.root.value)
            if tree.left:
                q.put(tree.left)
            if tree.right:
                q.put(tree.right)


if __name__ == '__main__':
    # init tree
    a = Tree(Node('A'))
    b = Tree(Node('B'))
    c = Tree(Node('C'))
    d = Tree(Node('D'))
    e = Tree(Node('E'))
    f = Tree(Node('F'))
    g = Tree(Node('G'))

    # h = Tree(Node('H'))
    # i = Tree(Node('I'))
    # d.add_left(h)
    # d.add_right(i)

    c.add_left(f)
    c.add_right(g)
    b.add_left(d)
    b.add_right(e)
    a.add_left(b)
    a.add_right(c)

    fn = partial(print, end=" ")

    # 先序遍历, 结果: A, B, D, E, C, F, G
    print('先序遍历')
    a.visit_first(fn)
    print()
    a.visit_first_norecur(fn)
    print("\n")

    # 中序遍历, 结果: D, B, E, A, F, C, G
    print('中序遍历')
    a.visit_middle(fn)
    print()
    a.visit_middle_norecur(fn)
    print('\n')

    # 后序遍历, 结果: D, E, B, F, G, C, A
    print('后序遍历')
    a.visit_last(fn)
    print()
    a.visit_last_norecur(fn)
    print('\n')

    # 层序遍历: A, B, C, D, E, F, G
    print('层序遍历')
    a.visit_level(fn)
    print()
