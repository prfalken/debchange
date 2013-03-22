#!/usr/bin/python

import os, tempfile
from subprocess import call
import shutil
import sys
import re
import time

EDITOR = os.environ.get('EDITOR','vim')

# read changelog file
if os.path.exists("debian/changelog"):
	with open('debian/changelog') as f:
		changelog_content = f.read()
else:
	print "You must run debchange.py in a source package containing debian/changelog"
	sys.exit(1)

# Get original information ( package_name (version) distrib; urgency )
first_line = changelog_content.split('\n')[0].strip()
template = re.compile(r"^(?P<pkg_name>.*) \((?P<pkg_version>.*)\) (?P<pkg_distrib>.*); (?P<pkg_urgency>.*)$" )
m = template.match(first_line)
info = m.groupdict()

# Get environment values for template
info['debfullname'] = os.environ.get('DEBFULLNAME', 'Firstname Lastname')
info['debemail'] = os.environ.get('DEBEMAIL', 'name@example.org')
# date format example: Fri, 13 Jul 2012 15:05:04 +0200
info['debian_formatted_date'] = time.strftime("%a, %d %b %Y %H:%M:%S +0200", time.localtime())

# Templated Changelog Entry 
template = """%(pkg_name)s (%(pkg_version)s) %(pkg_distrib)s; urgency=low

  * 

 -- %(debfullname)s <%(debemail)s>  %(debian_formatted_date)s

"""

pushed_content = template %info + changelog_content

with tempfile.NamedTemporaryFile() as f:

	# Write template contents
	f.write(pushed_content)
	f.flush()

	# Spawn Editor 
  	call([EDITOR, f.name])

	# Copy new file 
	shutil.copyfile(f.name, "debian/changelog")
