# relabel_clean.py
# relabel and clean lab files with menu options for ease
# uses code from relabel.py and clean_labfile.py 
# May 17, 2013

# from relabel.py:
# This script will take an experiment file and generate new lab files for
# all of the .wav files in a directory. Old .lab files, if present, are
# stored in a new directory called "0_old_labfiles"

# from clean_labfile.py:
# This script will clean lab files such that they are readable by the Prosodylab Aligner.
# Currently works for English, French, and German lab files

# TODO:
# 	- figure out more modularizations

# imports

import csv
import glob
import codecs
import re
from sys import exit
from shutil import move
from os import makedirs
from os.path import exists
from subprocess import call


# functions

def unicode_csv_reader(data, **kwargs):
	"""Enables all cells in a .csv file to be read as unicode strings."""
	data_file = csv.reader(data, **kwargs)
	for row in data_file:
		yield [unicode(cell, 'utf-8') for cell in row]

def parse(string, sep):
	"""Parse a string into a list."""
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

def indexer(list1, list2):
	"""Find the index of an object in list1 if it matches an object in list2"""
	index_list = []
	for x in list1:
		for y in list2:
			if x == y:
				index = list1.index(x)
				index_list.append(index)
	return index_list

def reader(list, index_list):
	"""Read in relevant data from a list using a list of indexes"""
	newlist = []
	for i in index_list:
		newlist.append(list[i])
	return newlist

def find_replace(text, list):
	"""Finds and replaces characters given in a string.
	Characters to be replaced must be given as a list of ordered pairs."""
	for pair in list:
		if pair[0] in text:
			text = text.replace(pair[0], pair[1])
	return text


def check_dir(filedir, olddir):
	goodname = False
	while goodname == False:
		if exists(filedir + olddir):
			print """Directory already exists!
Please pick a knew directory name for old lab files:"""
			olddir = raw_input("> ")
			if olddir[-1] != '/':
				olddir = olddir + '/'
		else:
			goodname = True
	return olddir

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
# change special chars to utf-8 encode
def add_pronunciation(words):

	new_words = []

	for item in words:
		list_string = list(item)
		for character in list_string:
			new_char = character.encode('unicode_escape')
			
			if '\\' in new_char:
				new_char = new_char.replace('\\', "")
			
			item = item + " " + new_char
		new_words.append(item)

	return new_words


# set replacement list for relabel
#	- regular punctuation (removed): . , ! ? : ; " / ellipsis(u2026) enter tab
#	- special quotations (removed): left-quotes(u201c) right-quotes(u201c) 
#		high-quotes(u201f) low-single-quote(u201a) low-quotes(u201e) double-prime(u2033)
#		angled-single-quotes(u2039 and u203a) angled-double-quotes(xab and xbb)
#	- unicode space (space): xa0
#	- single quotations ('): single-left-quote(u2018) single-right-quote(u2019) 
#		single-high-quote(u201b) prime(u2032)
#	- hyphens (-): soft-hypen(xad) en-dash(u2013) no-break(u2011) em-dash(u2014) figure(u2012)
replist =[[u".",u""], [u",",u""], [u"!",u""], [u"?",u""], [u":",u""], [u";",u""], 
	[u'"',u""], [u"/",u""], [u"\n",u""], [u"\\n",u""], [u"\t",u""], [u"\u2026",u""], 
	[u"\\", u""], [u"\u201c",u""], [u"\u201d",u""], [u"\u201f",u""], [u"\u201a",u""], 
	[u"\u201e",u""], [u"\u2033",u""], [u"\u2039",u""], [u"\u203a",u""], [u"\xab",u""], 
	[u"\xbb",u""], 	[u"\xa0",u" "], [u"\u2018",u"'"], [u"\u2019",u"'"], [u"\u201b",u"'"], 
	[u"\u2032",u"'"], [u"\xad",u"-"], [u"\u2013",u"-"],[u"\u2011",u"-"], [u"\u2014",u"-"], 
	[u"\u2012",u"-"]]
	
# replacement lists for clean_labfile
# set punctuation list (universal)
pun_list = [[u'\xab', ''], [u'\xbb', ''], ['\"', ''], ["-", ''], ["?", ''], ["!", ''], 
[',', ''], ['.', ''], [':', ''], [';', ''], ['\t', ' '], [' \n', ' '], ['\n', ' '],[u'\xa0', ' '], ['  ', ' '],
['[',''],[']',''], ['(',''], [')',''], [u'\u201e', '']]

