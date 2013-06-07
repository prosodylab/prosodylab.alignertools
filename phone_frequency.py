# Calculate the frequency of a set of phones, provided a dictionary and a set of .lab
# files.

import codecs
from glob import glob
from sys import exit

def dirclean(string):
	"""Clean raw input strings so that they are readable as directories."""
	if string[-1]==" ":
		string = string.replace(" ","")
	if string[-1]!="/":
		string = string + "/"
	return string

def parse(string, sep):
	"""Parse a string into a list."""
	# remove leading and trailing sep's
	if string[0] == sep:
		string = string[1:]
	if string[-1] == sep:
		string = string[:-1]
	id_list = []
	while string is not "":
		if sep not in string:
			id_list.append(string)
			string = ""
		else:
			index = string.index(sep)
			newstring = string[:index]
			id_list.append(newstring)
			string = string[index+1:]
	return id_list

def find_replace(text, list):
	"""Finds and replaces characters given in a string.
	Characters to be replaced must be given as a list of ordered pairs."""
	for pair in list:
		if pair[0] in text:
			text = text.replace(pair[0], pair[1])
	return text

# Define user form
print "\nphone_frequency.py"
print """
What is the dictionary file that you want to use?
You can drag and drop it into the Terminal window below.
Press enter to use the dictionary stored in the 
most current version of the aligner."""
dictionary = raw_input("> ")
if dictionary[-1] == " ":
	dictionary = dictionary.replace(" ","")
if dictionary == "":
	dictionary = "/Applications/Prosodylab-Aligner-v1/dictionary.txt"
print"""
Which set of .lab files are you using to calculate the
frequency? You can drag and drop it into the Terminal
window below."""
labdir = raw_input("> ")
labdir = dirclean(labdir)

mod = False

# Open dictionary
d = codecs.open(dictionary, 'r', 'utf-8')

# Parse dictionary
dlist = []
for line in d:
	line = line.replace("\n","")
	newline = parse(line," ")
	dlist.append(newline)
d.close()

# Make phone-only dictionary
phonedict = []
for line in dlist:
	phonedict.append(line[1:])

# Get list of unique phones
phonelist = []
for line in phonedict:
	for phone in line:
		if phone not in phonelist:
			phonelist.append(phone)
phonelist.sort()

# Make a counter list
countlist = []
for phone in phonelist:
	countlist.append([phone, 0])
countlist.append(['Total', 0])

# Make list of .lab files
lab_list = glob(labdir + '*.lab')

for file in lab_list:
	# Read in text and parse into words
	f = codecs.open(file, 'r', 'utf-8')
	txt = f.read(); f.close()
	txt = find_replace(txt, [['\n',''],[' \t',''],['\t','']])
	wordlist = parse(txt," ")
	
	# Read words in as phones
	wordchoice = []
	for word in wordlist:
		for entry in dlist:
			if word == entry[0]:
				if entry[-1] == '':
					entry = entry[:-1]
				wordchoice.append(entry)
	
	# pick the first entry if there are duplicates (not elegant)
	uniquewords = []; prev_line = [None]
	for word in wordchoice:
		if prev_line[0] != word[0]:
			uniquewords.append(word)
		prev_line = word

	# if a word is missing, add its pronunciation
	if len(uniquewords) != len(wordlist):
		# get words in uniquewords
		uwords = []
		for word in uniquewords:
			uwords.append(word[0])
			
		for word in wordlist:
			if word not in uwords:
				print "\nThe word %s is missing from the dictionary." % word
				print "Please provide its pronunciation below."
				print "Each phoneme must be separated by a space."
				phonestring = raw_input("> ")
				parsed_string = parse(phonestring, " ")
				# Make a new entry & append
				new_entry = []; new_entry.append(word)
				for phone in parsed_string:
					new_entry.append(phone)
				uniquewords.append(new_entry)
				dlist.append(new_entry)
				mod = True
	
	# read only the phones
	phones = []
	for word in uniquewords:
		onlyphones = word[1:]
		for phone in onlyphones:
			phones.append(phone)
	phonecount = len(phones)
	countlist[-1][1] = countlist[-1][1] + phonecount
	
	# Count phones
	for phone in phones:
		for ppair in countlist:
			if phone == ppair[0]:
				ppair[1] = ppair[1] + 1

# Store phonelist in a new file
countfile = open("phone_count.txt", "w")
for pair in countlist:
	textline = pair[0] + '\t' + str(pair[1]) + '\n'
	countfile.write(textline)
countfile.close()

# Store dictionary
if mod == True:
	dlist.sort()
	newdict = open("new_dictionary.txt", "w")
	for line in dlist:
		textline = None
		for item in line:
			if textline == None:
				textline = item
			else:
				textline = textline + ' ' + item
		textline = textline + '\n'
		textline = textline.encode('utf-8')
		newdict.write(textline)
	newdict.close()