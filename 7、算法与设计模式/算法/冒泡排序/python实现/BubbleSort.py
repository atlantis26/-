# coding:utf-8

import random

def BubbleSort(num):
    n = len(num)
    for i in range(0,n):
        for j in range(i,n):
            print i,j
            if num[i]>=num[j]:
                num[i],num[j]=num[j],num[i]
    return num

a = BubbleSort([3,5,4,7,8,1,2])
print a
