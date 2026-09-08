class Programmer:
    company="Microsoft"
    def __init__(self,name,salary,pincode ):
        self.name=name
        self.salary=salary
        self.pincode=pincode

p=Programmer("Aniket",120000,400701)
r=Programmer("Rohan",99999,400701)
print(p.name,p.salary,p.pincode,p.company)
print(r.name,r.salary,r.pincode,r.company)