#!/usr/bin/env python
# /* ex: set tabstop=2 expandtab: */
# /* ex: set shiftwidth=2 expandtab: */
# SpringpadToDayOne.py - Springpad JSON importer for DayOne.app
# Copyright (C) 2014 Nathan Polonski 
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from subprocess import call
from pipes import quote
import sys
import json

dayone = '/usr/local/bin/dayone'
mybuff = 4096

filename = sys.argv[1]
print "Opening %s" % filename
SpringPadFile = open(filename,'r')
SpringPadData = json.loads(SpringPadFile.read())
#print "%s" % SpringPadData

# TODO:
# - Add liked/starred support
# - find a way to detect 'pins' and write the post to match

# Load notes and tags for creation date
incr = 0
for my in SpringPadData:
    incr += 1
    args = ["-d=%s" % (my['created']) ]
    print "%04d - %s : %s : %s (%s)" % (incr, my['name'], my['liked'], my['created'], my['image'])
    if my.has_key('image') and my['image'] != None:
        # Load journal entry with image
        args.extend("-p=%s" % (my['image']))

    call("echo %s | %s %s new" %  (quote(my['text']), dayone, ' '.join(args)), shell=True, bufsize=mybuff )

    if incr > 3:
        break
    
sys.exit(0)
# Load images 
incr = 0
for my in SpringPadData:
    if my.has_key('attachments'):
        for pic in my['attachments']:
            if pic.has_key('image') and pic['image'] != '':
                incr += 1
                print "%04d %s" % (incr, pic['image'])
                call("echo image for %s | %s -d=%s -p=%s new" %  (quote(my['name']), dayone, my['created'], my['image']),shell=True, bufsize=mybuff )

    if incr > 3:
        break
