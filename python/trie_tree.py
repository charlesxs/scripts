# coding=utf-8
#

import os
import sys
import time

class Node(object):
    def __init__(self, value, children=None):
        self.children = children
        if children is None:
            self.children = {}
        self.value = value
        self.is_end = False

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.value == other.value
        return self.value == other

    def __repr__(self):
        return '<%s>:%s' % (self.value, self.is_end)

    def __sizeof__(self):
        return sys.getsizeof(self.value)

    __str__ = __repr__


class TrieTree(object):
    def __init__(self, patterns=None):
        self.root = {}
        if patterns is not None:
            self.build(patterns)

    def build(self, patterns):
        # rebuild trie tree
        self.clear()
        cursor, pre = self.root, None
        for p in patterns:
            values = p.split('.')
            for v in values:
                if v not in cursor:
                    cursor[v] = Node(v)
                pre, cursor = cursor, cursor[v].children
            pre[v].is_end = True
            cursor = self.root

    def add(self, pattern):
        cursor, pre = self.root, None
        values = pattern.split('.')
        for v in values:
            if v not in cursor:
                cursor[v] = Node(v)
            pre, cursor = cursor, cursor[v].children
        pre[v].is_end = True

    def remove(self, pattern):
        cursor, pre = self.root, None
        values = pattern.split('.')
        dels = []
        for v in values:
            if v not in cursor:
                return

            if len(cursor[v].children) <= 1:
                del_node = (v, cursor)
                dels.append(del_node)
            cursor = cursor[v].children

        while True:
            del_pat = '.'.join(x[0] for x in dels)
            if pattern.endswith(del_pat):
                value, node = dels[0]
                node.pop(value)
                return

            if not dels:
                break
            dels.pop(0)

    def clear(self):
        self.root.clear()

    def search(self, pattern):
        cursor, pre = self.root, None
        values = pattern.split('.')
        for v in values:
            if v not in cursor:
                break

            if cursor[v].is_end:
                return True
            pre, pre_key = cursor, v
            cursor = cursor[v].children
        return pre[pre_key].is_end

    def level_visit(self):
        size = 0
        queue, levels = [(0, self.root)], [0]
        while queue:
            level, current = queue.pop(0)
            for v in current.values():
                size += sys.getsizeof(v)
                if level == levels[0]:
                    levels.append(v)
                else:
                    print(levels[1:])
                    levels = [level, v]

                if v.children:
                    queue.append((level+1, v.children))
        if levels:
            print(levels[1:])
        print('Tree Szie: %d (bytes)' % size)

    def __contains__(self, pattern):
        return self.search(pattern)


if __name__ == '__main__':
    def dict_search(metric):
        values = metric.split('.')
        if not levels:
            return metric in d

        if len(values) < max(levels):
            return False

        for level in levels:
            if '.'.join(values[:level]) in d:
                return True
        return False


    with open('patterns.conf') as f:
        p = [s.strip() for s in f]

    d, levels = dict.fromkeys(p), None

    print time.time()
    tree = TrieTree(p)
    start = time.time()
    print start
    for _ in xrange(10000000):
        'h.l-orderpharos3_h_cn2.tcpconns_total.tcp_connections-ESTABLISHED' in tree
        #dict_search('h.l-orderpharos3_h_cn2.tcpconns_total.tcp_connections-ESTABLISHED')

    end = time.time()
    print end
    print end - start

