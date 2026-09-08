
class Calculator:
    def __init__(self,n):
        self.n=n
    def square(self):
        print(f" The square of number is:{self.n*self.n}")
    def  Cube(self):
        print(f" The cube of number is:{self.n*self.n*self.n}")
    def Squareroot(self):
        print(f"The square root of number is:{self.n**1/2}")
    
a=Calculator(4)
a.square()
a.Cube()
a.Squareroot()