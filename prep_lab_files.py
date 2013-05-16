#make_lab_file.py

#takes in folder with textgrid files, outputs lab files with text
#encoded in utf-8

import codecs
import re
from glob import glob
from os import makedirs
from os.path import exists
from subprocess import call

# extracts text from a textgrid file given the file name, file encoding, and the tier
# on which the text is found
def extract_text(filename, utf8, tiernum):

	if utf8 == False:
		with codecs.open(filename, 'r', 'utf-16') as f:
			myList = f.readlines()
	elif utf8 == True:
		with codecs.open(filename, 'r', 'utf-8') as f:
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

# creates a .lab file with the text from the textgrid file given the original file
# and the line of text
def create_file(file, textline):
	
	newfilename = file.replace(".TextGrid", ".lab")
	newfile = codecs.open(newfilename, 'w', 'utf-8')
	newfile.write(textline)
	newfile.close()
	
	return newfile

# extracts individual words from lab list and puts into list
def extract_word(file, list):

	f = codecs.open(file, "r", "utf-8")
	string = f.readline()
	
	newlist = string.rsplit(" ")
	
	for word in newlist:
		list.append(word)
		
	f.close()

	return list

# eliminates duplicates, taken from get_german_dict.py code
def no_copies(data):
	"""Eliminates identical entries in a list."""
	data_new = []; prev = None
	for line in data:
		if prev is not None and not line == prev:
			data_new.append(prev)
		prev = line
	return data_new


# on same line as each word, add its pronunciation
def add_pronunciation(words):

	new_words = []

	for item in words:
		list_string = list(item)
		for character in list_string:
			item = item + " " + character
		new_words.append(item)

	return new_words



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
Please make sure all files in this directory have the same encoding, either
UTF-8 or UTF-16. If you have both types in your directory, split them into 
two sub-directories and run this script for both of them.
Are the files in this directory UTF-8 or UTF-16? Enter 8 for UTF-8 and 16 for UTF-16.
"""
type = raw_input("> ")
if type == '8':
	utf8 = True
elif type == '16':
	utf8 = False
else: print("incorrect input. run script again.")

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

# for each file, make a .lab file and save the textgrid to a separate folder
for file in file_list:
	if ".TextGrid" in file:
	
		#extract line of text we need
		textline = extract_text(file, utf8, tiernum)
		
		#move the TextGrid file to a directory for the old files
		call(["mv", file, filedir + olddir])
		
		#create a new file with line of text
		newfile = create_file(file, textline)
		
# make a dictionary using the lab files just created

# updated list of files
lab_list = glob(filedir+"*")

dictionary_list = []

# for each file, get words from file and 
for file in lab_list:
	if ".lab" in file:
		
		#extract each word in file, put into dictionary list
		dictionary_list = extract_word(file, dictionary_list)
		
# sort list
sorted_words = sorted(dictionary_list)
		
# remove duplicates
unique_words = no_copies(sorted_words)

# make pronunciations
words_pronounced = add_pronunciation(unique_words)
		
# put list into a dictionary text file	
dictionary_file = codecs.open(filedir + "/dictionary.txt", 'w', 'utf-8')

for word in words_pronounced:
	dictionary_file.write(word)
	dictionary_file.write("\n")

dictionary_file.close()














