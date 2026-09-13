def main():
 try:
   a=int(input("Hey,Enter a number:"))
   print(a)
   return

 except Exception as e:
     print(e)
     return

 finally: 
   print("i am inside finally")

main()
     
