try:
    a=int(input("Enter a number:"))
    b=int(input("Enter b number:"))
    print(a/b)
except ZeroDivisionError as v:
    print("infinite")