#filter problem
def divisible5(n):
    if(n%5==0):
        return True
    return False

a=[1,2,33345,45,31441,413143,45,567,78,98]
f=list(filter(divisible5,a))
print(f)