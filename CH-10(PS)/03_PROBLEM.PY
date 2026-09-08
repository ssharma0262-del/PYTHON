# class Demo:
#     a=4
# o=Demo()
# print(o.a)#prints the class attribute is not present
# o.a = 0 #instance attribute is set
# print(o.a)#prints the instance attribute because instance attribute is not present
# print(Demo.a)#prints the class attribute
class Demo:
    a=4
o=Demo()
print(o.a)
o.a=0
print(o.a)
print(Demo.a)