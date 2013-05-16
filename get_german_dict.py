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
	
def find_replace_stress(data):
	"""Finds and replaces stressed vowels by splitting string into three subsections
	with the apostrophe as separator. the first instance of a 0 in the third substring
	is the vowel to be stressed"""
	data_stress = []
	for line in data:
		tmp_tuple = line.partition('\' ')
		new_line = tmp_tuple[0] + tmp_tuple[1] + tmp_tuple[2].replace('0', '1', 1)
		data_stress.append(new_line)
	return data_stress

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

#get rid of dashes
gpl_phones2 = find_replace(gpl_phones, [['-', '']])

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
				nstring = nstring + line[i] + sep
		line = nstring
	gpl_spaces.append(line)

# replace with phones that make more sense
repl_phones = [[' +', ' pf'], [' =', ' ts'],
[' J', ' tS'], [' _', ' dZ'], [' 1', ' ei'], [' )', ' EE'], [' 0', ' E~'],
[' c', ' I~'], [' |', ' oe'], [' /', ' OE'], [' ^', ' OE~'], [' $', ' OO'],
[' X', ' Oi'], [' 4', ' OI'], [' ~', ' O~'], [' V', ' ^'], [' 3', ' R'],
[' {', ' ae'], [' A', ' AA'], [' &', ' A'], [' W', ' Ai'], [' B', ' Au'],
[' 2', ' AI'], [' 6', ' AU'], [' q', ' A~'], [' #', ' aa']]
gpl_newphones = find_replace(gpl_spaces, repl_phones)

#replace all vowels
not_stress_vowels = [['i ', 'i0 '], ['I ', 'I0 '], ['y ', 'y0 '], ['Y ', 'Y0 '],
['u ', 'u0 '], ['U ', 'U0 '], ['e ', 'e0 '], ['ei ', 'ei0 '], ['EE ', 'EE0 '],
['E ', 'E0 '], ['E~ ', 'E~0 '], ['I~ ', 'I~0 '], ['oe ', 'oe0 '], ['OE ', 'OE0 '],
['OE~ ', 'OE~0 '], ['o ', 'o0 '], ['OO ', 'OO0 '], ['O ', 'O0 '], ['Oi ', 'Oi0 '],
['OI ', 'OI0 '], ['O~ ', 'O~0 '], ['^ ', '^0 '], ['@ ', '@0 '], ['R ', 'R0 '],
['ae ', 'ae0 '], ['a ', 'a0 '], ['A ', 'A0 '], ['Ai ', 'Ai0 '], ['Au ', 'Au0 '],
['AI ', 'AI0 '], ['AU ', 'AU0 '], ['A~ ', 'A~0 '], ['AA ', 'AA0 '], ['aa ', 'aa0 ']]
gpl_notstressed = find_replace(gpl_newphones, not_stress_vowels)

gpl_stressed = find_replace_stress(gpl_notstressed)

#get rid of apostrophes
gpl_final = find_replace(gpl_stressed, [['\' ', '']])

# make everything lowercase?
spelling = []
for line in gpl_unique:
	newline = line[0].lower()
	spelling.append(newline)

# stitch back into one file
gerdict = []; index = range(0,len(gpl_final))
for i in index:
	newline = [spelling[i], gpl_final[i]]
	gerdict.append(newline)

# sort dictionary (for good measure)
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