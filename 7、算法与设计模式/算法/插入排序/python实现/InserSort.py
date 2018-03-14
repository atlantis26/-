# coding:utf-8

import random

def InserSort(num):
    for i in range(1,len(num)):
        j=i-1
        tmp=num[i]
        while j>=0 and tmp<num[j]:
            num[j+1]=num[j]
            j-=1
        num[j]=tmp
    return num


a = InserSort([3,5,4,7,8,1,2])
print a
