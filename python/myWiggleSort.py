from random import choice


class Solution:
	@classmethod
	def wigglesort(cls, nums):
		nums.sort()
		div, mode = divmod(len(nums), 2)
		if mode: div += 1

		small, big = nums[:div], nums[div:]
		newlist = []
		if small[-1] < big[0]:
			list(map(lambda x,y: newlist.extend([x,y]), small, big))
		elif small[-1] == big[0]:
			while small[-1] == big[0]:
				newlist.extend([small.pop(), big.pop()])
			list(map(lambda x,y: newlist.extend([x,y]), small, big))

		return newlist


if __name__ == '__main__':
	#nums = [1, 3, 2, 2, 3, 1]
	nums = [1, 5, 1, 1, 6, 4]

#	def gen_nums():
#		source = list(range(10))
#		nums = []
#		for _ in range(10000000):
#			nums.append(choice(source))
#		return nums
#	nums = gen_nums()
	print(Solution.wigglesort(nums))

