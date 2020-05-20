# coding=utf-8
#
# 给定一个数组，数组中只包含 0 和 1
# 给定一个数字，比如是3，求将数组中任意的3个0替换成1后，数组中连续是1的最长长度是多少
#

dlist = [0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1]

def resolve(number):
    members = []
    stage_count = cursor = 0
    for i, v in enumerate(dlist):
        if v == 0:
            if number > 0:
                stage_count += 1
                number -= 1
            else:
                members.append(stage_count)
                cursor = _move(dlist, cursor, 1)
                stage_count = i - cursor + 1
                # print('cursor: ', cursor, 'stage_count: ', stage_count, 'current_index: ', i)
        else:
            stage_count += 1

    members.append(stage_count)
    # print(members)
    return max(members)

def _move(l, cursor, distance):
    for j in range(cursor, len(l)):
        if distance <= 0:
            break
        if l[j] == 0:
            cursor += 1
            distance -= 1
        else:
            cursor += 1
    return cursor

print(resolve(3))
