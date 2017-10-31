# coding=utf-8
#

def task(to):
    for i in range(to):
        yield
        print(f'task{to}', i)

def run(tasks):
    if isinstance(tasks, tuple):
        tasks = list(tasks)

    while tasks:
        for task in tasks:
            try:
                next(task)
            except StopIteration:
                tasks.remove(task)
                break


if __name__ == '__main__':
    run((
        task(3),
        task(4),
        task(2)
    ))

