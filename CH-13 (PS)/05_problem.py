from functools import reduce
a=[1,2,33345,45,31441,413143,45,567,78,98]

def greater(a,b):
    if(a>b):
        return a
    return b

print(reduce(greater,a))