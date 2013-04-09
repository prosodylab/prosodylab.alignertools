alignertools
============
Scripts for preparing data to be used by the Prosodylab-Aligner

* Erin Olson <erin.daphne.olson@gmail.com>
* Michael Wagner <chael@mcgill.ca>

## Funding

## License

## Languages

The languages that are currently supported by alignertools are listed below in alphabetical order.

* English
* French
* German
* Mi'gmaq

## Usage

This is a package of scripts that can be used to prepare data collected by the Prosodylab Experimenter. It contains the following kinds of scripts:

* relabel.py
* clean_labfile.py
* get_[language]_dict.py

### Relabel

The relabel.py script takes the original tab-delimited experiment file and generates a new set of .lab files for every .wav file in a directory. Old .lab files are stored in a new directory that is named by the user. All resulting .lab files will be encoded using UTF-8.

  $ python relabel.py
	
On startup, the user will the prompted to provide the following information:

* The name of the experiment file or files that will provide the new .lab text - these can be dragged and dropped into the Terminal window
* The id columns of the experiment files, separated by an underscore - the default is "experiment_item_condition"
* The directory where the .wav files are stored. It is assumed that all .wav files are stored in the same directory. This can be dragged and dropped into the Terminal window.
* The id columns of the sound files, separated by an underscore - the default is "experiment_participant_item_condition"
* The name of the directory in which to put any old .lab files - the default is "0_old_labfile_relabel/"

### Clean Labfile

The clean_labfile.py script takes the original .lab files in a directory and cleans their text to be readable by the Prosodylab-Aligner. Old .lab files are stored in a new directory that is named by the user. All resulting .lab files will be encoded using UTF-8.

	$ python clean_labfile.py

On startup, the user will be prompted to provide the following information:

* The language used in the .lab files. Currently, English, French, German, and Mi'gmaq are supported.
* The directory where the .lab files are stored. This can be dragged and dropped into the Terminal window.
* The name of the directory in which to put the old .lab files - the default is "0_old_labfile_clean/"

### Get Dictionary

There is a get_[language]_dict.py script for the each of the supported languages, except English, since support for this language is included in the Prosodylab-Aligner.

	$ python get_[language]_dict.py

In addition, a basic dictionary for each supported language is provided as part of the alignertools package. The French dictionary comes from Lexique v. 3.8.0, while the Germany dictionary is from ...
