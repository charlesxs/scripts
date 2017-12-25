package main

import (
	"fmt"
)


func mergeSort(ary1, ary2 []int) []int {
	ary1Len, ary2Len := len(ary1), len(ary2)
	mergeAry := make([]int, ary1Len + ary2Len)

	var i, j, k int
	for i < ary1Len && j < ary2Len {
		if ary1[i] < ary2[j] {
			mergeAry[k] = ary1[i]
			i++
		} else {
			mergeAry[k] = ary2[j]
			j++
		}
		k++
	}

	for i < ary1Len {
		mergeAry[k] = ary1[i]
		i++
		k++
	}

	for j < ary2Len {
		mergeAry[k] = ary2[j]
		j++
		k++
	}
	return mergeAry
}


func FindMedianOfTwoArrays(ary1, ary2 []int) int {
	newAry := mergeSort(ary1, ary2)
	newLen := len(newAry)

	div := newLen / 2
	mod := newLen % 2

	if mod == 0 {
		return (newAry[div-1] + newAry[div]) / 2
	}
	return newAry[div]
}

func main()  {
	ary1 := []int{1, 3, 8, 9, 11, 11, 15, 19}
	ary2 := []int{3, 7, 11, 13, 19, 20, 22, 23, 111}
	fmt.Println(mergeSort(ary1, ary2))

	fmt.Println(FindMedianOfTwoArrays(ary1, ary2))
}

// 问题描述: https://leetcode.com/problems/median-of-two-sorted-arrays/description/
//
