class Employee:
    language="python"#this is a class attrubute
    salary=1200000
    def getInfo(self):
        print(f"The language is{self.language}.The salary is{self.salary}")
    def greet(self):
        print("Good morning")
Aniket=Employee()
# Aniket.language="javascript"#this is an object attribute
Aniket.getInfo()
Aniket.greet()

