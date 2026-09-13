def myFunc():
    print("hello world!")

myFunc()
print(__name__)


if __name__==" _main_":
   #if this code is executed by running the file its present in
 print("we are directly running this code")
 myFunc()
 print( __name__)