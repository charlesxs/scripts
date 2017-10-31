# coding=utf-8
#
# based on event callback
#
# 3.6 syntax

from time import time
from typing import List


class Event(object):
    def __init__(self):
        self.callback = lambda: None
        event_list.append(self)

    def set_callback(self, callback):
        self.callback = callback

    def is_ready(self):
        result = self._is_ready()
        if result:
            self.callback()

        return result


class SleepEvent(Event):
    def __init__(self, timeout):
        super(SleepEvent, self).__init__()
        self.timeout = timeout
        self.start_time = time()

    def _is_ready(self):
        return time() - self.start_time >= self.timeout


def sleep(timeout):
    return SleepEvent(timeout)


def _next(task):
    try:
        event = next(task)
        event.set_callback(lambda: _next(task))
    except StopIteration:
        pass 


def runner(tasks):
    for task in tasks:
        _next(task)

    while event_list:
        for event in event_list:
            if event.is_ready():
                event_list.remove(event)
                break


event_list: List[Event] = []

if __name__ == '__main__':
    def task(name):
        print(name, 1)
        yield sleep(1)
        print(name, 2)
        yield sleep(2)
        print(name, 3)
        yield sleep(3)
        print(name, 'task over')
    
    runner((
        task('task1'),
        task('task2'),
        task('task3')
    ))

