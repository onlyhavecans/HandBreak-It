#!/usr/bin/env python
# encoding: utf-8
"""
Hand Break It
This script is a brisk gui to batch processing of video files to mp4 with the
…AppleTV 2 present using HandBrakeCLI. I'm not writing an encoder in this.
It pretends to be OS agnostic but it's obviously designed for OS X machines.

Created by David "BunnyMan" on 2011-08-13.
Copyright (c) 2011 White Rabbit Code. All rights reserved.
"""

import sys
import os
from subprocess import Popen
import Tkinter
import tkMessageBox
import tkFileDialog
import traceback


class HandbrakeError(Exception):
	pass


class DebugError(Exception):
	pass


def getRecursiveFiles(directory):
	''' This isn't too special really,
	just a copypaste function for crawling a path and getting all the files
	Feed it a directory and it uses os.walk to return array of files
	'''
	pinkiePie = []
	for (dirname, subdirectories, files) in os.walk(directory):
		for filename in files:
			pinkiePie.append(os.path.join(dirname, filename))
	return pinkiePie


def encodeFiles(inDirectory, outDirectory, recursive=True):
	''' This is is the encoder,
		it lists up all the files and runs HandBrakeCLI with the Apple TV 2 Preset
		This is the hook, you like it.
	'''
	handbrakeCLI = '/Applications/HandBrakeCLI'
	if not os.path.isfile(handbrakeCLI):
		raise HandbrakeError(
			'HandbrakeCLI not installed. Please install before running'
		)

	if not os.path.isdir(outDirectory):
		os.path.makedir(outDirectory)

	ponies = []
	if recursive:
		ponies = getRecursiveFiles(inDirectory)
	else:
		ponies = os.listdir(inDirectory)

	for episode in ponies:
		trixie = os.path.basename(episode)
		m4v = trixie[:-4] + '.m4v'
		twilightSparkle = os.path.join(outDirectory, m4v)
		# TODO Make this OS neutral
		# TODO Put in loging to file
		# TODO http://docs.python.org/library/subprocess.html
		Popen([
			handbrakeCLI,
			'-i', episode,
			'-o', twilightSparkle,
			'--preset="AppleTV 2"'
		])

	return(0)


def cli_main(argv=sys.argv):
	root = Tkinter.Tk()
	root.withdraw()
	progname = os.path.basename(argv[0])
	args = argv[1:]

	if len(args) != 2:
		inpath = tkFileDialog.askdirectory(
			title="Pick Video Directory",
			mustexist=True
		)
		outpath = tkFileDialog.askdirectory(
			title="Pick Output Directory",
			mustexist=False
		)
	else:
		(inpath, outpath) = args
	if inpath == "" or outpath == "":
		sys.stderr.write("usage: %s InDirectory OutDirectory\n" % (progname,))
		return 1

	try:
		raise DebugError("Don\'t run the encode process")
		# TODO we need a status window somewhere.
		encodeFiles(inpath, outpath)

	except OSError, e:
		# TODO This has a bug?
		tkMessageBox.showerror(
			"Hand Break It",
			"I had a directory access error: %s" % e  # traceback.format_exc() for debug
		)
		return(1)
	except HandbrakeError, e:
		tkMessageBox.showerror(
			"Hand Break It",
			"HandBrake had an error: %s" % e  # traceback.format_exc() for debug level
		)
		return(1)
	except DebugError, e:
		tkMessageBox.showerror(
			"Hand Break It",
			"Debug Throw: %s" % traceback.format_exc()
		)
		return(1)
	except Exception, e:
		tkMessageBox.showerror(
			"Hand Break It error",
			"I had an error:\n %s" % e  # traceback.format_exc() for debug level
		)
		return(1)

	tkMessageBox.showinfo(
			"Done",
			"I, PhotoFinish, am done.\nCheck the Log for details"
		)
	return 0


if __name__ == '__main__':
	sys.exit(cli_main())

