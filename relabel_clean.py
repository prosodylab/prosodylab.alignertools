# !/usr/bin/env python
# coding=utf8

# relabel_clean.py
# Erin Olson ekolson@mit.edu
# Last updated: 2014 06 17
#
# Copyright (c) 2011-2013 Erin Olson, Michael Wagner, and Yasemin Boulk
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# relabel_clean.py
# Erin Olson <ekolson@mit.edu> and Michael Wagner <chael@mcgill.ca>
#
# See README.md for usage information and a tutorial.

import re, getopt, sys, glob, codecs, csv
from os import makedirs
from os.path import exists
from shutil import move

# new small function
# ----------------------------------------------------------------------------------------

def name_check(dirname):
	"""Check to see if the directory name is in the right format"""
	if dirname[-1] == " ":
		dirname = dirname[:-1]
	if dirname[-1] != "/":
		dirname += "/"
	return dirname

# small functions imported wholesale from original relabel_clean.py
# ----------------------------------------------------------------------------------------

def unicode_csv_reader(data, **kwargs):
	"""Enables all cells in a .csv file to be read as unicode strings."""
	data_file = csv.reader(data, **kwargs)
	for row in data_file:
		yield [unicode(cell, 'utf-8') for cell in row]

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

def check_dir(filedir, olddir): # Yasemin's code
	"""Check to see if the old directory exists already"""
	goodname = False
	while goodname == False:
		if exists(filedir + olddir):
			print """Directory already exists!
Please pick a knew directory name for old lab files:"""
			olddir = raw_input("> ")
			olddir = name_check(olddir)
		else:
			goodname = True
	return olddir

# crucial steps (outlined below in 9 yds)
# ----------------------------------------------------------------------------------------

# STEP 2 - needs to return the exp_files in list form
def get_exp_files(exp_file_list):
	exp_files = []
	files = exp_file_list.split(" ")
	for file in files:
		ef = [x[:] for x in unicode_csv_reader(open(file, 'rU'), delimiter = '\t')]
		exp_files.append(ef)
	return exp_files

# STEPS 3 & 4 & 5 - needs to return a lot of stuff
def get_index(exp_files, col_names, wav_format):
	# get titles from exp_files
	titles = []
	for file in exp_files:
		title = file.pop(0)
		titles.append(title)
	
	# get column indices
	cols = col_names.split("_")
	column_indices = []
	for title in titles:
		c_index = indexer(title, cols)
		column_indices.append(c_index)
	
	# get text indices
	text_indices = []
	for title in titles:
		if u"lab" in title:
			lab_index = title.index(u"lab")
		elif u"text" in title:
			lab_index = title.index(u"text")
		else:
			exit("One of your files is missing a lab or a text column.")
		text_indices.append(lab_index)
	
	# get format
	file_name_format = wav_format.split("_")
	format_index = indexer(file_name_format, cols)
	
	return column_indices, text_indices, format_index

# STEP 6
def make_old_directory(file_dir, old_dir):
	# check name
	old_dir = check_dir(file_dir, old_dir)
	# make directory
	makedirs(file_dir + old_dir)

# STEP 7 - needs to return the globbed list
def read_files(file_dir, file_type):
	if file_type == "lab":
		return glob.glob(file_dir + "*.lab")
	elif file_type == "wav":
		return glob.glob(file_dir + "*.wav")
	else:
		exit("Unrecognized file type") # more for me than for anything else

# STEP 8A - return bits
def parse_file_name(file, format_index):
	parsed_filename = file.split("_")
	return reader(parsed_filename, format_index)

# STEP 8B - find line, otherwise spit back False
def find_line_in_file(files, bits, column_indices, lab_indices):
	row_found = False
	for file in files:
		ndx = files.index(file)
		for row in file:
			exp_bits = reader(row, column_indices[ndx])
			if exp_bits == bits:
				row_found = True
				row_index = file.index(row)
				file_index = files.index(file)
	
	if row_found == True:
		lab_index = lab_indices[file_index]
		return files[file_index][row_index][lab_index]
	else:
		return False

