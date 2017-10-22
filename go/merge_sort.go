package main

import "fmt"

func mergeBlock(lfrom, lto []int, low, mid, high int) {
    i, j, k := low, mid, low
    for i < mid && j < high {
        if lfrom[i] <= lfrom[j] {
            lto[k] = lfrom[i]
            i++
        } else {
            lto[k] = lfrom[j]
            j++
        }
        k++
    }

    for i < mid {
        lto[k] = lfrom[i]
        i++
        k++
    }

    for j < high {
        lto[k] = lfrom[j]
        j++
        k++
    }
}


func mergePass(lfrom, lto []int, block_len, list_len int) {
    low, mid, high := 0, block_len, block_len * 2
    for high < list_len {
        mergeBlock(lfrom, lto, low, mid, high)
        low, mid = high, high + block_len
        high = mid + block_len
    }

    if low + block_len < list_len {
        mergeBlock(lfrom, lto, low, low + block_len, list_len)
    } else {
        tmp := lfrom[low:]
        for _, v := range tmp {
            lto[low] = v
            low++
        }
    }
}


func MergeSort(list []int) []int {
    block_len, list_len := 1, len(list)
    tmplist := make([]int, list_len)
    for block_len < list_len {
        mergePass(list, tmplist, block_len, list_len)
        block_len *= 2
        mergePass(tmplist, list, block_len, list_len)
        block_len *= 2
    }

    return list
}


func main() {
    list := []int{99, 2, 100, 103, 105, 33, 2, 0, -10, 101, 97, 3, 44, 101, 10000, 3, -2, -1}
    fmt.Println(MergeSort(list))
}
