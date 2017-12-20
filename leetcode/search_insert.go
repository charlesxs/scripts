package main

import (
	"fmt"
)


func SearchInsert(target int, ary []int) int {
	i := len(ary) - 1
	for i >= 0 && target <= ary[i] {
		if target == ary[i] {
			return i
		}
		i--
	}
	return i + 1
}


func main() {
	ary := []int{1, 3, 5, 6}
	target := -1

	fmt.Print(SearchInsert(target, ary))
}
