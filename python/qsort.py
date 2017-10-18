# coding=utf-8
#
# 快排是一种递归排序算法, 核心思想是在一组序列数据上，选取一个划分点(通常用第一个数据作为划分点), 然后比这个划分点数据大的放表后面，小的放表前面,
# 直到一次循环对比完成, 这时表被分为大小两组, 大的集中在后面, 小的集中在前面.  然后用相同方式递归得到的这两组记录,直到所有递归完成, 则排序完成.
# 
# 而快排又有多种实现方式, 比如: 逆序对比 和 交换记录位置的方式.  下面这种方式是交换记录位置的方式,更简洁一些.
#
# 这里还有一个注意点: 就是在交换记录的过程中, 首先设置了一个游标(这里叫small), 永远指向最后一个比划分点小的数据的位置. 这样在交换过程中就很方便, 
# 遇到大的不动, 遇到小的数据, 则游标下一个数据必然比划分点大, 这样只需要让当前小元素和游标下一个元素相互交换即可, 然后游标向前走一步.
# 而一次循环完成后, 表前知道small位置前所有的元素都比划分点小, small位置后所有的元素都比划分点大,因此small所在的位置也就是划分点最正确的位置, 将
# 它们两个位置互换既可得到正确位置.
#

def qsort(lst):
    def _qsort(lst, begin, end):
        if begin >= end:
            return
        small, fdata = begin, lst[begin]
        for j in range(begin+1, end+1):
            if lst[j] < fdata:
                small += 1
                lst[small], lst[j] = lst[j], lst[small]
        lst[begin], lst[small] = lst[small], lst[begin]
        _qsort(lst, 0, small)
        _qsort(lst, small+1, end)
    _qsort(lst, 0, len(lst)-1)
    return lst



if __name__ == '__main__':
    lst = [9, 11, 2, 4, 6, 199, 100, 200, 3, -1]
    print lst
    print qsort(lst)
