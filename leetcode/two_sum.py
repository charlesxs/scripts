# Two Sum

class Solution:
	def __init__(self, nums, target):
		self.nums = nums
		self.target = target
		self._new_nums = self.reserve_index_sort()
	
	def reserve_index_sort(self):
		new_nums = [(i, v) for i, v in enumerate(self.nums)]
		new_nums.sort(
			key=lambda x: x[1]
		)
		return new_nums

	def bisect_pick(self):
		low = 0
		high = len(self.nums) - 1
		
		while low <= high:
			mid = (low + high) // 2
			midval = self._new_nums[mid][1]

			if midval < self.target:
				low = mid + 1
			elif midval > self.target:
				high = mid - 1
			else:
				return mid - 1

		if low !=0 and high != len(self.nums) - 1:
			if self._new_nums[mid][1] >= self.target:
				return mid - 1
			return mid
		return -1

	def two_sum(self):
		len_nums = len(self._new_nums)
		for i in range(len_nums):
			if self._new_nums[i][1] >= self.target:
				break

			for j in range(i+1, len_nums):
				if self._new_nums[j][1] >= self.target:
					break

				if self._new_nums[i][1] + self._new_nums[j][1] == self.target:
					return self._new_nums[i][0], self._new_nums[j][0]
		return -1, -1
			

if __name__ == '__main__':
	nums = [26, 1, 5, 25, 25, 22, 23, 3, 18, 23]
	target = 45
	s = Solution(nums, 19)
	print(s.bisect_pick())
	print(s.two_sum())
