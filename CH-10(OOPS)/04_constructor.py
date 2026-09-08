class Employee: 
    language = "Python" # This is a class attribute
    salary = 1200000

    def __init__(self,name,salary,language): # dunder method which is automatically called
        self.name=name
        self.salary=salary
        self.language=language
        print("I am creating an object")
 
 
    def getInfo(self):
        print(f"The language is {self.language}. The salary is {self.salary}")

    @staticmethod
    def greet():
        print("Good morning")


Aniket = Employee("Aniket",130000,"javascript") 
# Aniket.name = "Harry"
print(Aniket.name, Aniket.salary ,Aniket.language)

