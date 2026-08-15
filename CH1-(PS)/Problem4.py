# write a python program to print the contents of a directory using the os module search online for the function which does that/Q5 label the 
# program with contents
import os
# select the directory whose content you want to list
directory_path = '/'
# use the os module to list the content of the directories

contents = os.listdir(directory_path)
# print the content of the directories
print(contents)