package main

import (
	"fmt"
)

const (
	LPAREN = "("
	RPAREN = ")"
)


func GenParentheses(n int) {
	//res := make([]string, 0, n*n)
	rchain := make(chan string)

	var (
		r string
		lc, rc int
	)

	go func() {
		for {
			select {
			case v := <- rchain:
				fmt.Println(v)
			default:
			}
		}
	}()

	genParen(rchain, r, n, lc, rc)
}


func genParen(rchain chan string, r string, n, lc, rc int) {
	if lc == n {
		for i := 0; i < lc - rc; i++ {
			r += RPAREN
		}
		rchain <- r
		//close(rchain)
		return
	}

	if lc > rc {
		genParen(rchain, r + LPAREN, n, lc+1, rc)
		genParen(rchain, r + RPAREN, n, lc, rc+1)
	}

	if lc == rc {
		genParen(rchain, r + LPAREN, n, lc+1, rc)
	}
}


func main() {
	GenParentheses(3)
}


// 写这段代码的时候遇到几个小问题:
// 1. 一个slice 当作参数传递给另外一个函数的时候, 如果在另外的函数使用 s = append(s, xx) 这时候原函数中的slice s 并没有相应的改变,
// 但是如果使用 s[0] = xx, 那么原函数的slice s 第0个元素会改变, 因为 append后 虽然slice底层的数组没有变化, 但是上层的引用(slice
// 名) 其实却是生成一个新的引用. (这个地方是不如python list的, list也是引用传递, 而且传递的是list的实例, 另外的函数只要调实例方法来 l.append,
// 这样源函数内部的 l 也是会变化.)

// 2. 在 GenParentheses 函数中如果这么写:
// go genParen(rchain, r, n, lc, rc)
// for {
//    select {
//	  case v := <- rchain:
//		fmt.Println(v)
//	  default:
//    }
// }
// 首先，如果 select 内部没有default 语句, 等于就是不忽略所有channel都没准备好的情况，那么在 genParen这个 goroutine生成完所有的括号后，程序会报 deadlock,
// 然后退出。
// 而加上 default 程序虽然不会报deadlock退出，但是当 genParen生成完所有的括号后, 整个程序就阻塞了, 并不会退出。这是因为你在主goroutine 中监听并从一个
// channel中接收数据, 这个时候如果没有其他goroutine向这个channel发送数据(或者发送数据的goroutine都退出了), 那么主线程就会阻塞, 而此时其他的goroutine
// 又没有数据可以向这个channel中发送, 那么程序就出现了死锁. (即所有的goroutine都被阻塞住了.)
//
// 所以在这种情况下, 使用最后GenParentheses函数中的写法, 让接受channel的部分不在主线程中运行, 而生成数据的部分运行在main goroutine中, 这样数据生成完后, main
// goroutine 就会退出，相应的 接受部分的 goroutine 也会随之退出.
//
