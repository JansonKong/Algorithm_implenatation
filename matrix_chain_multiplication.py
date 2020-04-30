# -*- coding: UTF-8 -*-

"""
Copyright:SCUT
Author:kjs
Date:2020/4/30
Description: Solution for matrix chain multiplication problem.
"""


def init_state(num):
    state = [[float("inf") for i in range(num)] for i in range(num)]
    return state


def matrix_chain(pos, s, p, i, j):
    if s[i][j] < float("inf"):
        return s[i][j]

    if i == j:
        return 0

    min = float("inf")
    for k in range(i, j):
        temp = matrix_chain(pos, s, p, i, k) + matrix_chain(pos, s, p, k+1, j) + p[i-1]*p[k]*p[j]
        if temp < min:
            min = temp
            pos[i][j] = k
    s[i][j] = min
    return min


# Print the result
def print_partition(s, i, j):
  if i == j:
    print('A'+str(i), end='')
  else:
      print('(', end='')
      print_partition(s, i, s[i][j])
      print_partition(s, s[i][j]+1, j)
      print(')', end='')

if __name__ == '__main__':
    # p = [30, 35, 15]
    p = [30, 35, 15, 5, 10, 20, 25]

    s = init_state(len(p))
    pos = init_state(len(p))

    print(matrix_chain(pos, s, p, 1, len(p)-1))
    print_partition(pos, 1, len(p)-1)



