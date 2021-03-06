"""
随缘刷题
"""
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        """1248. 统计「优美子数组」
        https://leetcode-cn.com/problems/count-number-of-nice-subarrays/
        """
        index_list = []
        for index, num in enumerate(nums):
            if num % 2:
                index_list.append(index)
        length = len(index_list)
        output = 0
        if length >= k:
            index_list.insert(0, -1)
            index_list.append(len(nums))
            for index in range(1, length - k + 2):
                lft = (index_list[index] - index_list[index - 1])
                rht = (index_list[index + k] - index_list[index + k - 1])
                output += lft * rht
        return output

    def rightSideView(self, root: TreeNode) -> List[int]:
        """199. 二叉树的右视图
        https://leetcode-cn.com/problems/binary-tree-right-side-view/
        """
        if not root:
            return []

        def _get_child_nodes(result: List[int], nodes: List[TreeNode]):
            result.append(nodes[-1].val)
            child = []
            for node in nodes:
                if node.left:
                    child.append(node.left)
                if node.right:
                    child.append(node.right)
            if child:
                return _get_child_nodes(result, child)
            return result

        return _get_child_nodes([], [root])

    def generateParenthesis(self, n: int) -> List[str]:
        """22. 括号生成
        https://leetcode-cn.com/problems/generate-parentheses/
        """
        result = []
        if not n:
            return result
        data = [1 for _ in range(n)] + [-1 for _ in range(n)]  # ( 转换为 1   ) 转换为 -1
        rst = [1]  # 完整括号肯定由 ( 开头
        data.remove(1)
        lst = [(rst, data)]
        while lst:
            lst_bak = []
            for (_rst, _data) in lst:
                for i in [1, -1]:  # 依次取出  (  )
                    if i not in _data:
                        continue
                    _rst_bak = _rst[:]
                    _rst_bak.append(i)
                    if sum(_rst_bak) < 0:  # 相加 小于0说明 ) 多了
                        continue
                    _data_bak = _data[:]
                    _data_bak.remove(i)
                    if _data_bak:
                        lst_bak.append((_rst_bak, _data_bak))
                    else:
                        result.append(_rst_bak)
            lst = lst_bak[:]
        return ["".join(["(" if i == 1 else ")" for i in each]) for each in result]  # 数字转化成()

    def waysToChange(self, n: int) -> int:
        """面试题 08.11. 硬币
        https://leetcode-cn.com/problems/coin-lcci/
        拉闸
        """
        coins = [25, 10, 5, 1]
        return 0

    def trap(self, height: List[int]) -> int:
        """42. 接雨水
        https://leetcode-cn.com/problems/trapping-rain-water/
        拉闸
        光荣超时:https://leetcode-cn.com/submissions/detail/65325877/testcase/
        """
        water = 0
        if not height:
            return water
        max_height = max(height)

        def _strip(_lst: List[int], _key) -> List[int]:
            while _lst[0] == _key:
                _lst = _lst[1:]
            while _lst[-1] == _key:
                _lst = _lst[:-1]
            return _lst

        for n in range(max_height):
            height = _strip(height, n)
            string_height_bak = height[:]
            for index, s in enumerate(string_height_bak):
                if s == n:
                    water += 1
                    height[index] += 1
        return water

    def reversePairs(self, nums: List[int]) -> int:
        """面试题51. 数组中的逆序对
        https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof/
        拉闸
        光荣超时:https://leetcode-cn.com/submissions/detail/65503938/testcase/
        """
        result = 0
        for index, num in enumerate(nums):
            for n in nums[index + 1:]:
                if num > n:
                    result += 1
        return result

    def canJump(self, nums: List[int]) -> bool:
        """55. 跳跃游戏
        https://leetcode-cn.com/problems/jump-game/
        """
        nums_reverse = nums[::-1]
        nums_length = len(nums)
        l_pointer = r_pointer = 0  # 双指针
        while l_pointer != nums_length - 1:
            if r_pointer < nums_length:
                r_value = nums_reverse[r_pointer]
                distance = r_pointer - l_pointer
                if r_value >= distance:
                    l_pointer = r_pointer
                r_pointer += 1
            else:
                return False
        return True

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """56. 合并区间
        https://leetcode-cn.com/problems/merge-intervals/
        """
        if not intervals:
            return intervals
        results = []
        intervals.sort(key=lambda x: x[0])
        base_low, base_high = intervals[0]
        for (low, high) in intervals[1:]:
            if low <= base_high:
                if high > base_high:
                    base_high = high
            else:
                results.append([base_low, base_high])
                base_low, base_high = low, high
        else:
            results.append([base_low, base_high])
        return results

    def minDistance(self, word1: str, word2: str) -> int:
        """72. 编辑距离
        https://leetcode-cn.com/problems/edit-distance/
        拉闸 面向测试用例编程失败
        """
        mem = dict()

        def dp(i, j):
            if (i, j) in mem:
                return mem[(i, j)]
            if i == -1:     # 触底
                mem[(i, j)] = j + 1
            elif j == -1:     # 触底
                mem[(i, j)] = i + 1
            elif word1[i] == word2[j]:
                mem[(i, j)] = dp(i - 1, j - 1)
            else:
                mem[(i, j)] = min(
                    dp(i, j - 1) + 1,   # 插入操作
                    dp(i - 1, j) + 1,   # 删除操作
                    dp(i - 1, j - 1) + 1,   # 替换操作
                )
            return mem[(i, j)]
        return dp(len(word1) - 1, len(word2) - 1)

    def singleNumbers(self, nums: List[int]) -> List[int]:
        """面试题56 - I. 数组中数字出现的次数
        https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-lcof/
        仅仅能过关 官方推荐异或运算^
        """
        if len(nums) == 1:
            return nums
        nums.sort()
        result = []
        if nums[0] != nums[1]:
            result.append(nums[0])
        if nums[-1] != nums[-2] and nums[-1] not in result:
            result.append(nums[-1])
        for i in range(1, len(nums) - 1):
            if nums[i - 1] != nums[i] and nums[i] != nums[i + 1]:
                result.append(nums[i])
        return result

    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        """23. 合并K个排序链表
        https://leetcode-cn.com/problems/merge-k-sorted-lists/
        不想写笨方法
        """
        pass


