# f=open("poem.txt","r")
# data=f.read()
# print(data)
# f.close()

with open("poem.txt") as f:
    print(f.read())