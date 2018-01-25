#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# import weakref


class MyProperty(object):
    def __init__(self, fget=None, fset=None, fdel=None):
        self.fget = fget
        self.name = fget.__name__
        self.fset = fset
        self.fdel = fdel
        # self.ins = weakref.WeakKeyDictionary()

    def __get__(self, instance, cls):
        # if self.fget and instance:
            # self.ins[instance] = self.fget(instance)
            # return self.ins[instance]
        # return instance
        return self.fget(instance)

    def __set__(self, instance, value):
        # if instance in self.ins:
        #     self.ins[instance] = self.fset(instance, value)
        if self.fset:
            instance.__dict__[self.name] = self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel:
            self.fdel(instance)

    def getter(self, fn):
        self.fget = fn

    def setter(self, fn):
        self.fset = fn
        return self

    def deleter(self, fn):
        self.fdel = fn


# class DemoMeta(type):
#     def __new__(cls, name, bases, attrs):
#         print name, bases, attrs
#         return type.__new__(cls, name, bases, attrs)


class Demo(object):
    # __metaclass__ = DemoMeta

    def __init__(self, val):
        self.__val = val

    @MyProperty
    def val(self):
        return self.__val

    @val.setter
    def val(self, value):
        if value >= 0:
            self.__val = value
        else:
            raise ValueError('Expect the value is greater than 0.')


if __name__ == '__main__':
    a = Demo(10)

    print a.val
    a.val = -1
    print a.val
