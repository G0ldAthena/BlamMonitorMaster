# Blam Monitor Master
A Python script for handling Blam's monitor functions.
 
Most engines of the Halo MCC mod tools support file monitoring, which means any changes detected in files of a given type in the data folder are automatically recompiled into their tag formats. This script is a simple GUI handler to easily enable/disable these functions at will.

Supports Halo 2, Halo 3, Halo 3: ODST, Halo: Reach, and Halo 4, though not all engines share the same monitor commands.

Engine command support:
* Bitmaps: 2, 3, ODST, Reach, 4
* Bitmaps (Data and Tags): 2
* Models: 2, 3, ODST, Reach
* Models (Draft): 3, ODST, Reach
* Strings: 3, ODST, Reach, 4
* Structures: 2, 3, ODST

# Requirements
[Python](https://www.python.org/) - Developed with version 3.10.7, older version may work but are untested.

# Installation
Place the "BlamMonitorMaster.py" file in the root directory of the editing kit you wish to run the script with.

# Usage
Simply select an engine version, click the buttons of which file types you want monitored, and you're good to go!
Any changes detected will be monitored by tool and compiled into tags.
