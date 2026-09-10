class Employee:
    company="ITC"
    name="default name"
    def show(self):
        print(f"the name of the employee is {self.name} and the company is {self.company}")
class Coder:
    language="Python"
    def printLanguages(self):
        print(f"Out of all these languages here your language:{self.language}")
# class Programmer:
#     company="ITC Infotech"
#     def show(self):
#         print(f"the name is {self.name} and the salary is{self.salary} ")

#     def showLanguage(self):
#         print(f"The name is {self.name} and he is good in language{self.language} language")
class Programmer(Employee,Coder):
    company="ITC Infotech"
    def showLanguage(self):
        print(f"The name is {self.company} and he is good in language{self.language} language")

a=Employee()
b=Programmer()

b.show()
b.showLanguage()
b.printLanguages()