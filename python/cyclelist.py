from linklist import ListNode


class CycleList(object):
    def __init__(self):
        self.tail = None

    def is_empty(self):
        return self.tail is None

    def prepend(self, data):
        p = ListNode(data)
        if self.tail is None:
            self.tail = p.next_ = p
        else:
            p.next_ = self.tail.next_
            self.tail.next_ = p

    def append(self, data):
        self.prepend(data)
        self.tail = self.tail.next_

    def pop(self):
        if self.tail is None:
            raise TypeError('list is empty!')
        p = self.tail.next_
        self.tail.next_ = self.tail.next_.next_
        return p.data

    def printall(self):
        if self.tail is None:
            return

        cursor = self.tail.next_
        while cursor is not self.tail:
            print cursor.data,
            cursor = cursor.next_
        print cursor.data


#class CycleMeta(type):
#    def __new__(cls, name, bases, attrdict):
#        newattr = {k:v for k, v in attrdict.items() if k != 'prepend'}
#        return type.__new__(cls, name, bases, newattr)

#class CycleDescriptor(object):
#    def __set__(self, instance, value):
#        raise Exception('can not set new value')
#
#    def __get__(self, instance, cls):
#        if isinstance(instance, cls):
#            raise Exception('can not call it')
#

class CycleRepeatList(CycleList):
#    __metaclass__ = CycleMeta
#    prepend =  CycleDescriptor()

    def __init__(self, maxlen):
        super(CycleRepeatList, self).__init__()
        self.maxlen = maxlen
        self.length = 0
        self.cursor_index = 0

    def __len__(self):
        return self.length

    def prepend(self, data):
        self.append(data)
    
    def append(self, data):
        if self.length == self.maxlen:
            cursor = self.tail.next_
            cindex = 0
            while cursor is not self.tail and cindex != self.cursor_index:
                cursor = cursor.next_
                cindex += 1
            cursor.data = data
            if cursor is self.tail:
                self.cursor_index = 0
            else:
                self.cursor_index += 1
            return

        p = ListNode(data)
        if self.tail is None:
            self.tail = p.next_ = p
            self.length += 1
        else:
            p.next_ = self.tail.next_
            self.tail.next_ = p
            self.tail = p
            self.length += 1

    def pop(self):
        data = super(CycleRepeatList, self).pop()
        self.length -= 1
        self.cursor_index = 0
        return data
