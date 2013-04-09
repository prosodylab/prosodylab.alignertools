# get_french_dict
# coding: utf8

# This code will download Lexique 380 and from it make
# an aligner useable ASCII only dictionary.
# Erin Olson erin.daphne.olson@gmail.com
# Current date: 2013/04/09

import csv
from subprocess import call

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

def no_copies(data):
	"""Eliminates identical entries in a list."""
	data_new = []; prev = None
	for line in data:
		if prev is not None and not line == prev:
			data_new.append(prev)
		prev = line
	return data_new

# get Lexique 380 from website
call(["curl", "-o", "Lexique380.zip", "http://www.lexique.org/public/Lexique380.zip"])
call(["unzip", "Lexique380.zip"])
call(["cd", "./Lexique380/Bases+Scripts/"])

# open .csv file
lexique = [x[:] for x in csv.reader(open('Lexique380.txt','rb'),delimiter='\t')]

# limit to first two columns; remove titles
lexnew1 = []
for line in lexique:
	lexnew1.append(line[0:2])
titles = lexnew1.pop(0)

# eliminate rows with spaces in the first element
lexnew2 = []
for line in lexnew1:
	if not ' ' in line[0]:
		lexnew2.append(line)

# eliminate identical rows
lexnew3 = no_copies(lexnew2)

lexipa = []
for line in lexnew3:
	lexipa.append(line[1])
# find and replace hex codes, numbers in 2nd column
repl = [['\xc2\xb0', '~'], ['\xc2\xa7', '0']]
lexipanew = find_replace(lexipa, repl)

# separate everything in 2nd column by spaces
lexipanew2 = []; sep = ' '
for line in lexipanew:
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
	lexipanew2.append(line)

# replace annoying characters with those that make more sense
repl2 = [['N', 'gn'], ['G', 'ng'], ['0', 'x0'], ['1', 'x1'], ['2', 'x2'], ['5', 'x5'], ['8', 'x8'], ['9', 'x9']]
lexipanew3 = find_replace(lexipanew2, repl2)

# stitch back together into a new list; eliminate identicals; sort
frendict = []
index = range(0,len(lexnew3))
for i in index:
	newline = [lexnew3[i][0], lexipanew3[i]]
	frendict.append(newline)
frendictnew = no_copies(frendict)
frendictnew.sort()

# write to dictionary
call(["cd", "../.."])
dict = open('dictionary.txt','w')
index = range(0,len(frendictnew))
for i in index:
	newline = frendictnew[i][0] + sep + frendictnew[i][1] + '\n'
	dict.write(newline)