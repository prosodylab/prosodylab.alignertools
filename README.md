alignertools
============
Scripts for preparing data to be used by the Prosodylab-Aligner

* Erin Olson <erin.daphne.olson@gmail.com>
* Yasemin Boluk
* Kyle Gorman
* Michael Wagner <chael@mcgill.ca>

## Usage

This is a package of scripts that can be used to prepare existing data for use in the Prosodylab-Aligner. It contains the following kinds of scripts:

* relabel_clean.py
* rename.py
* prep_lab_files.py
* fix_lab.py
* get_[language]_dict.py

### Relabel & Clean

The relabel_clean.py script unites many useful transcription cleaning functions into a simple, iterative script. The user can choose to "relabel" corrupt .lab files (or create new ones) by taking the original tab-delimited experiment file and generating a new set of .lab files for every .wav file in a directory. The user can also opt to "clean" .lab files with the wrong transcription standards for the supported dictionaries, or generate a new orthography-based dictionary for use in the Prosodylab-Aligner. Old .lab files are stored in a new directory that is named by the user. All resulting .lab files will be encoded using UTF-8.

	$ python relabel.py
	
On startup, the user will be prompted to select the function they want to use. If the user selects the "relabel" function, they will have to provide the following information:

* The name of the tab-delimited experiment file or files that will provide the new .lab text - these can be dragged and dropped into the Terminal window
* The id columns of the experiment files, separated by an underscore - the default is "experiment_item_condition"
* The directory where the .wav files are stored. It is assumed that all .wav files are stored in the same directory. This can be dragged and dropped into the Terminal window.
* The id columns of the sound files, separated by an underscore - the default is "experiment_participant_item_condition"
* The name of the directory in which to put any old .lab files - the default is "0_old_labfile_relabel/"

The "clean" function requires the following:
* The language to be used for .lab file cleaning
* The directory where the .wav files are stored. It is assumed that all .wav files are stored in the same directory. This can be dragged and dropped into the Terminal window.
* The name of the directory in which to put the old .lab files - the default is "0_old_labfile_clean/"

The "dictionary" function requires the following:
* The directory where the .lab files are stored. This can be dragged and dropped into the Terminal window.

### Prep Lab Files

The prep_lab_files.py script takes as input any .TextGrid or .eaf (ELAN) file and returns a set of .lab files based on the transcriptions in that file. Ideally for use in conjunction with chop.praat, offered as part of the praatscripts package (to appear). An orthography-based dictionary will also be generated for use in the Prosodylab-Aligner.

	$ python prep_lab_files.py

On startup, the user will be prompted to select from the following options:
* The file format (.TextGrid or .eaf)
* The encoding format of the file (for use with .TextGrid files only)
* The annotation tier from which to make the .lab files and dictionary
* The name of the directory in which to put the old files

### Fix Lab Files

The fix_lab.py script ...

### Rename

The rename.py script acts as a find-and-replace editor for the names of files of a given directory. Old files are stored in a new directory that is named by the user.

	$ python rename.py

On startup, the user will be prompted to provide the following information:

* The directory where all of the files are stored. This can be dragged and dropped into the terminal window.
* The name of the directory in which to put old files - the default is "0_old_file_rename/"
* The problematic string in the file names that needs to be replaced
* The new string that will replace the old string

### Get Dictionary

There is a get_[language]_dict.py script for the each of the supported languages, except English, since support for this language is included in the Prosodylab-Aligner.

	$ python get_[language]_dict.py

In addition, a basic dictionary for each supported language is provided as part of the alignertools package. The French dictionary comes from Lexique v. 3.8.0 and will be downloaded to the user's computer automatically when running the script. The Germany dictionary is from ... and will need to be downloaded prior to running the get_german_dict.py script.
