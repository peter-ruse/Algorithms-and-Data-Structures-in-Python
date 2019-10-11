from sys import stdin


def max_subarray(a, n):
    """Finds the maximum sum subarray as well as the start and end indices of one such subarray."""
    max_so_far = -float('inf')
    max_ending_here = 0
    start = 0
    end = 0
    start_temp = 0
    for i in range(n):
        max_ending_here += a[i]
        if max_so_far < max_ending_here:
            max_so_far = max_ending_here
            start = start_temp
            end = i
        if max_ending_here < 0:
            max_ending_here = 0
            start_temp = i + 1
    return max_so_far, start, end


def max_subarray_1d(a, n):
    """Finds the max sum subarray, without locating a subarray that achieves it"""
    max_so_far = a[0]
    curr_max = a[0]
    for i in range(1, n):
        curr_max = max(a[i], curr_max + a[i])
        max_so_far = max(max_so_far, curr_max)
    return max_so_far


def max_subarray_2d(a, n, m):
    """Finds the max sum subarray of a 2-d array, along with the corners of one such subarray."""
    max_sum = -float('inf')
    for l in range(m):
        row_sums = [0] * n
        for r in range(l, m):
            for i in range(n):
                row_sums[i] += a[i][r]
            max_sum_temp, row_top_temp, row_bottom_temp = max_subarray(row_sums, n)
            if max_sum_temp > max_sum:
                max_sum = max_sum_temp
                row_top = row_top_temp
                row_bottom = row_bottom_temp
                col_left = l
                col_right = r
    return max_sum, row_top, row_bottom, col_left, col_right


if __name__ == '__main__':
    a = [[1, 2, -1, -4, -20],
        [-8, -3, 4, 2, 1],
        [3, 8, 10, 1, 3],
        [-4, -1, 1, 7, -6]]
    print(max_subarray_2d(a, 4, 5))
