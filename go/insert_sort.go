package main

import (
	"fmt"
)

func InsertSort(datalist []int) []int {
	var j int

	for i, d := range datalist {
		if i == 0 {
			continue
		}

		j = i
		for j > 0 && datalist[j-1] > d {
			datalist[j] = datalist[j-1]
			j--
		}
		datalist[j] = d
	}

	return datalist
}

func main() {
	list := []int{2, 5, 3, 7, 10, 8, 4, 1, 100, 5, 100, 200, -1, -3}

	fmt.Println(InsertSort(list))
}
