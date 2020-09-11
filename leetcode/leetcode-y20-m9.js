// ------------------------------------------------------------------------
// ----------------------- D1: 486. 预测赢家--------------------------------N
/**
 * @param {number[]} nums
 * @return {boolean}
 */
var PredictTheWinner = function(nums) {
    // 评论区说动态规划，我不会
};

// ------------------------------------------------------------------------
// ----------------------- D2: 剑指 Offer 20. 表示数值的字符串----------------
/**
 * @param {string} s
 * @return {boolean}
 */
var isNumber = function(s) {
    var v = s * 1;
    return v === 0 ? s.indexOf("0") > -1 : !isNaN(v)
};

// ------------------------------------------------------------------------
// ----------------------- D3: 51. N 皇后-----------------------------------
/**
 * @param {number} n
 * @return {string[][]}
 */
var solveNQueens = function(n) {
    var resp = new Array();
    function place(arr, x) {
        var lock = {y: [], l: [], r:[]};
        for (var i=0;i<x;i++){
            lock.y.push(arr[i]);
            lock.l.push(i + arr[i]);
            lock.r.push(i - arr[i]);
        }
        for (var y=0;y<n;y++){
            var l = y + x;
            var r = x - y;
            if (lock.y.indexOf(y) === -1 && lock.l.indexOf(l) === -1 && lock.r.indexOf(r) === -1){
                var local_arr = arr.slice();
                local_arr[x] = y;
                if (x + 1 === n) {
                    var queens = new Array(n);
                    for (var index=0;index<n;index++){
                        var board = new Array(n).fill(".");
                        board[local_arr[index]] = "Q";
                        queens[index] = board.join("");
                    }
                    resp.push(queens)
                } else {
                    place(local_arr, x + 1)
                }
            }
        }
    }
    place(new Array(n), 0);
    return resp
};

// ------------------------------------------------------------------------
// ----------------------- D7: 347. 前 K 个高频元素--------------------------
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number[]}
 */
var topKFrequent = function(nums, k) {
    var obj = {};
    nums.forEach(function (num) {
        obj[num] ? obj[num]++ : obj[num]=1
    });
    var arr = [];
    for (var key in obj) {
        arr.push({value: key, count: obj[key]})
    }
    arr.sort(function(x, y){
        return y.count - x.count
    });
    var result = [];
    for (var i=0; i<k; i++) {
        result.push(arr[i].value * 1)
    }
    return result
};

// ------------------------------------------------------------------------
// --------------------------- D8: 77. 组合--------------------------------
/**
 * @param {number} n
 * @param {number} k
 * @return {number[][]}
 * n=8, k=3
 * k=3:   1,   2,   3,   4,   5,   6,    7,  [8]   |    8 .................. 7 .....
 * k=2:   1,   2,   3,   4,   5,   6,   [7]        |    7    6  ...  2       6    5
 * k=1: [[1], [2], [3], [4], [5], [6]]             |   6-1  5-1      1      5-1  4-1
 */
var combine = function(n, k) {
    var arr = new Array();
    if (k === 1) {
        for (var i=n;i>0;i--) {
            arr.push([i])
        }
        return arr
    }
    for (var i=n;i>0;i--) {
        arr.push(i)
    }
    var result = new Array();
    for (var index=0;index<=n-k;index++){
        var next_result = combine(n - index - 1, k - 1);
        next_result.forEach(function(next_arr){
            next_arr.push(arr[index])
            result.push(next_arr)
        })
    }
    return result
};

// ------------------------------------------------------------------------
// --------------------------- D9: 39. 组合总和-----------------------------
/**
 * @param {number[]} candidates
 * @param {number} target
 * @return {number[][]}
 */
var combinationSum = function(candidates, target) {
    var newCandidates = candidates.filter(function(x){
        return x<=target
    });
    var results = [];
    newCandidates.forEach(function(num, index){
        var difference = target - num;
        if (difference > 0){
            var _results = combinationSum(newCandidates.slice(index), difference);
            _results.forEach(function(_result){
                _result.push(num);
                results.push(_result)
            })
        }
        if (difference === 0){
            results.push([num])
        }
    });
    return results
};

// ------------------------------------------------------------------------
// --------------------------- D10: 40. 组合总和 II-------------------------
// --------------------------- 在 D9 上加了个去重.. -------------------------
/**
 * @param {number[]} candidates
 * @param {number} target
 * @return {number[][]}
 */
var combinationSum2 = function(candidates, target) {
    var newCandidates = candidates.filter(function(x){
        return x<=target
    });
    var results = [];
    var results_str = [];
    newCandidates.forEach(function(num, index){
        var difference = target - num;
        if (difference > 0){
            var _results = combinationSum2(newCandidates.slice(index + 1), difference);
            _results.forEach(function(_result){
                _result.push(num);
                _result.sort();
                var _result_str = _result.toString();
                if (results_str.indexOf(_result_str) === -1){
                    results_str.push(_result_str);
                    results.push(_result)
                }
            })
        }
        if (difference === 0){
            var _result = [num];
            var _result_str = _result.toString();
            if (results_str.indexOf(_result_str) === -1){
                results_str.push(_result_str);
                results.push(_result)
            }
        }
    });
    return results
};

// ------------------------------------------------------------------------
// --------------------------- D11: 216. 组合总和 III-----------------------
/**
 * @param {number} k
 * @param {number} n
 * @return {number[][]}
 */
var combinationSum3 = function(k, n) {
    const nums = [1,2,3,4,5,6,7,8,9];
    let current = [];
    const result = [];
    const set = new Set();
    const bt = (index, rest, target) => {
        if(rest === 0 && target !== 0 || index > nums.length) {
            return;
        }

        if(rest === 0 && target === 0) {
            const currentSetItem = current.slice().sort((a, b) => a - b).join('|');
            if(!set.has(currentSetItem)) {
                result.push(current.slice());
                set.add(currentSetItem);
            }
            return;
        }

        current.push(nums[index]);
        bt(index + 1, k - current.length, target - nums[index]);
        current.pop();
        bt(index + 1, k - current.length, target);
    };

    bt(0, k, n);
    return result;
};
