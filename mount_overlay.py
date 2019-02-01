#!/usr/bin/python

import os
from sys import argv
from subprocess import call

# Expected language list is in the form "fr,es,en,". Make it a real python list
# Only two arguments are expected. First is list of languages, second is the mount point where they are accessible from.
langs = argv[1].rstrip(",").split(",")
source = argv[2].rstrip("/")

# Mount tmpfs
call("mount -t tmpfs tmpfs /tmp/overlay", shell=True)

# Make sure all needed folders are there
folder_list = ["/tmp/overlay/work", "/tmp/overlay/upper", "/root/.kolibri/content"]
for f in folder_list:
    if not os.path.exists(f):
        os.makedirs(f)

# Build overlay command
upperdir = "/tmp/overlay/upper"
workdir = "/tmp/overlay/work"
merged = "/root/.kolibri/content"
lowerdir = str()

for lang in langs:
    lowerdir += source + "/" + lang + "/content:"

lowerdir = lowerdir.rstrip(":")

fullcommand = "mount -t overlay overlay -o lowerdir=" + \
              lowerdir + ",upperdir=" + upperdir + ",workdir=" + workdir + \
              " " + merged

# Mount overlay
call(fullcommand, shell=True)
