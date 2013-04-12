# rename.py

# This script acts as a find-and-replace option for changing the names of files
# stored in a directory. Original files will be stored in a separate directory.
# Will only work on relevant files (those that have the problematic string).
# Erin Olson erin.daphne.olson@gmail.com
# Current date: 2013/04/12

from glob import glob
from os import makedirs
from os.path import exists
from subprocess import call

# form
print """rename

This script works like a regular find-and-replace option on word processors.
Please use it accordingly!

What is the file directory?
You can drag and drop the files into the Terminal window to fill out this space
WARNING: No individual directory should have a space character
If so, please go back and replace any spaces with underscores
(Yes it is a little ridiculous to have to do this by hand when you have this
script, but otherwise Python can't read it. Sorry!)"""
filedir = raw_input("> ")
if filedir[-1] == ' ':
	filedir = filedir.replace(" ", '')
if filedir[-1] != '/':
	filedir = filedir + '/'
print"""
What would you like to call the directory for old files?
Default is: 0_old_file_rename/
Press enter to use default"""
olddir = raw_input("> ")
if olddir == '':
	olddir = "0_old_file_rename/"
if olddir[-1] != '/':
	olddir = olddir + "/"
print "\nPlease type what you would like to find below:"
oldstring = raw_input("> ")
print "\nPlease type what you would like to replace it with below:"
newstring = raw_input("> ")

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
	if oldstring in file:
		# make a set of file names
		oldfilename = file.replace(filedir, '')
		newfilename = oldfilename.replace(oldstring, newstring)
		
		# move old file to olddir; copy this file into normal dir
		call(["mv", file, filedir + olddir + oldfilename])
		call(["cp", filedir + olddir + oldfilename, filedir + newfilename])