# STEP 8Ci - clean text
def clean_text(lang, text):
	rep_list =[[u".",u""], [u",",u""], [u"!",u""], [u"?",u""], [u":",u""], [u";",u""], 
		[u'"',u""], [u"/",u""], [u"\n",u" "], [u"\\n",u" "], [u"\t",u" "], [u"\u2026",u""], 
		[u"\\", u""], [u"\u201c",u""], [u"\u201d",u""], [u"\u201f",u""], [u"\u201a",u""], 
		[u"\u201e",u""], [u"\u2033",u""], [u"\u2039",u""], [u"\u203a",u""], [u"\xab",u""], 
		[u"\xbb",u""], 	[u"\xa0",u" "], [u"\u2018",u"'"], [u"\u2019",u"'"], [u"\u201b",u"'"], 
		[u"\u2032",u"'"], [u"\xad",u""], [u"\u2013",u""],[u"\u2011",u""], [u"\u2014",u""], 
		[u"\u2012",u""], [u"\xab", ''], [u'\xbb', ''], ["  ", " "], ["[", ""],
		["]", ""], ["(", ""], [")", ""], [" '", " "], ["' ", " "]]
	
	if lang == "en":
		rep_list.extend([['0', 'zero '], ['1', 'one '], ['2', 'two '], ['3', 'three '], ['4', 'four '],
			['5', 'five '], ['6', 'six '], ['7', 'seven '], ['8', 'eight '], ['9', 'nine '], 
			['&', 'and'], ['\'s', ' s'], ["\'S", " S"], ['\'ll', ' ll'], ["'LL", " LL"], 
			['\'d', ' d'], ["'D", " D"], ['%', ' percent'], ["-", ""],
			['\'ve', ' ve'], ["'VE", " VE"]])
	elif lang == "fr":
		rep_list.extend([["s'", "s' "], ["S'", "S' "], ["d'", u"d' "], 
			["D'", "D' "], ["l'", "l' "], ["L'", "L' "], ["n'", "n' "], ["N'", "N' "], ["qu'", "qu' "], 
			["Qu'", "Qu' "], ["j'", "j' "], ["J'", "J' "], ["t'", "t' "], ["T'", "T' "], ["m'", "m' "], 
			["Y'", "Y' "], ["y'", "y' "],["M'", "M' "], ["jusqu'", "jusqu "], ["Jusqu'", "Jusqu "],  
			['0', 'zero '], ['1', 'un '], ['2', 'deux '],['3', 'trois '], ['4', 'quatre '], 
			['5', 'cinq '], ['6', 'six '], ['7', 'sept '], ['8', 'huit '], ['9', 'neuf '], 
			['&', 'et']])
	elif lang == "de":
		rep_list.extend([['0', 'zero '], ['1', 'ein '], ['2', 'zwei '], ['3', 'drei '],
			['4', 'vier '], ['5', 'fünf '], ['6', 'sechs '], ['7', 'sieben '], ['8', 'acht '],
			['9', 'neun '], ['&', 'und']])
	elif lang == "en-celex":
		rep_list.extend([["'D", " 'D"], ["'d", " 'd"], ["'RE", " 'RE"], ["'re", " 're"],
			["'LL", " 'LL"], ["'ll", " 'll"], ["'S ", " 'S "], ["'s ", " 's "], ["'VE", " 'VE"],
			["'ve", " 've"], ["0", "zero "], ["1", "one "], ["2", "two "], ["3", "three "],
			["4", "four "], ["5", "five "], ["6", "six "], ["7", "seven "], ["8", "eight "],
			["9", "nine "], ["&", "and "], ["%", " percent"]])
	elif lang == "en-timit":
		rep_list.extend([['0', 'zero '], ['1', 'one '], ['2', 'two '], ['3', 'three '], ['4', 'four '],
			['5', 'five '], ['6', 'six '], ['7', 'seven '], ['8', 'eight '], ['9', 'nine '], 
			['&', 'and'], ["%", " percent"]])
	elif lang == "nl":
		rep_list.extend([["0" , "nul "], ["1", "een "], ["2", "twee "], ["3", "drie "], ["4", "vier "],
			["5", "vijf "], ["6", "zes "], ["7", "zeven "], ["8", "acht "], ["9", "negen "],
			["&", "en"]])
		
	text = find_replace(text, rep_list)
	
	if text[0] == "'":
		text = text[1:]
	if text[-1] == "'":
		text = text[:-1]
	
	text = text.upper()
	return text.encode('utf-8')

# STEP 8Cii - store dictionary words
def store_to_dictionary(text, dict_list):
	for word in text.split(" "):
		if word not in dict_list:
			dict_list.append(word)
	return dict_list

