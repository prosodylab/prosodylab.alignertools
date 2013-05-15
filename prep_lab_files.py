#make_lab_file.py

#takes in folder with textgrid files, outputs lab files with text
#encoded in utf-8

import codecs
import re
from glob import glob
from os import makedirs
from os.path import exists
from subprocess import call

def extract_text(filename, tiernum):

	with codecs.open(filename, 'r', 'utf-16') as f:
		myList = f.readlines()
	
	f.close()
	
	size = len(myList)
	
	tierstring = "item [" + tiernum + "]:"
	
	for x in myList:
		if tierstring in x:
			tierindex = myList.index(x) 
			
	for y in range (tierindex, size):
		if "text" in myList[y]:
			textindex = y
			break;
		
	textline = myList[textindex]
	
	tmp = re.search('\"(.+?)\"', textline)
	if tmp:
		text = tmp.group(1)
	
	return text
	
def create_file(file, textline):
	
	newfilename = file.replace(".TextGrid", ".lab")
	newfile = codecs.open(newfilename, 'w', 'utf-8')
	newfile.write(textline)
	newfile.close()
	
	return newfile

#test to create lab file first

#form
print"""
What is the file directory?
You can drag and drop the files into the Terminal window to fill out this space
WARNING: No individual directory should have a space character
If so, please go back and replace any spaces with underscores
"""
filedir = raw_input("> ")
if filedir[-1] == ' ':
	filedir = filedir.replace(" ", '')
if filedir[-1] != '/':
	filedir = filedir + '/'

print"""
What would you like to call the directory for old files?
Default is: 0_old_file_textgrid/
Press enter to use default"""
olddir = raw_input("> ")
if olddir == '':
	olddir = "0_old_file_textgrid/"
if olddir[-1] != '/':
	olddir = olddir + "/"


print """
Enter the tier number for your line of text in your textgrid file.
If you don't know what tier it is, open up your file in praat, and find the number
to the left of your tier.
Please note: this script only works if all files in the directory have the same tier
number for the line of text you want to extract.
"""
tiernum = raw_input("> ")
	
# check for directory & make a new one
goodname = False
while goodname == False:
	if exists(filedir + olddir):
		print "Directory already exists!\nPlease pick a new directory name for old labfiles:"
		olddir = raw_input("> ")
		if olddir[-1] != '/':
			olddir = olddir + '/'
	else:
		goodname = True
makedirs(filedir + olddir)

# make a list of the files
file_list = glob(filedir+"*")

for file in file_list:
	if ".TextGrid" in file:
	
		#extract line of text we need
		textline = extract_text(file, tiernum)
		
		#move the TextGrid file to a directory for the old files
		call(["mv", file, filedir + olddir])
		
		#create a new file with line of text
		newfile = create_file(file, textline)
		

