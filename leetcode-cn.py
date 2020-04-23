"""
随缘刷题
"""
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        """1248. 统计「优美子数组」"""
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
        """199. 二叉树的右视图"""
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
        """22. 括号生成"""
        result = []
        if not n:
            return result
        data = [1 for _ in range(n)] + [-1 for _ in range(n)]       # ( 转换为 1   ) 转换为 -1
        rst = [1]           # 完整括号肯定由 ( 开头
        data.remove(1)
        lst = [(rst, data)]
        while lst:
            lst_bak = []
            for (_rst, _data) in lst:
                for i in [1, -1]:           # 依次取出  (  )
                    if i not in _data:
                        continue
                    _rst_bak = _rst[:]
                    _rst_bak.append(i)
                    if sum(_rst_bak) < 0:       # 相加 小于0说明 ) 多了
                        continue
                    _data_bak = _data[:]
                    _data_bak.remove(i)
                    if _data_bak:
                        lst_bak.append((_rst_bak, _data_bak))
                    else:
                        result.append(_rst_bak)
            lst = lst_bak[:]
        return ["".join(["(" if i == 1 else ")" for i in each]) for each in result]     # 数字转化成()


if __name__ == '__main__':
    # opt = Solution().numberOfSubarrays([1, 1, 2, 1, 1], 3)
    # opt = Solution().numberOfSubarrays([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2)

    opt = Solution().generateParenthesis(11)
    print(opt)
    pass

