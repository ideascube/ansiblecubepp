from sys import argv
from subprocess import Popen

# Expected language list is in the form "fr,es,en,". Make it a real python list
# Only two arguments are expected. First is list of languages, second is the mount point where they are accessible from.
langs = argv[1].rstrip(",").split(",")
source = argv[2].rstrip("/")

# Make sure all needed folders are there
folder_list = ["/tmp/overlay", "/tmp/overlay/work", "/tmp/overlay/upper", "/root/.kolibri/content"]
for f in folder_list:
    if not os.path.exists(f):
        os.makedirs(f)

# Mount tmpfs
Popen("mount -t tmpfs tmpfs /tmp/overlay")

# Build overlay command
upperdir = "/tmp/overlay/upper"
workdir = "/tmp/overlay/work"
merged = "/root/.kolibri/content"
lowerdir = str()

for lang in langs:
    lowerdir += source + "/" + lang + ":"

lowerdir = lowerdir.rstrip(":")

fullcommand = "mount -t overlay overlay -o lowerdir=" + \
              lowerdir + ",upperdir=" + upperdir + ",workdir=" + workdir + \
              " " + merged

# Mount overlay
Popen(fullcommand)
