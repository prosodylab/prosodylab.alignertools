# get_german_dict.py
# coding: utf-8

# This code will take the GPL Dictionary and from it make
# an aligner-useable dictionary.
# Erin Olson erin.daphne.olson@gmail.com
# Current date: 2013/04/25

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

def no_copies(data):
	"""Eliminates identical entries in a list."""
	data_new = []; prev = None
	for line in data:
		if prev is not None and not line == prev:
			data_new.append(prev)
		prev = line
	return data_new

def find_replace(data, list):
	"""Finds and replaces characters given in a list of strings.
	Characters to be replaced must be given as a list of ordered pairs."""
	data_new = []
	for line in data:
		for pair in list:
			if pair[0] in line:
				line = line.replace(pair[0], pair[1])
		data_new.append(line)
	return data_new

# open dictionary file; parse lines into a list
gplcd = open("GPL.CD", "r"); gpl_lines = []
for line in gplcd:
	parsed_line = parse(line,'\\')
	gpl_lines.append(parsed_line)

# keep only the 2nd & 4th columns
gpl_new = []
for line in gpl_lines:
	newline = [line[1], line[3]]
	gpl_new.append(newline)

# eliminate duplicates
gpl_unique = no_copies(gpl_new)

# work only with phonemic transcription
gpl_phones = []
for line in gpl_unique:
	gpl_phones.append(line[1])

# get rid of apostrophes and dashes
gpl_phones2 = find_replace(gpl_phones, [['\'',''],['-','']])

# insert spaces
gpl_spaces = []; sep = ' '
for line in gpl_phones2:
	l = len(line)
	if l > 1:
		index = range(0,l)
		for i in index:
			if 0 < i < l-1:
				nstring = nstring + line[i] + sep
			elif i == 0:
				nstring = line[i] + sep
			else:
				nstring = nstring + line[i]
		line = nstring
	gpl_spaces.append(line)

# replace with phones that make more sense
repl_phones = [['+', 'pf'], ['=', 'ts'],
['J', 'tS'], ['_', 'dZ'], ['1', 'ei'], [')', 'EE'], ['0', 'E~'],
['c', 'I~'], ['|', 'oe'], ['/', 'OE'], ['^', 'OE~'], ['$', 'OO'],
['X', 'Oi'], ['4', 'OI'], ['~', 'O~'], ['V', '^'], ['3', 'R'],
['{', 'ae'], ['A', 'AA'], ['&', 'A'], ['W', 'Ai'], ['B', 'Au'],
['2', 'AI'], ['6', 'AU'], ['q', 'A~'], ['#', 'aa']]
gpl_newphones = find_replace(gpl_spaces, repl_phones)

# make everything lowercase?
spelling = []
for line in gpl_unique:
	newline = line[0].lower()
	spelling.append(newline)

# stitch back into one file
gerdict = []; index = range(0,len(gpl_newphones))
for i in index:
	newline = [spelling[i], gpl_newphones[i]]
	gerdict.append(newline)

# sort dictionary (for goot measure)
gerdict.sort()

# write to file
dict = open('dictionary.txt','w')
index = range(0,len(gerdict))
for i in index:
	printline = gerdict[i][0] + sep + gerdict[i][1] + '\n'
	dict.write(printline)

# close files
gplcd.close()
dict.close()