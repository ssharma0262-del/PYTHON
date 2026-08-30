a=int(input("Enter your age"))
#if statement no:1
if(a%2==0):
    print("a is even")
  #end of if statment no:1
    #if statement no:2
if(a>=18):
    print("you are above the age of consent")
    print("Good for you")

elif(a<0):
    print("You are entering an invalid age")

else:
    print("you are below the age of consent")

#end of if statement no:2
print("end of program")