def run():
    # opt = Solution().numberOfSubarrays([1, 1, 2, 1, 1], 3)
    # opt = Solution().numberOfSubarrays([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2)
    # opt = Solution().generateParenthesis(11)
    # opt = Solution().waysToChange(11)       # 崩了崩了
    # opt = Solution().trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    # opt = Solution().trap([4, 2, 3])
    # opt = Solution().reversePairs([7, 5, 6, 4])
    # opt = Solution().canJump([2, 3, 1, 1, 4])
    # opt = Solution().canJump([3, 2, 1, 0, 4])
    # opt = Solution().merge([[1, 3], [2, 6], [8, 10], [15, 18]])
    # opt = Solution().merge([[1, 4], [4, 5]])
    # opt = Solution().minDistance(word1="horse", word2="ros")
    # opt = Solution().minDistance(word1="intention", word2="execution")
    # opt = Solution().minDistance(word1="zoologicoarchaeologist", word2="zoopsychologist")
    opt = Solution().minDistance(word1="abcdxabcde", word2="abcdeabcdx")
    # opt = Solution().singleNumbers(nums=[4, 1, 4, 6])
    # opt = Solution().singleNumbers(nums=[1, 2, 10, 4, 1, 4, 3, 3])
    # l1 = ListNode(1)
    # l1.next = ListNode(4)
    # l1.next.next = ListNode(5)
    # l2 = ListNode(1)
    # l2.next = ListNode(3)
    # l2.next.next = ListNode(5)
    # l3 = ListNode(2)
    # l3.next = ListNode(6)
    # lists = [l1, l2, l3]
    # opt = Solution().mergeKLists(lists=lists)
    print(opt)


if __name__ == '__main__':
    run()
