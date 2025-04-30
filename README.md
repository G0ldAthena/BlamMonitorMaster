<p align="center">
<img src=https://i.imgur.com/y8MCh3J.png align="center">
<h1>Blam Monitor Master</h1>
</p>
A Python-built GUI for handling Blam's monitor functions.
 
Most engines of the Halo MCC mod tools support **file monitoring**, which means any changes detected in files of a given type in the data folder are automatically recompiled into their tag formats. This executable is a simple GUI handler to easily enable/disable these functions at will.

Supports Halo 2, Halo 3, Halo 3: ODST, Halo: Reach, and Halo 4, though not all engines share the same monitor commands.

Engine command support:
|                         | Halo 2   | Halo 3   | Halo 3: ODST | Halo: Reach | Halo 4   |
|------------------------:|:-----:|:-----:|:------:|:-------:|:-----:|
| Bitmaps                 | X  | X  | X   | X    | X  |
| Bitmaps (Data and Tags) | X  |    |     |      |    |
| Models                  | X  | X  | X   | X    |    |
| Models (Draft)          |    | X  | X   | X    |    |
| Strings                 |    | X  | X   | X    | X  |
| Structures              | X  | X  | X   |      |    |

> [!NOTE]
> 
> By default, Tool's string monitoring function places recompiled strings into the root */tags/* folder, rather than the tags folder equivalent of the source data file path. As of BMM v1.1, this oddity has been accounted for by automatically moving the recompiled tag to the right location.
>

# Requirements
None! The executable version has no requirements.

If you choose to download the source script, it was developed with version 3.10.7. Older versions may work but are untested.

# Installation
Place the BlamMonitorMaster executable file in the root directory of the editing kit you wish to monitor.

# Usage
Simply click the buttons of which file types you want monitored, and you're good to go! Any changes detected will be monitored by tool and compiled into tags.

The engine version should be automatically selected by default (using tool.exe's properties), but you may also set it manually.

# Credits
<b>GoldAthena</b>
- Code and UI

<b>Paddy Tee</b>
 - Logo
