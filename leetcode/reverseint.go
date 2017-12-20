package main

import (
	"fmt"
	//"strconv"
	"math"
)

//func ReverseInt(num int) int {
//	n := []byte(strconv.Itoa(num))
//	var i, j int
//	j = len(n) - 1
//	for i <= j {
//		n[i], n[j] = n[j], n[i]
//		i++
//		j--
//	}
//	rs, _ := strconv.Atoi(string(n))
//	return rs
//}

func ReverseInt(num int) int {
	var (
		digitalSymbol = 1
		result int
	)

	if num < 0 {
		digitalSymbol = -1
		num = num * -1
	}

	for num != 0 {
		result = result * 10 + (num % 10)
		num = num / 10
	}
	result = result * digitalSymbol

	if result > math.MaxInt32 || result < math.MinInt32 {
		return 0
	}
	return result
}

func main() {
	fmt.Println(ReverseInt(123))
	fmt.Println(ReverseInt(-123))
}
