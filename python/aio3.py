# coding=utf-8
# python >= 3.6
#

from time import time

event_list = []
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


class IOProxy(object):
    def __init__(self):
        super(IOProxy, self).__init__()
        self.callback = lambda *args: None
        self._done = False

    def set_callback(self, callback):
        self.callback = callback

    def done(self, value=None):
        self._done = True
        self.callback(value)


def sleep(timeout):
    iop = IOProxy()
    event = SleepEvent(timeout)
    event.set_callback(lambda: iop.done())
    return iop


def _next(gen, ioproxy, value=None):
    try:
        try:
            yielded_iop = gen.send(value)
        except TypeError:
            yielded_iop = next(gen)
        yielded_iop.set_callback(lambda value: _next(gen, ioproxy, value))
    except StopIteration as e:
        ioproxy.done(e.value)


def coroutine(func):
    def wrapper(*args, **kwargs):
        iop = IOProxy()
        gen = func(*args, **kwargs)
        _next(gen, iop)
        return iop
    return wrapper


def run():
    while len(event_list):
        for event in event_list:
            if event.is_ready():
                event_list.remove(event)
                break


if __name__ == '__main__':
    @coroutine
    def long_add(x, y, duration=1):
        yield sleep(duration)
        return x + y

    @coroutine
    def task(duration):
        print('start:', time())
        print((yield long_add(1, 2, duration)), time())
        print((yield long_add(3, 4, duration)), time())

    task(2)
    task(1)
    run()

