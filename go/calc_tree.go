package main

import (
	"fmt"
	"github.com/golang-collections/collections/stack"
	"strconv"
	"strings"
)


const (
	LEFT_BRACKET = iota
	RIGHT_BRACKET
	MATH_SYMBOL
	DIGITAL
)


type Token struct {
	value string
	_type interface{}
}

func NewToken(value string, _type interface{}) *Token {
	return &Token{value, _type}
}

func (t *Token) String() string {
	return fmt.Sprintf("%s<%d>", t.value, t._type)
}


type Tree struct {
	data *Token
	left *Tree
	right *Tree
}

func NewTree(data *Token, left, right *Tree) *Tree {
	return &Tree{
		data: data,
		left: left,
		right: right,
	}
}

func AssertTree(data interface{}) *Tree {
	if v, ok := data.(*Tree); ok {
		return v
	}
	return nil
}

func (t *Tree) SetLeft(ot *Tree) {
	t.left = ot
}

func (t *Tree) SetRight(ot *Tree)  {
	t.right = ot
}

func (t *Tree) MiddelVisit() {
	if t.left != nil {
		t.left.MiddelVisit()
	}

	fmt.Printf("%v", t.data)

	if t.right != nil {
		t.right.MiddelVisit()
	}
}



func Tokenize(expr string) []*Token {
	exprs := make([]*Token, 0, len(expr))
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
			exprs = append(exprs, token)
		}
	}
	return exprs
}


func MakeTree(tokens []*Token) *Tree {
	s := stack.New()
	for _, t := range tokens {
		switch t._type {
		case LEFT_BRACKET, MATH_SYMBOL:
			s.Push(NewTree(t, nil, nil))
		case DIGITAL:
			make_sub_tree(s, t)
		case RIGHT_BRACKET:
			r := AssertTree(s.Pop())
			if r.data._type == LEFT_BRACKET {
				panic("parser error")
			}
			left_paren := AssertTree(s.Pop())
			if left_paren.data._type != LEFT_BRACKET {
				panic("parser error")
			}

			make_sub_tree(s, r)
		}
	}

	return AssertTree(s.Pop())
}

func make_sub_tree(s *stack.Stack, i interface{})  {
	var current *Tree

	switch v := i.(type) {
	case *Tree:
		current = v
	case *Token:
		current = NewTree(v, nil, nil)
	}

	for s.Len() >= 1 && AssertTree(s.Peek()).data._type != LEFT_BRACKET {
		root := AssertTree(s.Pop())
		if root.data._type != MATH_SYMBOL {
			panic("wrong expression, expect math symbol")
		}

		left := AssertTree(s.Pop())
		if left.data._type != MATH_SYMBOL && left.data._type != DIGITAL {
			panic("wrong expression, expect digital")
		}

		root.SetLeft(left)
		root.SetRight(current)
		current = root
	}
	s.Push(current)
}

func calcTree(t *Tree) int {
	switch t.data.value {
	case "+":
		return calcTree(t.left) + calcTree(t.right)
	case "-":
		return calcTree(t.left) - calcTree(t.right)
	case "*":
		return calcTree(t.left) * calcTree(t.right)
	case "/":
		return calcTree(t.left) / calcTree(t.right)
	default:
		v, _ := strconv.Atoi(t.data.value)
		return v
	}
}

func Calc(expr string) int {
	tokens := Tokenize(expr)

	tree := MakeTree(tokens)

	return calcTree(tree)
}

func main() {
	//expr := "(3+4) * 5 / ((2+3) *3)"
	expr := "(3 + 4) * 5  / ((2+3) * 3) * 3"

	fmt.Println(Calc(expr))

}

