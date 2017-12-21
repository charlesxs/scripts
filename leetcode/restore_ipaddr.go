package main

import (
	"fmt"
	"strconv"
)


func RestoreAddr(addr string) []string {
	var (
		res = make([]string, 0, 12)
		addrLen = len(addr)
	)

	if addrLen < 4 || addrLen > 12 {
		return res
	}


	for i:=3; i>0; i-- {
		for j:=3; j>0; j-- {
			for k:=3; k>0; k-- {
				//fmt.Println(i, j, k)
				if i + j + k >= addrLen {
					continue
				}
				s1, s2, s3, s4 := addr[0:i], addr[i:i+j], addr[i+j:i+j+k], addr[i+j+k:addrLen]
				//fmt.Println(s1, s2, s3, s4)
				if isValid(s1) && isValid(s2) && isValid(s3) && isValid(s4) {
					res = append(res, s1 + "." + s2 + "." + s3 + "." + s4)
				}
			}
		}
	}
	return res
}


func isValid(s string) bool {
	i, e := strconv.Atoi(s)

	if e != nil {
		return false
	}

	if i > 255 {
		return false
	}

	return true
}


func main() {
	str := "25525511135"
	//str := "1111111111"
	//str := "123456789"
	//str := "12345678"
	//str := "123456"
	//str := "12345"
	//str := "1234"
	res := RestoreAddr(str)
	fmt.Println(res, len(res))
}