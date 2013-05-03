# clean_labfile.py

# This script will clean lab files such that they are readable by the Prosodylab Aligner.
# Currently works for English, French, and German lab files
# Erin Olson erin.daphne.olson@gmail.com
# Current Date: 2013/05/03

import glob
import codecs
from shutil import move
from os import makedirs
from os.path import exists

def find_replace(text, list):
	"""Finds and replaces characters given in a string.
	Characters to be replaced must be given as a list of ordered pairs."""
	for pair in list:
		if pair[0] in text:
			text = text.replace(pair[0], pair[1])
	return text

# form
print "clean_labfile\n"
print "What language is the data in?"
lang = raw_input("> ")
if lang not in ["English", "english", "French", "french", "German", "german"]:
	exit("""Sorry, this language is not currently supported!
A list of supported languages can be found below:
- English
- French
- German""")
print """
What is the file directory?
You can drag and drop the file into the Terminal window to fill out this space"""
filedir = raw_input("> ")
if filedir[-1] == ' ':
	filedir = filedir.replace(' ', '')
if filedir[-1] != "/":
	filedir = filedir + "/"
print """
What would you like to call the directory for old lab files?
Default is: 0_old_labfile_clean/
Press enter to use default"""
olddir = raw_input("> ")
if olddir == '':
	olddir = "0_old_labfile_clean/"
if olddir[-1] != "/":
	olddir = olddir + "/"

# check to see if the old lab file directory exits; make if not
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

# set punctuation list (universal)
pun_list = [[u'\xab', ''], [u'\xbb', ''], ['\"', ''], ["-", ''], ["?", ''], ["!", ''], 
[',', ''], ['.', ''], [':', ''], [';', ''], ['\t', ' '], ['\n', ''], [u'\xa0', ' '], ['  ', ' '],
['[',''],[']',''], ['(',''], [')','']]

# select language-specific character replacement list
if lang == "French" or lang == "french":
	char_list = [["s'", "s "], ["S'", "S "], ["c'", "c "], ["C'", "C "], ["d'", u"d "], 
	["D'", "D "], ["l'", "l "], ["L'", "L "], ["n'", "n "], ["N'", "N "], ["qu'", "qu "], 
	["Qu'", "Qu "], ["j'", "j "], ["J'", "J "], ["t'", "t "], ["T'", "T "], ["m'", "m "], 
	["Y'", "Y "], ["y'", "y "],["M'", "M "], ["jusqu'", "jusqu "], ["Jusqu'", "Jusqu "],  
	['0', 'zero '], ['1', 'un '], ['2', 'deux '],['3', 'trois '], ['4', 'quatre '], 
	['5', 'cinq '], ['6', 'six '], ['7', 'sept '], ['8', 'huit '], ['9', 'neuf '], 
	['&', 'et'], ['\'', '']]
elif lang == "German" or lang == "german":
	char_list = [['0', 'zero '], ['1', 'ein '], ['2', 'zwei '], ['3', 'drei '],
	['4', 'vier '], ['5', 'fuenf '], ['6', 'sechs '], ['7', 'sieben '], ['8', 'acht '],
	['9', 'neun '], ['&', 'und']]
elif lang == "English" or lang == "english":
	char_list = [['0', 'zero '], ['1', 'one '], ['2', 'two '], ['3', 'three '], ['4', 'four '],
	['5', 'five '], ['6', 'six '], ['7', 'seven '], ['8', 'eight '], ['9', 'nine '], 
	['&', 'and'], ['\'', ''], ['%', 'percent']]
else:
	char_list = None
	
# append lists:
rep_list = char_list; rep_list.extend(pun_list)

# make a list of all of the relevant files
lab_list = glob.glob(filedir + '*.lab')

for file in lab_list:
	f = codecs.open(file, 'r', 'utf-8')
	txt = f.read(); f.close()
	txtnew = find_replace(txt, rep_list)
	
	# make upper or lowercase:
	if lang == "English" or lang == "english":
		txtnew = txtnew.upper()
	else:
		txtnew = txtnew.lower()
	
	txtnew = txtnew.encode('utf-8')
	
	# make a useful name for the lab file; move old file
	filename = file.replace(filedir, '')
	move(file, filedir + olddir + filename)
	
	# make a new file
	filenew = open(filedir + filename, 'w')
	filenew.write(txtnew)
	filenew.close()