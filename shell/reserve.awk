#!/usr/bin/env awk
# 第5列相同的, 只保留最后3行
# 35000 11111111 0 1 1-fengdeng_03_10.43.14.232
# 35000 11111111 0 2 1-fengdeng_03_10.43.14.232
# 35000 11111111 0 3 1-fengdeng_03_10.43.14.232
# 35000 11111111 0 4 1-fengdeng_03_10.43.14.232
# 35000 11111111 0 5 1-fengdeng_03_10.43.14.232
# 35000 11111111 0 1 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 2 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 3 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 4 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 5 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 6 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 7 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 8 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 9 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 10 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 11 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 12 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 13 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 14 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 15 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 16 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 17 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 18 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 19 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 20 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 21 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 22 1-fengdeng_03_10.43.14.231
# 35000 11111111 0 1 1-fengdeng_03_10.43.14.235
# 35000 11111111 0 2 1-fengdeng_03_10.43.14.235
# 35000 11111111 0 3 1-fengdeng_03_10.43.14.235
# 35000 11111111 0 4 1-fengdeng_03_10.43.14.235
# 35000 11111111 0 5 1-fengdeng_03_10.43.14.235
# 35000 11111111 0 1 1-fengdeng_03_10.43.14.236
# 35000 11111111 0 1 1-fengdeng_03_10.43.14.237
# 35000 11111111 0 2 1-fengdeng_03_10.43.14.237

function echo_array(lines, __ARGEND__, i, line_length) {
    line_length = length(lines)
    if (line_length <= 0) {
        return
    }

    for (i=0; i<line_length; i++) {
        if (line_length <= 3) {
            print lines[i]
            continue
        }

        if (i > (line_length - 4)) {
            print lines[i]
        }
    }
}

function clear_array(lines, __ARGEND__, i) {
    for (i in lines) {
        delete lines[i]
    }
}

# main
{
    if (pre) {
        if (pre == $5) {
           lines[count] = $0
           count++
        } else {
            echo_array(lines)
            clear_array(lines)

            lines[0] = $0
            count = 1
            pre = $5
        }
    } else {
        lines[count] = $0
        count++
        pre = $5
    }
}

END {
    echo_array(lines)
}
