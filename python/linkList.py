# coding=utf-8
#

class ListNode:
    def __init__(self, data, next_=None):
        self.data = data
        self.next_ = next_


class LinkList:
    def __init__(self):
        self._head = None

    def __len__(self):
        return self.length

    def is_empty(self):
        return self._head is None

    @property
    def length(self):
        cursor, curindex = self._head, 0
        while cursor is not None:
            curindex += 1
            cursor = cursor.next_
        return curindex

    def prepend(self, data):
        if self._head is None:
            self._head = ListNode(data)
        else:
            self._head = ListNode(data, self._head)

    def append(self, data):
        if self._head is None:
            self._head = ListNode(data)
            return

        cursor = self._head
        while cursor.next_ is not None:
            cursor = cursor.next_

        cursor.next_ = ListNode(data)

    def insert(self, index, data):
        if self._head is None or index == 0:
            self.prepend(data)
            return 

        cursor, curindex = self._head, 0
        while cursor.next_ is not None and curindex < (index - 1):
            curindex += 1
            cursor = cursor.next_

        if (index -1) > curindex:
            self.append(data)
            return 

        cursor.next_ = ListNode(data, cursor.next_)

    def remove(self, data):
        if self._head is None:
            raise TypeError('list is empty!')
        
        if self._head.data == data:
            self._head = self._head.next_
            return 

        cursor = self._head 
        while cursor.next_ is not None and cursor.next_.data != data:
            cursor = cursor.next_

        if cursor.next_ is None:
            raise ValueError('data {0} is not in list'.format(data))
        cursor.next_ = cursor.next_.next_


    def pop(self):
        if self._head is None:
            raise TypeError('list is empty!')

        node = self._head
        self._head = self._head.next_
        return node.data

    def reverse(self):
        if self._head is None:
            raise TypeError('list is empty!')

        cursor = self._head
        while cursor.next_ is not None:
            current, cursor.next_ = cursor.next_, cursor.next_.next_
            current.next_, self._head = self._head, current

    def sort(self):
        if self._head is None or self._head.next_ is None:
            return

        cursor = self._head.next_
        self._head.next_ = None
        while cursor is not None:
            p, q = None, self._head
            while q is not None and q.data <= cursor.data:
                p = q
                q = q.next_

            nc = cursor.next_
            if p is None:
                cursor.next_ = self._head
                self._head = cursor
            else:
                cursor.next_ = p.next_
                p.next_ = cursor
            cursor = nc

    def printall(self):
        if self._head is None:
            return 

        cursor = self._head
        while cursor is not None:
            print cursor.data,
            cursor = cursor.next_
