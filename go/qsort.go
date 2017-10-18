package main

import "fmt"


func Qsort(list []int) []int {
    qsort(list, 0, len(list) - 1)
    return list
}

func qsort(list []int, begin, end int) {
    if begin >= end {
        return
    }
    small, fdata := begin, list[begin]

    for j := begin + 1; j <= end; j++ {
        if list[j] < fdata {
            small++
            list[small], list[j] = list[j], list[small]
        }
    }
    list[begin], list[small] = list[small], list[begin]

    qsort(list, begin, small)
    qsort(list, small + 1, end)
}

func main() {
    list := []int{9, 2, 8, 199, 100, 2, 0, 11}
    fmt.Println(Qsort(list))
}
