# coding=utf-8
#

class Node:
    def __init__(self, data, next_):
        self.data = data
        self.next = next_

    def __repr__(self):
        return self.data

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def append(self, data):
        node = Node(data, None)
        if self.head is None:
            self.head = node

        if self.tail is None:
            self.tail = node

        self.tail.next = node
        self.tail = node
    
    def show(self):
        cursor = self.head
        while True:
            print cursor.data, 
            if cursor.next is None:
                break
            cursor = cursor.next
        print
    
    def reverse(self):
        cursor = org = self.head
        while True:
            if org.next is None:
                self.tail = org
                break

            self.head = org.next
            org.next = self.head.next
            self.head.next = cursor
            cursor = self.head

if __name__ == '__main__':
    l = LinkedList()
    for i in range(9):
        l.append(i)
    l.show()
    l.reverse()
    l.show()
