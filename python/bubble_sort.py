# coding=utf-8
#
# 添加一个 change 变量, 优化算法让其更具有适应性, 比如给定一个已经排好序的序列, 则只需要循环 n 次, 避免了无用功.
#

def bubble_sort(lst):
    length = len(lst)
    for i in range(length):
        change = False
        for j in range(1, length - i):
            if lst[j] <= lst[j-1]:
                lst[j], lst[j-1] = lst[j-1], lst[j]
                change = True
        if not change:
            break
    return lst


if __name__ == '__main__':
    lst = [-1, 199, 2, 91, 3, 19, 1, 0, 1, 2]
    lst2 = [1, 2, 3, 4, 5, 6, 7, 8]
    print bubble_sort(lst)
    print bubble_sort(lst2)
