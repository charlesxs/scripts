# coding=utf-8
# 归并排序的核心思想是 将一组序列数据看做是若干组子序列数据, 并进行两两合并, 合并过程中对其排序, 然后会得出若干个较大的排序过的子序列(2倍与原始子
# 序列), 然后对这些排序过的子序列再 两两合并, 一直重复, 直到子序列长度跟原始表长度相等 说明排序完成. 
#
# 这其中需要一个长度为 n 的表作为辅助空间, 因为在两两合并过程中, 两对子序列相互对比, 将最小的数据一一复制到辅助表中, 直到合并完成, 第二次合并时,
# 辅助表作为源表, 向原始表合并 copy, 来回翻转.
#
# 归并排序基本方法如下:
# 1. 初始时, 把待排序序列中的 n 个记录看成是 n 个有序子序列(因为一个记录的序列总是排好序的), 每个子序列的长度均为1
# 2. 把当时序列组里的有序子序列两两归并,完成一遍后序列组里的排序序列个数减半, 每个子序列长度加倍.
# 3. 对加长的有序子序列重复上面的操作, 最终得到一个长度为 n 的有序序列.
#

import random

def merge_block(lfrom, lto, low, mid, high):
    '''
        控制两个 子序列进行归并, 并copy 到临时表中
    '''
    i, j, k = low, mid, low
    while i < mid and j < high:
        if lfrom[i] <= lfrom[j]:
            lto[k] = lfrom[i]
            i += 1
        else:
            lto[k] = lfrom[j]
            j += 1
        k += 1

    while i < mid:
        lto[k] = lfrom[i]
        i += 1
        k += 1

    while j < high:
        lto[k] = lfrom[j]
        j += 1
        k += 1


def merge_pass(lfrom, lto, block_len, length):
    '''
        控制进行当子序列长度为 n 时, 一次完整的归并
    '''
    low, mid, high = 0, block_len, block_len * 2
    while high < length:
        k = merge_block(lfrom, lto, low, mid, high)
        low, mid = high, high + block_len
        high = mid + block_len
    
    if low + block_len < length:
        merge_block(lfrom, lto, low, low + block_len, length)
    else:
        lto[low:] = lfrom[low:]
        

def merge_sort(lst):
    '''
        此为总控制函数, 因为临时表和原表要来回copy,所以最后真正的结果存在那个表中要看
        exchange % 2 的结果, 因为当copy奇数次的时候, 结果在 tmplist表中, 偶数次则在lst 
        中, 这样中方式是最后可能少copy一次, 下面的merge_sort() 是书中的例子, 优点是简单,缺点
        可能要多copy 一次, 将已经排序好的结果从 tmplist, 在复制回 lst中.
    '''
    block_len, length = 1, len(lst)
    tmplist = [None] * length
    exchange = 0
    while block_len < length:
        if exchange % 2 == 0:
            merge_pass(lst, tmplist, block_len, length)
        else:
            merge_pass(tmplist, lst, block_len, length)
        exchange += 1
        block_len *= 2
    if exchange % 2 == 0:
        return lst
    return tmplist

# def merge_sort(lst):
#     block_len, length = 1, len(lst)
#     tmplist = [None] * length
#     while block_len < length:
#         merge_pass(lst, tmplist, block_len, length)
#         block_len *= 2
#         merge_pass(tmplist, lst, block_len, length)
#         block_len *= 2
#     return lst


if __name__ == '__main__':
    data = []
    for i in range(16):
        data.append(random.choice(range(100)))
    # lst = [199, 23, 56, 11, 20, 2, 22, 3, 0, 4, 8, 6, -1]
    print('orgin: ', data)
    print('sorted: ', merge_sort(data))

