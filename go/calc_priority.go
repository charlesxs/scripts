package main

import (
	"fmt"
	"github.com/golang-collections/collections/stack"
	"strings"
	"strconv"
	"errors"
)


const (
	LEFT_BRACKET = iota
	RIGHT_BRACKET
	DIGITAL
	MATH_SYMBOL
)


type Token struct {
	value string
	_type int
}

func NewToken(value string, _type int) *Token {
	return &Token{
		value: value,
		_type: _type,
	}
}

func AssertToken(i interface{}) *Token {
	if v, ok := i.(*Token); ok {
		return v
	}
	return nil
}

func (t *Token) String() string {
	return fmt.Sprintf("%s<%d>", t.value, t._type)
}


func Tokenize(expr string) []*Token {
	tokens := make([]*Token, 0, len(expr))
	var token *Token

	for _, v := range expr {
		newv := string(v)

		switch newv {
		case "(":
			token = NewToken(newv, LEFT_BRACKET)
		case ")":
			token = NewToken(newv, RIGHT_BRACKET)
		case "+", "-", "*", "/":
			token = NewToken(newv, MATH_SYMBOL)
		default:
			if strings.Trim(newv, " ") == "" {
				continue
			}
			token = NewToken(newv, DIGITAL)
		}

		if token != nil {
			tokens = append(tokens, token)
		}
	}
	return tokens
}



func ConvertSuffixExpression(tokens []*Token) []*Token {
	primap := map[string]int{
		"(": 1,
		"+": 3,
		"-": 3,
		"*": 5,
		"/": 5,
	}

	exprs := make([]*Token, 0, len(tokens))
	ops := stack.New()
	for _, t := range tokens {
		if t._type == DIGITAL{
			exprs = append(exprs, t)

		} else if ops.Len() < 1 || t._type == LEFT_BRACKET {
			ops.Push(t)

		} else if t._type == MATH_SYMBOL {
			for ops.Len() >= 1 &&
				primap[AssertToken(ops.Peek()).value] >= primap[t.value] {
				exprs = append(exprs, AssertToken(ops.Pop()))
			}

			ops.Push(t)

		} else if t._type == RIGHT_BRACKET {
			for ops.Len() >= 1 && AssertToken(ops.Peek())._type != LEFT_BRACKET {
				exprs = append(exprs, AssertToken(ops.Pop()))
			}

			if AssertToken(ops.Pop())._type != LEFT_BRACKET {
				panic("wrong expression, expect left paren")
			}
		}
	}

	for ops.Len() >= 1 {
		exprs = append(exprs, AssertToken(ops.Pop()))
	}

	return exprs
}


func Calc(expr string) int {
	s := stack.New()
	opsmap := map[string]func(left, right int) int{
		"+": func(left, right int) int {
			return left + right
		},

		"-": func(left, right int) int {
			return left - right
		},

		"*": func(left, right int) int {
			return left * right
		},

		"/": func(left, right int) int {
			return left / right
		},
	}

	tokens := ConvertSuffixExpression(
		Tokenize(expr),
	)

	for _, t := range tokens {
		switch t._type {
		case DIGITAL:
			s.Push(t.value)

		case MATH_SYMBOL:
			if s.Len() < 2 {
				panic("parse error, less than two digital")
			}

			right, err := AssertInt(s.Pop())
			if err != nil {
				panic("AssertInt error, bad expression")
			}

			left, err := AssertInt(s.Pop())
			if err != nil {
				panic("AssertInt error, bad expression")
			}

			res := opsmap[t.value](left, right)

			s.Push(res)
		}
	}

	res, err := AssertInt(s.Pop())
	if err != nil {
		panic("Calculate failed")
	}
	return res
}


func AssertInt(i interface{}) (int, error) {
	switch v := i.(type) {
	case string:
		return strconv.Atoi(v)
	case int:
		return v, nil
	default:
		return 0, errors.New("AssertInt error, bad expression")
	}

}

func main()  {
	expr := "(3 + 4) * 5  / ((2+3) * 3) * 3"
	//expr := "3 + 4 * 5  / (2+3)"

	fmt.Println(Calc(expr))
}

