package main

import (
	"fmt"
)


//func RemoveElement(ele int, list []int) (int, []int) {
//	var (
//		i, count int
//	)
//	length := len(list)
//	for i < length-count {
//		if list[i] != ele {
//			i++
//			continue
//		}
//
//		for j := i; j < (length-count-1); j++{
//			list[j] = list[j+1]
//		}
//		count++
//		i = 0
//	}
//	return length - count, list[0:length-count]
//}



func RemoveElement(ele int, list []int) (int, []int) {
	var i int

	length := len(list)

	for j := 0; j < length; j++ {
		if list[j] != ele {
			list[i] = list[j]
			i++
		}
	}

	return i, list[0:i]
}



func main() {
	list := []int{3, 3, 6, 2, 3, 4, 3}

	fmt.Println(RemoveElement(3, list))
}

