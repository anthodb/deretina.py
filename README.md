deretina.py
Written by Cory Alder
designed to be used as a build script from Xcode
automatically scales all retina graphics (denoted by <filename>@2x.png) to half size

CONFIGURATION
depending on your preference, set should_overwrite_existing_files.
script expects images to be located in $SOURCE_ROOT/Assets/
(change that on line 33)

INSTALLATION
Place in $SOURCE_ROOT, and add a run-script build step
Make sure the run script happens before "copy bundle resources"

Script:
/usr/bin/python $SOURCE_ROOT/deretina.py

<img src="https://raw.github.com/coryalder/deretina.py/master/img/runscript.png">

(if you know how to run python direct from Xcode, let me know. cory@davander.com)

last updated Sept. 17th 2011