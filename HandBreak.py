#!/usr/bin/env python
# encoding: utf-8
"""
Hand Break
Bulk encoder frontend for HandBreakCLI.
This is designed to help batch encode chunks of videos without having to
 constantly use custom one line bash scripts. It uses presets to simplify the
 process.
When run with no flags it gives a nice sparse GUI but you can run it fully
 headless by running it with -i and -o flags. Check --help for all flags.

Created by David "BunnyMan" on 2011-08-13.
Copyright (c) 2011 White Rabbit Code. All rights reserved.
"""

from __future__ import print_function
import sys
import os
import re
from subprocess import call, check_output, Popen, STDOUT, PIPE
import argparse
import traceback


class HandbrakeError(Exception):
    """
    The exception used for handbrake specific errors.
    """
    pass


class HandBrake(object):
    """
    API to HandBreakCLI
    Locates the binary and offers access to it's presets and encoding

    Example;
    hb = Handbrake()
    validPresetsTuple = hb.presets()
    if hb.is_valid_preset('My Preset'):
        success = hb.encode('C:\in\MyVid.avi', 'C:\Videos', 'My Preset')
    """

    def __init__(self):
        self._handBrakeCLI = self.find_handbrake()
        self._validPresets = self.get_presets()

    def presets(self):
        """
        Return a Tuple of the valid presets for this handbrake instance
        """
        return self._validPresets

    def is_valid_preset(self, preset):
        """
        Verify that the preset is valid in the current copy of HandBrakeCLI
        Returns True or False
        """
        if preset in self._validPresets:
            return True
        else:
            return False

    def encode(self, inFile, outFile, preset, output=sys.stdout):
        """
        Encode inFile to outFile with preset.
        Preset must be a valid preset as listed from self.presets()

        Optionally you can pass it a file handle to write all the output too

        Raises HandBreakError if preset is not valid
        """
        if not self.is_valid_preset(preset):
            raise HandbrakeError("Supplied preset not valid")
        returnCode = False
        process = Popen([self._handBrakeCLI, '-v', '0', '-m',
                         '-Z', preset,
                         '-i', inFile, '-o', outFile],
            stderr=STDOUT, stdout=PIPE)
        while process.returncode is None:
            line = process.stdout.readline().strip()
            print(line, file=output)
            if line == "Rip done!":
                returnCode = True
            process.poll()
        return returnCode

    def find_handbrake(self):
        """
        Finds and returns the handbrake binary as string.
        It uses brute force but it should be OS agnostic.
        Should be private.
        """
        if sys.platform == 'win32':
            if os.path.isfile("HandBrakeCLI.exe"):
                return os.path.abspath("HandBrakeCLI.exe")
            else:
                raise HandbrakeError(
                    "HandbrakeCLI.exe not installed next to script!")
        elif os.path.isfile("/Applications/HandBrakeCLI"):
            return "/Applications/HandBrakeCLI"
        elif call(['which', '-s', 'HandBrakeCLI']):
            output = check_output(['which', 'HandBrakeCLI'])[0]
            return output.strip()
        else:
            raise HandbrakeError("HandbrakeCLI not installed!")

    def get_presets(self):
        """
        Calls the HandBrakeCLI executable and returns all of it's valid
        presets.
        It's expensive so it shouldn't really be called more than once in an
        objects lifetime.
        Should be private.
        """
        output = check_output([self._handBrakeCLI, '--preset-list'],
            stderr=STDOUT)
        pattern = re.compile('\+ ([\w\s]+):')
        return tuple(re.findall(pattern, output))


def parse_arguments():
    """
    Set up all the arguments the program takes, parse the programs arguments,
     and then return the results of parse_args()
    """
    parser = argparse.ArgumentParser(description="Batch encode a directory of\
        video files using handbrake presets")
    parser.add_argument('--in-directory', '-i',
        help="Input directory. You need both -in & -out to run headless")
    parser.add_argument('--out-directory', '-o',
        help="Output directory. You need both -in & -out to run headless")
    parser.add_argument('--recursive', '-r', action='store_false',
        default=True, help="DISABLE recursive scanning of input directory")
    parser.add_argument('--preset', '-p', default='Universal',
        help="Handbrake preset to use, defaults to Apple Universal")
    parser.add_argument('--list-presets', '-l', action='store_true',
        help="List available presets and quit")
    return parser.parse_args()