# STEP 8Ciii - move old .lab file
def move_old_lab(file_dir, old_dir, file_name):
	if exists(file_dir + file_name):
		move(file_dir + file_name, file_dir + old_dir + file_name)

# STEP 8Civ - write text to new .lab file
def write_to_lab(file_dir, file_name, text):
	labfile = open(file_dir + file_name, 'w')
	labfile.write(text)
	labfile.close()

# STEP 9
def make_dictionary_file(file_dir, dict_list):
	# add pronunciation
	dictionary = []
	for word in dict_list:
		pron = " ".join(list(word))
		entry = word + " " + pron
		dictionary.append(entry)
	
	# sort
	dictionary.sort()
	
	# save
	d = open(file_dir + "dictionary.txt", "w")
	d.write("\n".join(dictionary))
	d.close()

# fitting steps together, depending on what you want to do
# ----------------------------------------------------------------------------------------

# Simplest case: make a dictionary from existing .lab files:
def create_dictionary(file_dir):
	"""Creates a dictionary from text in existing, cleaned .lab files"""
	word_list = []
	file_list = read_files(file_dir, "lab") # step 7
	for file in file_list:
		with open(file, 'r') as f:
			text = f.read()
		word_list = store_to_dictionary(text, word_list) # step 8cii
	make_dictionary_file(file_dir, word_list) # step 9

# Cleaning:
def clean_module(file_dir, old_dir, lang, dict):
	"""Cleans existing .lab files"""
	word_list = []
	make_old_directory(file_dir, old_dir) # step 6
	file_list = read_files(file_dir, "lab") # step 7
	for file in file_list:
		with open(file, 'r') as f:
			text = f.read()
		filename = file.replace(file_dir, '')
		text = clean_text(text, lang) # step 8ci
		if dict == True:
			word_list = store_to_dictionary(text, word_list) # step 8cii
		move_old_lab_file(file_dir, old_dir, filename) # step 8ciii
		write_to_lab(file_dir, filename, text) # step 8civ
		
	if dict == True and word_list != []:
		make_dictionary_file(file_dir, word_list) # step 9

# Relabeling:
def relabel_module(exp_file_list, col_names, file_dir, wav_format, old_dir, lang, dict):
	"""Generates cleaned .lab files from a tab-delimited text file"""
	word_list = []
	exp_files = get_exp_files(exp_file_list) # step 2
	ci, ti, fi = get_index(exp_files, col_names, wav_format) # steps 3 - 5
	
	# check to see that there are no .lab files
	f_list = glob.glob(file_dir + "*")
	lab_found = False
	for f in f_list:
		if ".lab" in f:
			lab_found = True
	if lab_found == True:
		make_old_directory(file_dir, old_dir) # step 6
	del f_list
	
	file_list = read_files(file_dir, "wav") # step 7
	for file in file_list:
		# get a file name for the lab file
		file_name = file.replace(file_dir, '')
		file_name = file_name.replace('.wav', '')
		lab_name = file_name + ".lab"
		
		bits = parse_file_name(file_name, fi) # step 8a
		text = find_line_in_file(exp_files, bits, ci, ti) # step 8b
		if text != False:
			text = clean_text(lang, text) # step 8ci
			if dict == True:
				word_list = store_to_dictionary(text, word_list) # step 8cii
			if lab_found == True:
				move_old_lab(file_dir, old_dir, lab_name) # step 8ciii
			write_to_lab(file_dir, lab_name, text) # step 8civ
	if word_list != [] and dict == True:
		make_dictionary_file(file_dir, word_list) # step 9

# get info from user (step 1/main)
# ----------------------------------------------------------------------------------------

