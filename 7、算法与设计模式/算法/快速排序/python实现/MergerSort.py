# coding:utf-8

import random

def MergerSort(num):
    if len(num)<=1:
        return num
    left=MergerSort(num[:len(num)/2])
    right=MergerSort(num[len(num)/2:])
    result=[]
    while len(left)>0 and len(right)>0:
        if left[0]>right[0]:
            result.append(right.pop(0))
        else:
            result.append(left.pop(0))
    return result



a = MergerSort([3,5,4,7,8,1,2])
print a
