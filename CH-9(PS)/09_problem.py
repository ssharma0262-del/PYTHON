with open("file.txt") as f:
    content1 = f.read()

with open("this_copy.txt") as f:
  content2 = f.read()
if (content1==content2):
    print(" yes these files are identical")
else:
  print ("no these files are not identical")