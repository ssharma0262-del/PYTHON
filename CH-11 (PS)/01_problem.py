class TwoDvector:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def show(self):
        print(f"the vector is{self.x}x + {self.y}y")

class ThreeDvector(TwoDvector):
    def __init__(self, x, y,z):
        super().__init__(x, y)
        self.z=z
    def show(self):
        print(f"the vector is {self.x}x+{self.y}y+{self.z}z")

a=TwoDvector(1,2)
a.show()
b=ThreeDvector(1,2,3)
b.show()

