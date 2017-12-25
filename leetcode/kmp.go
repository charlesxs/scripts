package main

import (
	"fmt"
)


func maxMap(m map[int]string) (string, int) {
	var max int
	for k := range m {
		if k > max {
			max = k
		}
	}
	return m[max], max
}


func lengthOfLongestSubstring(s string) (string, int) {
	var (
		i, j = 0, 1
	)
	length := len(s)
	//res := make([]int, length)
	res := make(map[int]string)

	for j < length {
		for p := i; p < j; p++ {
			if s[p] == s[j] {
				res[j-i] = s[i:j]
				//res = append(res, j - i)
				i = p + 1
				break
			}

			if p == j - 1 && j == length - 1{
				res[j-i+1] = s[i:j+1]
				break
			}
		}
		j++
	}
	return maxMap(res)
}


func main() {
	s1 := "abcabcbb"
	s2 := "pwwkew"
	s3 := "bbbbb"
	s4 := "dafddwrtyq"
	s5 := "dawdrtdywd"
	fmt.Println(lengthOfLongestSubstring(s1))
	fmt.Println(lengthOfLongestSubstring(s2))
	fmt.Println(lengthOfLongestSubstring(s3))
	fmt.Println(lengthOfLongestSubstring(s4))
	fmt.Println(lengthOfLongestSubstring(s5))
}

// 问题描述: https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
//