def print_presets(output=sys.stdout):
    """
    Print the available presets and more info message to output
    """
    handbrake = HandBrake()
    presetTuple = handbrake.presets()
    print("Available presets; {}.".format(", ".join(presetTuple)), output)
    print("Please check HandBrake for more information.", output)


def check_valid_preset(preset):
    """
    Return boolean to denote valid HandBrake preset
    """
    handbrake = HandBrake()
    return handbrake.is_valid_preset(preset)


def get_recursive_files(directory):
    """
    Crawl the supplied path and return a list of the files
    """
    fileArray = []
    for (directory, subdirectories, files) in os.walk(directory):
        for filename in files:
            fileArray.append(os.path.join(directory, filename))
    return fileArray


def get_output_file(inFile, outDirectory):
    """
    Take the input the file and the desired output directory, using both to
     generate the output file, with full path.
    inFile can be just a filename or have the path to the file in it.
    """
    inFileName = os.path.basename(inFile)
    outFileName = os.path.splitext(inFileName)[0] + ".m4v"
    return os.path.join(outDirectory, outFileName)


def gui_main(arguments):
    """
    This is the gui version, it will prompt for what information it needs
    and also uses pop ups to display errors
    """
    import Tkinter
    import tkMessageBox
    import tkFileDialog
    root = Tkinter.Tk()
    root.withdraw()
    inDirectory = tkFileDialog.askdirectory(title="Pick Video Directory",
        mustexist=True)
    outDirectory = tkFileDialog.askdirectory(title="Pick Output Directory",
        mustexist=False)
    if not inDirectory or not outDirectory:
        tkMessageBox.showerror(
            "Hand Break It",
            "You have to select both in and out directories")
        return 1
    if not os.path.isdir(outDirectory):
        os.makedirs(outDirectory)

    if arguments.recursive:
        videos = get_recursive_files(inDirectory)
    else:
        videos = [os.path.join(inDirectory, videoFile) for
                  videoFile in os.listdir(inDirectory)]

    try:
        for episode in videos:
            outFile = get_output_file(episode, outDirectory)
            handbrake = HandBrake()
            handbrake.encode(episode, outFile, arguments.preset)
    except OSError, errorMessage:
        tkMessageBox.showerror(
            "Hand Break It",
            "I had a directory access error: {}".format(errorMessage))
        return 1
    except HandbrakeError, errorMessage:
        tkMessageBox.showerror(
            "Hand Break It",
            "HandBrake had an error: {}".format(errorMessage))
        return 1
    except Exception:
        tkMessageBox.showerror(
            "Hand Break It error",
            "I had an error:\n {}".format(traceback.format_exc()))
        return 1
    tkMessageBox.showinfo("Done",
        "I am done!\nCheck the Log for details")
    return 0


def cli_main(arguments):
    """
    Bypassing all the heavy gui this is designed for quick batches and no
     prompts, assuming everything needed was supplied to argsparse.
    """
    inDirectory = os.path.expanduser(arguments.in_directory)
    outDirectory = os.path.expanduser(arguments.out_directory)
    if not os.path.isdir(outDirectory):
        os.makedirs(outDirectory)
    if arguments.recursive:
        videos = get_recursive_files(inDirectory)
    else:
        videos = [os.path.join(inDirectory, videoFile) for
                  videoFile in os.listdir(inDirectory)]
    try:
        for episode in videos:
            outFile = get_output_file(episode, outDirectory)
            handbrake = HandBrake()
            handbrake.encode(episode, outFile, arguments.preset)
    except OSError, errorMessage:
        print("I had a directory access error: {}".format(errorMessage))
        return 1
    except HandbrakeError, errorMessage:
        print("HandBrake had an error: {}".format(errorMessage))
        return 1
    except Exception:
        print("I had an error:\n {}".format(traceback.format_exc()))
        return 1

    print("I am done.", "Check the Log for details", sep="/n")
    return 0

if __name__ == '__main__':
    args = parse_arguments()
    if args.list_presets:
        print_presets()
        sys.exit(0)
    if not check_valid_preset(args.preset):
        print("\"{}\" is not in the valid preset list".format(
            args.preset))
        print_presets()
        sys.exit("9")
    if args.in_directory and args.out_directory:
        sys.exit(cli_main(args))
    else:
        sys.exit(gui_main(args))
