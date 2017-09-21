package main

import (
	"fmt"
	"errors"
)


const (
	Empty = 0
)

type Stack struct {
	size int
	data []int
}



func (s *Stack) Push(v int) error {
	if len(s.data) >= s.size {
		return errors.New("exceed the size")
	}

	s.data = append(s.data, v)
	return nil
}


func (s *Stack) Pop() (int, error) {
	length := len(s.data)
	if length <= 0 {
		return Empty, errors.New("Empty stack")
	}

	data := s.data[length - 1]
	s.data = s.data[:(length - 1)]
	return data, nil
}

func (s *Stack) Top() (int, error)  {
	length := len(s.data)
	if length <= 0 {
		return Empty, errors.New("Empty stack")
	}

	return s.data[length - 1], nil
}


func (s *Stack) String() (res string) {
	for k, v := range s.data {
		res += fmt.Sprintf("[%v: %v] ", k, v)
	}
	return
}


func main() {
	s := &Stack{size: 30}


	for i:=0; i<=10; i++ {
		err := s.Push(i)
		if err != nil {
			break
		}
		v, _ := s.Top()
		fmt.Println(v)
	}

	fmt.Println("")
	fmt.Println(s.String())
	fmt.Println("")

	for i:=0; i<=10; i++ {
		v, err := s.Pop()
		if err != nil {
			break
		}

		fmt.Println(v)
	}


}