#!/usr/bin/env python3
# Python3
#
#   A simple script that vizualises a DNA sequence from FASTA file to a PNG image
#   Programmed by /u/logwet with the help of several stackexchange commenters :)
#

import logging
from argparse import ArgumentParser
from copy import deepcopy, copy
from datetime import timedelta
from math import ceil
from os import remove, makedirs
from os.path import exists
from re import sub
from time import time

from PIL import Image, ImageDraw

from largearray import Array

uuid = id(time())

parser = ArgumentParser()
parser.add_argument("file", help="Location of input file. path/to/file (FASTA file formats supported)")
parser.add_argument("-i", "--image-name",
                    help="Where to save finished image file. path/to/file (Default: Name_of_input_file.png)")
parser.add_argument("-s", "--dump-size", help="The size of temp files to dump to disk. (Default & Max: 5)", type=int)
parser.add_argument("-t", "--temp", help="Where to dump temp files. path/to/directory/ (Default: .cache/)", type=str)
parser.add_argument("-d", "--debug-file", help="Where to store debug file. path/to/file (Default ./cache/debug.log")
args = parser.parse_args()
filepath = args.file
ipath = ".".join(filepath.split(".")[:-1]) + ".png"
if args.image_name:
    ipath = args.image_name
print(ipath)
dsize = 5
if args.dump_size:
    dsize = args.dump_size
cachedir = ".cache/"
if args.temp:
    cachedir = args.temp
debugpath = '.cache/debug%d.log' % uuid
if args.debug_file:
    debugpath = args.debug_file
if not exists(filepath):
    raise Exception("Path of input file does not exist")
print("Debug at %s" % debugpath)
if exists(debugpath):
    remove(debugpath)
if not exists(cachedir):
    makedirs(cachedir)
logging.basicConfig(filename=debugpath, level=logging.DEBUG)
logging.info("Init: %d" % uuid)

del parser, ArgumentParser, remove, exists,

print("Generating vizualization of %s" % filepath)
starttime = time()
file = open(filepath, 'r')
logging.info("File opened")
logging.info("Serializing %s ..." % filepath)
raw = ''.join([n for n in file.readlines() if not n.startswith('>')]).replace('\n', "").lower()
logging.info("Replaced FASTA info")
file.close()
del file
raw = sub(r'[rykmswbdhv-]', "n", raw)  # Handles miscellaneous FASTA characters
raw = sub(r'[^atgcn]', "", raw)  # Handles 4 bases and not-known

sequence = Array(name="sequence", cachedirectory=cachedir, a=list(raw), maxitems=(dsize * 10))
sequence.trim()
logging.info("Parsed characters (%d items)" % len(sequence))
del sub, raw
endtime = [time()]
print("The input file has been serialized. %s (%d items) Calculating path..." % (
    str(timedelta(seconds=(endtime[0] - starttime))), len(sequence)))

action = {  # The different bases and their respective colours and movements
    "a": ((0, 255, 0), 0, -1),  # green - Moves up
    "t": ((255, 0, 0), 0, 1),  # red - Moves Down
    "g": ((255, 0, 255), -1, 0),  # hot pink - Moves Left
    "c": ((0, 0, 255), 1, 0),  # blue - Moves Right
    "n": ((0, 0, 0), 0, 0),  # black - Stays on spot
}

maxp = [[0, 0], [0, 0]]  # Top left and bottom right corners of completed path
curr = [0, 0]

pendingactions = Array(name="pendingactions", cachedirectory=cachedir, maxitems=dsize)
logging.info("%d temp files will be created [pendingactions]" % ceil(len(sequence) / pendingactions.maxitems))

for i in sequence:
    # get the actions associated from dict
    curr[0] += action[i][1]
    curr[1] += action[i][2]
    if curr[0] > maxp[0][0]:
        maxp[0][0] = curr[0]
    elif curr[0] < maxp[1][0]:
        maxp[1][0] = curr[0]
    if curr[1] > maxp[0][1]:
        maxp[0][1] = curr[1]
    elif curr[1] < maxp[1][1]:
        maxp[1][1] = curr[1]
    pendingactions.append((copy(curr), action[i][0]))
pendingactions.trim()
del sequence.a
del sequence, copy, deepcopy

# Final dimensions of image + 10px border
dim = (abs(maxp[0][0] - maxp[1][0]) + 20, abs(maxp[0][1] - maxp[1][1]) + 20)
endtime.append(time())
print("The path has been calculated. %s Rendering image... %s" % (
    str(timedelta(seconds=(endtime[1] - starttime))), "(" + str(dim[0]) + "x" + str(dim[1]) + ")"))

with Image.new("RGBA", dim, None) as img:
    logging.info("Initial image created. (%d x %d)" % (dim[0], dim[1]))
    draw = ImageDraw.Draw(img)
    logging.info("Draw object created")

    for i in pendingactions:
        draw.point((i[0][0] + abs(maxp[1][0]) + 10, i[0][1] + abs(maxp[1][1]) + 10), fill=i[1])
    logging.info("Path Drawn")


    def mean(n):  # I couldn't find an average function in base python
        s = float(n[0] + n[1]) / 2
        return s


    # Start and End points are dynamically sized to the dimensions of the final image
    draw.ellipse([((abs(maxp[1][0]) + 10) - ceil(mean(dim) / 500), (abs(maxp[1][1]) + 10) - ceil(mean(dim) / 500)),
                  ((abs(maxp[1][0]) + 10) + ceil(mean(dim) / 500), (abs(maxp[1][1]) + 10) + ceil(mean(dim) / 500))],
                 fill=(255, 255, 0), outline=(255, 255, 0))  # yellow
    draw.ellipse([((curr[0] + abs(maxp[1][0]) + 10) - ceil(mean(dim) / 500),
                   (curr[1] + abs(maxp[1][1]) + 10) - ceil(mean(dim) / 500)), (
                      (curr[0] + abs(maxp[1][0]) + 10) + ceil(mean(dim) / 500),
                      (curr[1] + abs(maxp[1][1]) + 10) + ceil(mean(dim) / 500))], fill=(51, 255, 255),
                 outline=(51, 255, 255))  # neon blue
    logging.info("Start and End points drawn")

    del pendingactions.a
    del maxp, curr, mean, dim, draw, ImageDraw, pendingactions

    endtime.append(time())
    print("The image has been rendered. %s Saving..." % str(timedelta(seconds=(endtime[2] - endtime[1]))))
    img.save(ipath, "PNG", optimize=True)
    logging.info("Image saved at %s" % ipath)

endtime.append(time())
del img, Image
print("Done! %s Image is saved as: %s" % (str(timedelta(seconds=(endtime[3] - endtime[2]))), ipath))
print("Program took %s to run" % str(timedelta(seconds=(endtime[3] - starttime))))
logging.info("%s | %s | %s | %s # Parsing File | Computing Path | Rendering | Saving" % (
    str(timedelta(seconds=(endtime[0] - starttime))), str(timedelta(seconds=(endtime[1] - starttime))),
    str(timedelta(seconds=(endtime[2] - starttime))), str(timedelta(seconds=(endtime[3] - starttime)))))