def display_help_screen():
	"""Display screen with helpful information"""
	print "\nCommand-line help for using relabel_clean.py\n"
	print "General usage:"
	print "    $ python relabel_clean.py [options] mode [text_file] file/directory/\n"
	raw_input("see functions")
	print """===== FUNCTIONS =====
Function      Usage
relabel       Generates new .lab files for a directory from a given tab-
              delimited text file. Needs both text_file and file/directory
clean         Cleans the text of .lab files in a directory
dictionary    Makes a basic dictionary from the text of the .lab files in a 
              directory
"""
	raw_input("see options")
	print """===== OPTIONS =====
Short + Example       Long      Usage
-c text_file_columns  --col     Specifies which columns to use for finding
                                .lab file text when using the RELABEL mode.
                                Default is experiment_item_condition
-d                    --dict    Makes a basic dictionary from .lab file text
-f file_name_format   --form    Specifies the format for .wav file names when
                                using the RELABEL mode. Default is experiment_
                                participant_item_condition
-h                    --help    Displays this screen
-l en                 --lang    Specifies which language to use when cleaning
                                .lab file text. Default is none
-o old/dir/name/      --old     Specifies what to call the old .lab file
                                directory. Default is 0_old_labfile_relabel/ or
                                0_old_labfile_clean/, depending on function
"""
	raw_input("see examples")
	print """===== EXAMPLES =====
Function      Example
relabel       $ python relabel_clean.py -c filename -f filename -l en 
                  relabel tab/delimited/text_file.txt file/directory/
clean         $ python relabel_clean.py -d --lang fr --old 0_old_labfile/
                  clean file/directory/
dictionary    $ python relabel_clean.py dictionary file/directory/
"""
	sys.exit(0)

def parse_command_line(com_string):
	"""Parses the command line and returns a dictionary of options"""
	#	REMINDER: command line format is $ python relabel_clean.py [options] module (exp_file) file/dir/
	opt_dict = {}
	opts, args = getopt.getopt(com_string, "c:df:hl:o:", ["col=", "dict", "form=", "help", "lang=", "old="])
	
	# display help screen if present
	for option, value in opts:
		if option == "-h" or option == "--help":
			display_help_screen()
	
	# determine module to be used
	if args[0] == "relabel":
		opt_dict["module"] = "1"
	elif args[0] == "clean":
		opt_dict["module"] = "2"
	elif args[0] == "dictionary":
		opt_dict["module"] = "3"
	else:
		sys.exit("Unrecognized module.")
	
	# populate option dictionary for each module with defaults and arguments
	if opt_dict["module"] == "1":
		if len(args) == 3:
			opt_dict["text file"] = args[1]
			opt_dict["file dir"] = name_check(args[2])
		else:
			opt_dict["text file"] = None
			opt_dict["file dir"] = None
			
		opt_dict["columns"] = "experiment_item_condition"
		opt_dict["dict"] = False
		opt_dict["format"] = "experiment_participant_item_condition"
		opt_dict["lang"] = None
		opt_dict["old dir"] = "0_old_labfile_relabel/"
	elif opt_dict["module"] == "2":
		if len(args) == 2:
			opt_dict["file dir"] = name_check(args[1])
		else:
			opt_dict["file dir"] = None
		
		opt_dict["dict"] = False
		opt_dict["lang"] = None
		opt_dict["old dir"] = "0_old_labfile_clean/"
	elif opt_dict["module"] == "3":
		if len(args) == 2:
			opt_dict["file dir"] = name_check(args[1])
		else:
			opt_dict["file dir"] = None
	
	# override defaults with options, if necessary
	for option, value in opts:
		if option == "-c" or option == "--col":
			opt_dict["columns"] = value
		elif option == "-d" or option == "--dict":
			opt_dict["dict"] = True
		elif option == "-f" or option == "--form":
			opt_dict["format"] = value
		elif option == "-l" or option == "--lang":
			opt_dict["lang"] = value
		elif option == "-o" or option == "--old":
			opt_dict["old dir"] = name_check(value)
	
	return opt_dict
	

