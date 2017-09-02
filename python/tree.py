# coding=utf-8
#

from functools import partial


class SStack:
    def __init__(self):
        self._elems = []

    def is_empty(self):
        return self._elems == []

    def top(self):
        if len(self._elems) < 1:
            raise Exception('in SStack.top()')
        return self._elems[-1]

    def push(self, elem):
        self._elems.append(elem)

    def pop(self):
        if len(self._elems) < 1:
            raise Exception('in SStack.pop()')
        return self._elems.pop()


class Tree:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def post_visit(self, proc):
        if self.left is not None:
            self.left.post_visit(proc)

        if self.right is not None:
            self.right.post_visit(proc)

        proc(self.data)


def postorder_nonrec(t, proc):
    s = SStack()
    while t is not None or not s.is_empty():
        while t is not None:
            s.push(t)
            t = t.left if t.left is not None else t.right

        t = s.pop()
        proc(t.data)
        if not s.is_empty() and s.top().left == t:
            t = s.top().right
        else:
            t = None


if __name__ == '__main__':
    t1 = Tree('-', Tree('a'), Tree('b'))
    t2 = Tree('/', Tree('c'), Tree('d'))
    t3 = Tree('+', t2, Tree('e'))
    t = Tree('x', t1, t3)

    fn = partial(print, end=" ")
    t.post_visit(fn)
    print()
    postorder_nonrec(t, fn)




