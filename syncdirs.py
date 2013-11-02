#!/cygdrive/c/Python26/python

import os
from os import system
from os import path
import sys
from optparse import OptionParser

usage = 'usage: ' + path.basename(sys.argv[0]) + ' source destination'
parser = OptionParser(usage)

music_types = [ ".mp3", ".m4a" ]

parser.add_option(
	'-p', 
	'--preview',
	action='store_true', 
	dest='preview', 
	default=False,
	help='show which files would be copied, but don\'t copy anything'
)

parser.add_option(
	'-f', 
	'--flatten',
	action='store_true', 
	dest='flatten', 
	default=False,
	help='if this flag is set, the destination dir is expected to be flat with no subdirectories, and all files will put put into it. If a duplicate name is found, it is ignored'
)
				  
parser.add_option(
	'-m', 
	'--music-only',
	action='store_true', 	
	dest='music_only',
	default=False,
	help='only sync .mp3 and .m4a files'
)

(options, args) = parser.parse_args()
 
from_dir = args[0]
to_dirs = args[1:]

if options.preview:
	print '***** START PREVIEW *****'

# for every file in every directory starting at from_dir and descending recursively
for root, dirs, files in os.walk(from_dir):
	for file in files:
		# for each directory we've been asked to sync to
		for to_dir in to_dirs:
			_, ext = os.path.splitext(file)
			
			# if we asked for music only and this isn't a music type, skip
			if options.music_only and ext not in music_types:
				continue
			
			# construct a 'from path' ex: 
			# if from_dir is C:\foo this could be something like C:\foo\bar\file.mp3
			from_path = path.join(root, file)
			
			# if the flatten option is specified, copy the file directly into the 'to_dir' ex:
			if options.flatten:
				to_path = to_dir			
			else:
				# get the relative path from from_dir, ex:
				# if root is C:\foo\bar and from_dir is C:\foo, this would get us bar
				relative_path = path.relpath(root, from_dir)

				# construct our destination directory, ex:
				# if the to_dir is G:\foo_backup, this would get us G:\foo\bar\
				to_path = path.join(to_dir, relative_path)
			
			# construct our final desination path, ex: G:\foo_backup\bar\file.mp3
			to_file = path.join(to_path, file)

			# if this file doesn't already exist in the destination, copy it
			if not path.exists(to_file): 
			
				# tell the user what we're about to do
				command = 'xcopy "%s" "%s"\\ /E /H' % (from_path, to_path)
				prettyCommand = 'copy "%s to %s"' % (from_path, to_path)
				print prettyCommand
				print

				# don't actually run the command if 'preview' is specified
				if not options.preview:
					system(command)

if options.preview:
	print '***** END PREVIEW *****'
	