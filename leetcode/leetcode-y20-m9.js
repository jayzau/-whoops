/** D7: 347. 前 K 个高频元素
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
