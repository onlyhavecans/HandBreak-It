# "HandBreak" is an advanced batch script for HandbrakeCLI
## Overview
Have you ever had a lot of files to encode all at once. Adding batches of video files in to handbreak is cumbersome and time consuming so instead take a handbreak from handbrake and use this quick program!

The goal behind this is not to replace Handbrake GUI but to add a way to quickly and easily do a large batch encode of files based on saved presets. For serious one time conversions you just double click the HandBreak.py file and follow the instructions, it will tell you when it is done. The program can also be scripted at the command line level and run headless.

I am currently taking what started as a simple script and am trying to refactor it in to a full program. Since it is a one trick pony and obviously not too popular I will probably only push it to version two with a sparse GUI. If I get requests or issues for this I will happily work on them.

## Versions
* 2.0 (Next version, **trunk**)
    * Major Rewrite!
    * Program renamed
    * First version with full linux & windows compatibility!
* 1.5.1
    * Fixes a bug where nothing would encode when using non-recursive (-r & --recursive)
* 1.5
    * Takes the preset as a flag, and will default to Apple > Universal as its default encoding preset.
    * If run without the in and out flags the sparse GUI will come up to prompt.
    * Ability to disable recursive directory reading with a flag
    * Use --help or -h to see command line options.
* 1.0
    * This version is CLI with a option sparse GUI for selecting folders and errors.
    * It only uses the AppleTV 2 preset.
    * This version is currently only for Mac OS X

## Usage
1. Download HandBrakeCLI from http://handbrake.fr/downloads2.php
2. Install
    * Windows users should put HandBrakeCLI.exe in the SAME directory as the script
    * Mac OS X users should install it in /Applications
    * Unix/Linux users should put it anywhere in path
2. Run this script from the command line or double click for GUI mode
3. Enjoy