# language-specific character replacement list
french_char_list = [["s'", "s "], ["S'", "S "], ["c'", "c "], ["C'", "C "], ["d'", u"d "], 
["D'", "D "], ["l'", "l "], ["L'", "L "], ["n'", "n "], ["N'", "N "], ["qu'", "qu "], 
["Qu'", "Qu "], ["j'", "j "], ["J'", "J "], ["t'", "t "], ["T'", "T "], ["m'", "m "], 
["Y'", "Y "], ["y'", "y "],["M'", "M "], ["jusqu'", "jusqu "], ["Jusqu'", "Jusqu "],  
['0', 'zero '], ['1', 'un '], ['2', 'deux '],['3', 'trois '], ['4', 'quatre '], 
['5', 'cinq '], ['6', 'six '], ['7', 'sept '], ['8', 'huit '], ['9', 'neuf '], 
['&', 'et'], ['\'', '']]

german_char_list = [['0', 'zero '], ['1', 'ein '], ['2', 'zwei '], ['3', 'drei '],
['4', 'vier '], ['5', 'fuenf '], ['6', 'sechs '], ['7', 'sieben '], ['8', 'acht '],
['9', 'neun '], ['&', 'und'], [u'\xdc','Ue'], [u'\xfc', 'ue'], [u'\xd6','Oe'], 
[u'\xf6', 'oe'], [u'\xc4','Ae'], [u'\xe4', 'ae'], [u'\xdf', 'ss']]

english_char_list = [['0', 'zero '], ['1', 'one '], ['2', 'two '], ['3', 'three '], ['4', 'four '],
['5', 'five '], ['6', 'six '], ['7', 'seven '], ['8', 'eight '], ['9', 'nine '], 
['&', 'and'], ['\'', ''], ['%', 'percent']]


# user form

menu = True

