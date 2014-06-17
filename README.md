alignertools
============
Scripts for preparing data to be used by the Prosodylab-Aligner

* Erin Olson <ekolson@mit.edu>
* Yasemin Boluk
* Kyle Gorman
* Michael Wagner <chael@mcgill.ca>

## Usage

This is a package of scripts that can be used to prepare existing data for use in the Prosodylab-Aligner. It contains the following kinds of scripts:

* `relabel_clean.py`
* `rename.py`
* `prep_lab_files.py`
* `fix_lab.py`

### Relabel & Clean

The `relabel_clean.py` script unites many useful transcription cleaning functions into a single script. The user can choose to "relabel" corrupt `.lab files` (or create new ones) by taking the original tab-delimited experiment file and generating a new set of `.lab` files for every `.wav` file in a directory. The user can also opt to "clean" `.lab` files with the wrong transcription standards for the supported dictionaries, or generate a new orthography-based dictionary for use in the Prosodylab-Aligner (hereafter referred to as a "basic dictionary"). Old `.lab` files are stored in a new directory that is named by the user. All resulting `.lab` files will be encoded using UTF-8.

In general, if the user selects the "relabel" function, the "clean" function will also be performed on any resulting `.lab` files.

#### Basic usage
There are two ways to use this script. The first involves starting up the script in the following way:

    $ python relabel_clean.py
	
On startup, the user will be prompted to select the function they want to use. If the user selects the "relabel" function, they will have to provide the following information:

* The two-character language code to be used for `.lab` file text cleaning
* The name of the tab-delimited experiment file or files that will provide the new `.lab` text - these can be dragged and dropped into the Terminal window
* The id columns of the experiment files, separated by an underscore - the default is `experiment_item_condition`
* The directory where the .wav files are stored. It is assumed that all `.wav` files are stored in the same directory. This can be dragged and dropped into the Terminal window.
* The file name format of the sound files, separated by an underscore - the default is `experiment_participant_item_condition`
* The name of the directory in which to put any old `.lab` files - the default is `0_old_labfile_relabel/`
* Whether the user wants to create a basic dictoionary out of the `.lab` file text or not

The "clean" function requires the following:
* The language to be used for `.lab` file cleaning
* The directory where the `.wav` files are stored. It is assumed that all `.wav` files are stored in the same directory. This can be dragged and dropped into the Terminal window.
* The name of the directory in which to put the old `.lab` files - the default is `0_old_labfile_clean/`
* Whether the user wants to create a basic dictionary out of the `.lab` file text or not

The "dictionary" function requires the following:
* The directory where the `.lab` files are stored. This can be dragged and dropped into the Terminal window.

#### Command-line usage
The `relabel_clean` script now also allows more experienced users to use a *command-line interface* for performing the same tasks. It can be used in the following way:

    $ python relabel_clean.py [options] function [tab-delimited_experiment_file.txt] file/directory/

In general, all *options* are those bits of information that relabel_clean.py will have default values for, such as the name of the directory for old .lab files or the file name format for sound files. If no option is specified in the command line, the default value of that option will be used. All options have a *short*, one-character name and a *long*, three- to four-characther name. Long and short option names are interchangeable. A full list of options is provided below:

Short | Long | Usage | Purpose
------|------|-------|--------
`-c` | `--col` | `--c column_names` | Specifies which columns to use for finding .lab file text when using the RELABEL mode.  Default is `experiment_item_condition`
`-d` | `--dict` | `-d` |  Makes a basic dictionary from .lab file text
`-f` | `--form` | `-f file_name_format` | Specifies the format for .wav file names when  using the RELABEL mode. Default is `experiment_participant_item_condition`
`-h` | `--help` | `-h` | Displays the help screen
`-l` | `--lang` | `-l en` | Specifies which language to use when cleaning .lab file text. Default is none (only basic cleaning performed)
`-o` | `--old` | `-o old/directory/` | Specifies what to call the old .lab file directory. Default is 0_old_labfile_relabel/ or 0_old_labfile_clean/, depending on function used

The *function* is the name of the function that the user wishes to make use of. These are:
* `relabel`
* `clean`
* `dictionary`

All other arguments are *essential* to the functioning of the script, and consist of the name of one tab-delimited experiment file (if using the relabel function) and the name of the file directory (for all functions).

##### Command-line Examples
Here is an example of how to use the `relabel` function from the command line, with all options set to non-default values:

    $ python relabel_clean.py -l en -c item_condition -f subject_group_item_condition -o 0_corrupted_labfiles/ -d relabel full_experiment_file.txt experiment_soundfiles/

Here is a breakdown of what each component of this example does:
* **python relabel_clean.py** This calls the script
* **-l en** This sets the cleaning language to English
* **-c item_condition** This tells the script that the item and condition columns are to be used in locating the `.lab` text in the experiment file
* **-f subject_group_item_condition** This tells the script that the `.wav` file name format is `subject_group_item_condition.wav`
* **-o 0_corrupted_labfiles** This tells the script to call the directory for old `.lab` files `0_corrupted_labfiles`
* **-d** This tells the script to make a basic dictionary from the words in the `.lab` file text
* **relabel** This tells the script to use the `relabel` function
* **full_experiment_file.txt** This tells the script that the experiment file is `full_experiment_file.txt`
* **experiment_soundfiles/** This tells the script that the sound files can be found in the directory `experiment_soundfiles/`

Here is a much shorter example of how to use the `clean` function from the command line, using long option names:

    $ python relabel_clean.py --lang en --dict clean experiment_soundfiles/

Here is a breakdown of what each component of this example does:
* **python relabel_clean.py** This calls the script
* **--lang en** This sets the cleaning language to English
* **--dict** This tells the script to make a basic dictionary from the words in the `.lab` file text
* **clean** This tells the script to use the `clean` function
* **experiment_soundfiles/** This tells the script that the sound files can be found in the directory `experiment_soundfiles/`

Notice that after the `clean` function is called, there is no need to specify a tab-delimited experiment file.

Finally, here is an example of how to use the `dictionary` function alone:

    $ python relabel_clean.py dictionary experiment_soundfiles/

### Prep Lab Files

The `prep_lab_files.py` script takes as input any `.TextGrid` or `.eaf` (ELAN) file and returns a set of `.lab` files based on the transcriptions in that file. Ideally for use in conjunction with `chop.praat`, offered as part of the praatscripts package (to appear). An orthography-based dictionary will also be generated for use in the Prosodylab-Aligner.

    $ python prep_lab_files.py

On startup, the user will be prompted to select from the following options:
* The file format (`.TextGrid` or `.eaf`)
* The encoding format of the file (for use with `.TextGrid` files only)
* The annotation tier from which to make the `.lab` files and dictionary
* The name of the directory in which to put the old files

### Rename

The `rename.py` script acts as a find-and-replace editor for the names of files of a given directory. Old files are stored in a new directory that is named by the user.

    $ python rename.py

On startup, the user will be prompted to provide the following information:

* The directory where all of the files are stored. This can be dragged and dropped into the terminal window.
* The name of the directory in which to put old files - the default is `0_old_file_rename/`
* The problematic string in the file names that needs to be replaced
* The new string that will replace the old string

### Get Dictionary

In previous versions of this software, there was a `get_[language]_dict.py` script for the each of the supported languages, except English, since support for this language is included in the Prosodylab-Aligner. These scripts are now deprecated, and full dictionaries for English, French, German, and Dutch may be found in the [prosodylab.dictionaries](https://github.com/prosodylab/prosodylab.dictionaries) depository.
