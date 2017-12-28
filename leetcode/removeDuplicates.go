package main

import (
	"fmt"
)


func RemoveDuplicates(list []int ) int {
	length := len(list)
	if length == 0 {
		return length
	}

	var i int
	for j := 1; j < length; j++ {
		if list[i] != list[j] {
			i++
			list[i] = list[j]
		}
	}

	return  i + 1
}


func main() {
	list := []int{1, 3, 3, 5, 6, 9, 9, 9, 9, 10, 10, 11}

	r := RemoveDuplicates(list)
	fmt.Println(list[:r], r)
}


// 问题描述: https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/
//