while menu == True:

	print"""
===== MENU =====
1. relabel files
2. clean files
3. a dictionary
4. quit

Please enter the number for the option you would like to select
	"""
	value = raw_input("> ")
	
	if value == "1":
		# run relabel script
		
		print """relabel\n
What are the experiment files? (must include directory)
You can drag and drop the files into the Terminal window to fill out this space
WARNING: No individual directory should include a space chacter
If so, please go back and replace any spaces with underscores"""
		exp_file_names = raw_input("> ")
		if exp_file_names[-1] == ' ':
			chars = list(exp_file_names)
			chars[-1] = ''
			exp_file_names = "".join(chars)
		print """
What are the id columns of the experiment file?
Default is: experiment_item_condition
Press enter to use default"""
		exp_string = unicode(raw_input("> "), 'utf-8')
		if exp_string == '':
			exp_string = "experiment_item_condition"
		print """
What is the sound directory?
You can drag and drop the file into the Terminal window to fill out this space"""
		sounddir = raw_input("> ")
		if sounddir[-1] == ' ':
			sounddir = sounddir.replace(" ", '')
		if sounddir[-1] != '/':
			sounddir = sounddir + '/'
		print """
What are the id columns of the sound file?
Default is: experiment_participant_item_condition
Press enter to use default"""
		sound_string = unicode(raw_input("> "), 'utf-8')
		if sound_string == '':
			sound_string = "experiment_participant_item_condition"
		print """
What would you like to call the directory for the old lab files?
Default is: 0_old_labfile_relabel/
Press enter to use default"""
		olddir = raw_input("> ")
		if olddir == '':
			olddir = "0_old_labfile_relabel/"
		if olddir[-1] != '/':
			olddir = olddir + "/"
			
		# parse name formats; get indices for names
		column_names = parse(exp_string, "_")
		file_name_format = parse(sound_string, "_")
		name_index = indexer(file_name_format, column_names)
		
		# parse experiment files; assign labels
		files = parse(exp_file_names, " "); exp_files = []
		for file in files:
			exp_file = [x[:] for x in unicode_csv_reader(open(file,'rU'),delimiter='\t')]
			exp_files.append(exp_file)
			
		# check to see if the old lab file directory exits; make if not
		olddir = check_dir(sounddir, olddir)
		makedirs(sounddir + olddir)
		
		# get indices for columns
		titles = []
		for file in exp_files:
			title = file.pop(0)
			titles.append(title)
		column_indices = []
		for title in titles:
			c_index = indexer(title, column_names)
			column_indices.append(c_index)
	
		# find the column index that will have the relevant text
		lab_indices = []
		for title in titles:
			if u"lab" in title:
				lab_index = title.index(u"lab")
			elif u"text" in title:
				lab_index = title.index(u"text")
			else:
				ind = titles.index(title)
				print files[ind]
				exit("This experiment file does not have a lab or a text column!")
			lab_indices.append(lab_index)
			
		# make a list of the soundfiles in the directory
		soundfiles = glob.glob(sounddir+"*.wav")
		
		for file in soundfiles:
			# get a useable file name; make a lab file name
			filename = file.replace(sounddir, '')
			filename = filename.replace('.wav', '')
			labname = filename + '.lab'
	
			# parse file name; store useful parts to list
			parsed_filename = parse(filename, "_")
			bits = reader(parsed_filename, name_index)
	
			# find the right row in the experiment file
			row_found = False
			for file in exp_files:
				ndx = exp_files.index(file)
				for row in file:
					exp_bits = reader(row, column_indices[ndx])
					if exp_bits == bits:
						row_found = True; row_index = file.index(row); file_index = exp_files.index(file)
	
			# if the row is found, remove current lab file
			if row_found == True:
				if exists(sounddir + filename + '.lab'):
					move(sounddir + labname, sounddir + olddir + labname)
				lab_index = lab_indices[file_index]
				lab_text = exp_files[file_index][row_index][lab_index]
		
				# replace problematic characters
				lab_text = find_replace(lab_text, replist)
				lab_text = lab_text.encode('utf-8')
		
				print lab_text
				labfile = open(sounddir + labname, 'w')
				labfile.write(lab_text)
				labfile.close()
		
		
	elif value == "2":
		# run clean script
				
		print "clean_labfile\n"
		
		language = True
		
		while language == True:
			print"""Select one of the following languages by inputing the number:
1. English
2. French
3. German
4. quit (your language choice is not available)			
			"""
			choice = raw_input("> ")
			
			if choice == "1":
				print("You selected English.")
				language = False
			elif choice == "2":
				print("You selected French.")
				language = False
			elif choice == "3":
				print("You selected German.")
				language = False
			elif choice == "4":
				print("quit")
				language = False
			else:
				print("Invalid input.")
		
		if choice == "4":
			break;
		
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
		olddir = check_dir(filedir, olddir)
		makedirs(filedir + olddir)
		
		# append lists:
		
		if choice == "1":
			rep_list = english_char_list; rep_list.extend(pun_list)
		elif choice == "2":
			rep_list = french_char_list; rep_list.extend(pun_list)
		elif choice == "3":
			rep_list = german_char_list; rep_list.extend(pun_list)
		

		# make a list of all of the relevant files
		lab_list = glob.glob(filedir + '*.lab')

		for file in lab_list:
			f = codecs.open(file, 'r', 'utf-8')
			txt = f.read(); f.close()
			txtnew = find_replace(txt, rep_list)
	
			# make upper or lowercase:
			if choice == "1":
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
	
	elif value == "3":
		# create a dictionary
				
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
		
		# check if dictionary already exists
		dictname = filedir + "/dictionary.txt"
		
		tmpList = []
		old_dict_list = []
		
		# if it does, extract the first word on each line
		if exists(dictname):
		
			with codecs.open(dictname, 'r', 'utf-8') as f:
				tmpList = f.readlines()			
			
			f.close()
			
			for item in tmpList:
				item = item.split()[0]
				old_dict_list.append(item)
				
		# make a dictionary using the lab files just created
		# if a dictionary already exists, merge the two lists of words first
		
		# updated list of files
		lab_list = glob.glob(filedir+"*")

		dictionary_list = []

		# for each file, get words from file and 
		for file in lab_list:
			if ".lab" in file:
		
				#extract each word in file, put into dictionary list
				dictionary_list = extract_word(file, dictionary_list)
		
		dictionary_list = dictionary_list + old_dict_list
		
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
	
	elif value == "4":
		# quit
		print("quit")		
		menu = False
		
	else:
		print("Incorrect input. Try again.")
