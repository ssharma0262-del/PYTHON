def greatest():
    a=int(input("enter a number:"))
    b=int(input("enter a number"))
    c=int(input("enter a number"))
    if(a>b and a>c):
        print("a is greater")
    else:
        print("a is not greater")

greatest()



def greatest(a,b,c):
    if(a>b and a>c):
        return a
    elif(b>a and b>c):
        return b
    elif(c>a and c>b):
        return c

a=1
b=2
c=3

print(greatest(a,b,c))