from sys import stdin
from random import randrange
from time import clock

from binary_search import binary_search_floor


def convex_hull(lines):
    """Finds the convex hull (lower envelope) of the lines.
    lines[i][0] is the intercept, and lines[i][1] the slope, of line i
    """

    # sort the lines first by slope, then by intercept
    lines.sort(key=lambda x: (x[1], -x[0]), reverse=True)

    # remove all redundant parallel lines,
    # only keeping ones with lower intercept
    relevant_lines = []
    relevant_lines.append(lines[0])
    for i in range(1, len(lines)):
        if lines[i][1] != lines[i - 1][1]:
            relevant_lines.append(lines[i])

    if len(relevant_lines) == 1:
        return relevant_lines, [-float('inf'), float('inf')]

    # pop the top line off the stack as long as it's irrelevant
    # come the new one, then append the new one
    relevant_lines_final = [relevant_lines[0], relevant_lines[1]]
    for i in range(2, len(relevant_lines)):
        a0, a1 = relevant_lines_final[-2]
        b0, b1 = relevant_lines_final[-1]
        c0, c1 = relevant_lines[i]
        while True:
            if (a0 - c0) / (c1 - a1) <= (a0 - b0) / (b1 - a1):
                relevant_lines_final.pop()
                if len(relevant_lines_final) < 2:
                    relevant_lines_final.append(relevant_lines[i])
                    break
                else:
                    a0, a1 = relevant_lines_final[-2]
                    b0, b1 = relevant_lines_final[-1]
            else:
                relevant_lines_final.append(relevant_lines[i])
                break

    # find the vertices of the hull; the left-most and right-most vertices
    # are of course always -infinity and +infinity
    vertices = []
    vertices.append(-float('inf'))
    for i in range(1, len(relevant_lines_final)):
        a0, a1 = relevant_lines_final[i - 1]
        b0, b1 = relevant_lines_final[i]
        vertices.append((a0 - b0) / (b1 - a1))
    vertices.append(float('inf'))

    return relevant_lines_final, vertices


def min_val(x, relevant_lines, vertices):
    """Finds the minimum value of all lines at the given value x."""
    
    i = binary_search_floor(x, vertices)
    return relevant_lines[i][0] + relevant_lines[i][1] * x


if __name__ == '__main__':
    n = 1000000
    lines = [[randrange(100), randrange(100)] for _ in range(n)]
    x = randrange(-50, 50)

    relevant_lines, vertices = convex_hull(lines)

    t0 = clock()

    ans_fast = min_val(x, relevant_lines, vertices)

    t1 = clock()

    ans_brute = float('inf')
    for i in range(n):
        curr_val = lines[i][0] + lines[i][1] * x
        if curr_val < ans_brute:
            ans_brute = curr_val

    t2 = clock()

    print('fast answer:', ans_fast)
    print('brute answer:', ans_brute)
    print('\n')
    print('fast time:', t1 - t0)
    print('brute time:', t2 - t1)
