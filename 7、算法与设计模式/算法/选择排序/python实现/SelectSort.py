# coding:utf-8

import random

def SelectSort(num):
    for i in range(0,len(num)):
        mindex=i
        for j in range(i,len(num)):
            if num[mindex]>num[j]:
                mindex=j
        num[mindex],num[i]=num[i],num[mindex]
    return num


a = SelectSort([3,5,4,7,8,1,2])
print a