def main():
	"""Get info from user and pass on to correct module"""
	# If using the command line, parse it into a dictionary; otherwise save as None
	if len(sys.argv) > 1:
		opt_dict = parse_command_line(sys.argv[1:])
	else:
		opt_dict = None
	
	# Get module from user or from command line
	if opt_dict == None:
		print """
===== MENU =====
1. make new .lab files (relabel)
2. reformat existing .lab files (clean)
3. make a dictionary from existing .lab file text

Please enter the number for the option you would like to select:"""
		value = raw_input("> ")
		assert value in ["1", "2", "3"]
	else:
		value = opt_dict["module"] # stored in opt_dict
	
	# For each module, check dictionary and pass on
	if value == "1":
		# get language
		if opt_dict == None:
			print "\nmake new .lab files (relabel)"
			
			print "\nWhat language are your .lab files in? Please use two-character language code"
			print "Recognised codes are en, en-celex, en-timit, fr, de, nl"
			print "If your language is not listed, please leave this field blank"
			lang = raw_input("> ").lower()
		else:
			lang = opt_dict["lang"]
		
		# get tab-delimited text files
		if opt_dict == None or opt_dict["text file"] == None:
			print """\nWhat are the tab-delimited text files that contain the
lab file text (experiment files)? (must include directory)
You can drag and drop the files into the Terminal window to fill out this space
WARNING: No individual directory should include a space chacter
If so, please go back and replace any spaces with underscores"""
			exp_files = raw_input("> ")
			if exp_files[-1] == " ":
				exp_files = exp_files[:-1]
		else:
			exp_files = opt_dict["text file"]
		
		# get column names
		if opt_dict == None:
			print """\nWhat are the columns that identify the lab text (id columns of the experiment
file)? Separate all id columns with an underscore
Default is: experiment_item_condition
Press enter to use default"""
			exp_cols = unicode(raw_input("> "))
			if exp_cols == "":
				exp_cols = "experiment_item_condition"
		else:
			exp_cols = opt_dict["columns"]
		
		# get file directory
		if opt_dict == None or opt_dict["file dir"] == None:
			print """\nWhat is the sound directory?
You can drag and drop the file into the Terminal window to fill out this space"""
			file_dir = raw_input("> ")
			file_dir = name_check(file_dir)
		else:
			file_dir = opt_dict["file dir"]
		
		# get file name format
		if opt_dict == None:
			print """\nWhat format are the sound file names in?
(What are the id columns of the sound file?)
Default is: experiment_participant_item_condition
Press enter to use default"""
			format = unicode(raw_input("> "))
			if format == '':
				format = "experiment_participant_item_condition"
		else:
			format = opt_dict["format"]
		
		# get old directory name
		if opt_dict == None:
			print """\nWhat would you like to call the directory for the old lab files?
Default is: 0_old_labfile_relabel/
Press enter to use default"""
			old_dir = raw_input("> ")
			if old_dir == '':
				old_dir = "0_old_labfile_relabel/"
			old_dir = name_check(old_dir)
		else:
			old_dir = opt_dict["old dir"]
		
		# get dictionary option
		if opt_dict == None:
			print "\nWould you like to create a dictionary from the lab file text?"
			print "Please answer 'y' or 'yes' if so"
			d_choice = raw_input("> ").lower()
			if d_choice == "y" or d_choice == "yes":
				dict = True
			else:
				dict = False
		else:
			dict = opt_dict["dict"]
		
		# pass on
		relabel_module(exp_files, exp_cols, file_dir, format, old_dir, lang, dict)
		sys.exit(0)
	
	elif value == "2":
		# get language
		if opt_dict == None:
			print "\nreformat existing .lab files (clean)"
			
			print "\nWhat language are your .lab files in? Please use the two-character language code"
			print "Recognised codes are en, en-celex, en-timit, fr, de, nl"
			print "If your language is not listed, please leave this field blank"
			lang = raw_input("> ").lower()
		else:
			lang = opt_dict["lang"]
		
		# get file directory
		if opt_dict == None or opt_dict["file dir"] == None:
			print """\nWhat is the sound directory?
You can drag and drop the file into the Terminal window to fill out this space"""
			file_dir = raw_input("> ")
			file_dir = name_check(file_dir)
		else:
			file_dir = opt_dict["file dir"]
			
		# get the name of the old directory
		if opt_dict == None:
			print """\nWhat would you like to call the directory for old lab files?
Default is: 0_old_labfile_clean/
Press enter to use default"""
			old_dir = raw_input("> ")
			old_dir = name_check(old_dir)
		else:
			old_dir = opt_dict["old dir"]
		
		# see if the user wants to use a dictionary
		if opt_dict == None:
			"\nWould you like to create a dictionary from the lab file text?"
			print "Please answer 'y' or 'yes' if so"
			d_choice = raw_input("> ").lower()
			if d_choice == "y" or d_choice == "yes":
				dict = True
			else:
				dict = False
		else:
			dict = opt_dict["dict"]
		
		# pass on
		clean_module(file_dir, old_dir, lang, dict)
		sys.exit(0)
		
	elif value == "3":
		if opt_dict == None:
			print "\nmake a dictionary from existing .lab file text"
		
		if opt_dict == None or opt_dict["file dir"] == None:
			print """\nWhat is the .lab file directory?
You can drag and drop the file into the Terminal window to fill out this space"""
			file_dir = raw_input("> ")
			file_dir = name_check(file_dir)
		else:
			file_dir = opt_dict["file dir"]
		
		create_dictionary(file_dir)
		sys.exit(0)

main()
