package main

import (
	"fmt"
	"math"
)

type List struct {
	data int
	head, next, last *List
}

func NewList() *List {
	 return new(List)
}

func NewListFromData(n int) *List {
	first := &List{
		data: n,
		next: nil,
	}
	first.head = first
	return first
}


func (l *List) Append(n int)  {
	if l.head == nil {
		l.data, l.head = n, l
		l.last = l
		return
	}
	//current := l.head
	//for current.next != nil {
	//	current = current.next
	//}
	//current.next = NewListFromData(n)

	nlist := NewListFromData(n)
	l.last.next = nlist
	l.last = nlist
}

func (l *List) Prepend(n int) {
	if l.head == nil {
		l.data, l.head = n, l
		l.last = l
		return
	}
	newhead := NewListFromData(n)
	newhead.next = l.head
	l.head = newhead
}

func (l *List) Length() int {
	var count int
	if l.head == nil {
		return count
	}

	current := l.head
	for current != nil {
		count++
		current = current.next
	}
	return count
}

func (l *List) Pop() int {
	if l.head == nil {
		return 0
	}

	node := l.last
	current := l.head
	for current.next.next != nil {
		current = current.next
	}
	l.last = current
	l.last.next = nil
	return node.data
}

func (l *List) Insert(i, n int) {
	if l.head == nil {
		l.head = NewListFromData(n)
		return
	}

	if i == 0 {
		l.Prepend(n)
		return
	}

	var count int
	current := l.head
	for current.next != nil {
		if count == i - 1 {
			node := NewListFromData(n)
			current.next, node.next = node, current.next
			return
		}
		current = current.next
		count++
	}

	l.Append(n)
}

func (l *List) Reverse() {
	if l.head == nil || l.head.next == nil {
		return
	}
	var (
		current, previous *List
	)

	current, previous = l.head, nil
	l.last = current
	for current.next != nil {
		node := current

		current = current.next
		node.next = previous
		previous = node
	}

	l.head = current
	l.head.next = previous
}

func (l *List) ForEach(fn func(i, n int)) {
	if l.head == nil {
		return
	}
	var index int
	current := l.head
	for current != nil {
		fn(index, current.data)
		current = current.next
		index++
	}
}


func addTwoNumbers(l1, l2 *List) *List {
	var (
		r1, r2 int
	)
	l1.ForEach(func(i, n int) {
		r1 = int(math.Pow10(i)) * n + r1
	})

	l2.ForEach(func(i, n int) {
		r2 = int(math.Pow10(i)) * n + r2
	})

	s := r1 + r2
	l3 := NewList()
	for s != 0 {
		l3.Append(s % 10)
		s /= 10
	}

	return l3
}

func main() {
	// 432 + 384 = 816

	list := NewList()
	list.Append(2)
	list.Append(3)
	list.Append(4)

	l2 := NewList()
	l2.Append(4)
	l2.Append(8)
	l2.Append(3)

	l3 := addTwoNumbers(list, l2)
	l3.ForEach(func(i, n int) {
		fmt.Println(i, n)
	})
}

