// 使用 morris遍历实现前序、后序、中序遍历
package main

import (
	"fmt"
)

type ProcessFunc[T any] func(T)

// Node is tree node
type Node[T any] struct {
	value T
	left  *Node[T]
	right *Node[T]
}

// MorrisPre 实现 morris先序遍历
func (tree *Node[T]) MorrisPre(process ProcessFunc[T]) {
	if tree == nil {
		return
	}

	// 设置current指针，指向tree 的head节点
	current := tree
	// 声明 mostRight 节点
	var mostRight *Node[T]

	for current != nil {
		mostRight = current.left

		if mostRight != nil {
			// 找到最右子节点
			for mostRight.right != nil && mostRight.right != current {
				mostRight = mostRight.right
			}

			// 如果最右子节点的right子树为空，则临时让其指向当前节点。 (用于之后能够回到current节点)
			if mostRight.right == nil {
				mostRight.right = current
				// 处理当前节点
				process(current.value)

				// current节点向左移动
				current = current.left
				continue
			} else {
				mostRight.right = nil
			}
		} else {
			// 处理当前节点
			process(current.value)
		}

		// 当 当前节点所有的左子树处理完成后或者当前节点没有左子树，向右移动
		current = current.right
	}
}

// MorrisIn 实现 morris中序遍历
func (tree *Node[T]) MorrisIn(process ProcessFunc[T]) {
	if tree == nil {
		return
	}

	current := tree
	var mostRight *Node[T]

	for current != nil {
		mostRight = current.left
		if mostRight != nil {
			for mostRight.right != nil && mostRight.right != current {
				mostRight = mostRight.right
			}

			if mostRight.right == nil {
				mostRight.right = current
				current = current.left
				continue
			} else {
				mostRight.right = nil
			}
		}

		// 当mostRight是nil 说明来到了叶子节点，此时直接处理叶子节点数据
		// 而且此时叶子节点的 right节点一定是指向之前的current节点的，因此下面的 current = current.right就又回溯到了上级节点
		// 回溯到上级节点后，再经过一轮 mostRight处理，则此叶子节点的 mostRight.right = nil
		process(current.value)
		current = current.right
	}
}

// MorrisPost 实现morris后续遍历
func (tree *Node[T]) MorrisPost(process ProcessFunc[T]) {
	if tree == nil {
		return
	}

	current := tree
	var mostRight *Node[T]
	for current != nil {
		mostRight = current.left
		if mostRight != nil {
			for mostRight.right != nil && mostRight.right != current {
				mostRight = mostRight.right
			}

			if mostRight.right == nil {
				mostRight.right = current
				current = current.left
				continue
			} else {
				mostRight.right = nil
				tree.processEdge(current.left, process)
			}
		}
		current = current.right
	}

	tree.processEdge(tree, process)
}

// 辅助处理方法
func (tree *Node[T]) processEdge(node *Node[T], process ProcessFunc[T]) {
	tail := tree.reverseEdge(node)
	cur := tail
	for cur != nil {
		process(cur.value)
		cur = cur.right
	}

	tree.reverseEdge(tail)
}

// 翻转树
func (tree *Node[T]) reverseEdge(node *Node[T]) *Node[T] {
	var (
		pre  *Node[T]
		next *Node[T]
	)

	for node != nil {
		next = node.right
		node.right = pre
		pre = node
		node = next
	}
	return pre
}

func main() {
	t1 := &Node[int]{value: 1}
	t2 := &Node[int]{value: 2}
	t3 := &Node[int]{value: 3}
	t4 := &Node[int]{value: 4}
	t5 := &Node[int]{value: 5}
	t6 := &Node[int]{value: 6}
	t7 := &Node[int]{value: 7}

	t3.left = t6
	t3.right = t7
	t2.left = t4
	t2.right = t5
	t1.left = t2
	t1.right = t3

	fmt.Printf("先序遍历: ")
	t1.MorrisPre(func(d int) {
		fmt.Printf("%d ", d)
	})

	fmt.Println()
	fmt.Printf("中序遍历: ")
	t1.MorrisIn(func(d int) {
		fmt.Printf("%d ", d)
	})

	fmt.Println()
	fmt.Printf("后序遍历: ")
	t1.MorrisPost(func(d int) {
		fmt.Printf("%d ", d)
	})
}
