#make_lab_file.py

#takes in folder with textgrid files, outputs lab files with text
#encoded in utf-8

# TODO: 
#	- if dictionary already exists, merge with existing one

import codecs
import re
from glob import glob
from os import makedirs
from os.path import exists
from subprocess import call

# extracts text from a textgrid file given the file name, file encoding, and the tier
# on which the text is found
def extract_textgrid(filename, utf8, tiernum):

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


# extract text lines from eaf file given the file name
def extract_eaf(filename, tierid):

	textlist = []

	with codecs.open(filename, 'r', 'utf-8') as f:
		myList = f.readlines()
		
	f.close()
	
	tierstring = "TIER_ID=\"" + tierid + "\""
	
	# start index
	for x in myList:
		if tierstring in x:
			tierindex = myList.index(x)
	
	size = len(myList)
	endindex = size
	
	# end index
	for y in range (tierindex, size):
		if "</TIER>" in myList[y]:
			endindex = y
			break;

	tmplist = []
	
	for z in range (tierindex, endindex):
		if "<ANNOTATION_VALUE>" in myList[z]:
			tmplist.append(myList[z])
	

	for item in tmplist:
		if "<ANNOTATION_VALUE></ANNOTATION_VALUE>" not in item:
			tmp_tuple = item.partition('<ANNOTATION_VALUE>')
			tmp_string = tmp_tuple[2]
			another_tuple = tmp_string.partition('</ANNOTATION_VALUE>')
			final_string = another_tuple[0]
			textlist.append(final_string)
	
	return textlist

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

menu = True

while menu == True:

	print"""
What kind of files would you like to convert to .lab files? Please enter the number
for your selection:

1. .TextGrid
2. .eaf
3. quit
"""

	filetype = raw_input("> ")
	
	if filetype == "1":
		print"""
You have selected .TextGrid files to convert.
Please make sure all TextGrid files in this directory have the same encoding, either
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

		print """
Enter the tier number for your line of text in your TextGrid files.
If you don't know what tier it is, open up your file in praat, and find the number
to the left of your tier.
Please note: this script only works if all TextGrid files in the directory have the same tier
number for the line of text you want to extract.
"""
		tierid = raw_input("> ")
		
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

		# for each textgrid file, make a .lab file and save the textgrid to a separate folder
		for file in file_list:

			# textgrid files
			if ".TextGrid" in file:
	
				# extract line of text we need
				textline = extract_textgrid(file, utf8, tierid)
		
				# move the TextGrid file to a directory for the old files
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

		
	
	elif filetype == "2":
		print"""
You have selected .eaf files to convert.
Enter the TIER_ID for your list of phrases. If you don't know what it is, open your .eaf
file in a text editing program and search for TIER_ID. There will be several TIERS with different
IDs, make sure you select the tier that lists your entire phrase in the notation you want."""

		tierid = raw_input("> ")

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
Default is: 0_old_file_eaf/
Press enter to use default"""

		olddir = raw_input("> ")
		if olddir == '':
			olddir = "0_old_file_eaf/"
		if olddir[-1] != '/':
			olddir = olddir + "/"

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

		# for each eaf file, make all possible .lab files and save eaf to a separate folder
		for file in file_list:

			# textgrid files
			if ".eaf" in file:
	
				# extract all the lines of text needed
				textlist = extract_eaf(file, tierid)
				
				# move eaf file to a directory for the old files
				call(["mv", file, filedir + olddir])
		
				#create all files necessary with lines of text from list
				for text in textlist:
					filename = filedir + text.replace(" ", "_") + ".lab"
					newfile = codecs.open(filename, 'w', 'utf-8')
					newfile.write(text)
					newfile.close()
					
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


	elif filetype == "3":
		print("quit.")
		menu = False
	
	else:
		print("Incorrect input. Try again.")



