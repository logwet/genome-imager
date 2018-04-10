#!/usr/bin/env python
# Python3
#
#   A simple script that vizualises a DNA sequence from .FASTA file to a .png image
#   Programmed by /u/logwet with the help of countless stackexchange commenters :)
#

from PIL import Image, ImageDraw, PngImagePlugin
from re import sub
from time import sleep
Image._initialized=2

path = input("""What is the input file? .fasta format recommended
?> """)
file = open(path,'r')
out = [n for n in file.readlines() if not n.startswith('>')]
file.close()
raw = ''.join(out).replace('\n',"").lower()
del out
raw = sub(r'[rykmswbdhv-]', "n", raw)
raw = sub(r'[^atgcn]', "", raw)
del sub
sequence = list(raw)
del raw

action = {
    "a": [(0,255,0),0,-1], #green
    "t": [(255,0,0),0,1], #red
    "g": [(255,0,255),-1,0], #hot pink
    "c": [(0,0,255),1,0], #blue
    "n": [(0,0,0),0,0], #black
}

count = [[0,0],[0,0]]

start = [0,0]
curr = start[:]

pendingactions = []
for i in sequence:
    #get the actions associated from dict
    actionlist = action[i]
    curr[0] += actionlist[1]
    curr[1] += actionlist[2]
    if curr[0] > count[0][0]:
        count[0][0] = curr[0]
    elif curr[0] < count[1][0]:
        count[1][0] = curr[0]
    if curr[1] > count[0][1]:
        count[0][1] = curr[1]
    elif curr[1] < count[1][1]:
        count[1][1] = curr[1]
    pendingactions.append((curr[:],actionlist[0]))

del sequence

dim = (abs(count[0][0]-count[1][0])+20,abs(count[0][1]-count[1][1])+20)
print("The path has been calculated. The Image is now being generated %s"%("("+str(dim[0])+"x"+str(dim[1])+")"))
img = Image.new("RGBA", dim, None)
draw = ImageDraw.Draw(img)

for i in pendingactions:
    draw.point([i[0][0]+abs(count[1][0])+10,i[0][1]+abs(count[1][1])+10], fill=i[1])

draw.ellipse([(abs(count[1][0])+8,abs(count[1][1])+8),(abs(count[1][0])+12,abs(count[1][1])+12)], fill = (255,215,0), outline = (255,215,0)) #gold
draw.ellipse([(curr[0]+abs(count[1][0])+8,curr[1]+abs(count[1][1])+8),(curr[0]+abs(count[1][0])+12,curr[1]+abs(count[1][1])+12)], fill = (105,5,235), outline = (105,5,235)) #purple

loc = '%s.png'%path.split(".", 1)[0]
img.save(loc)
print("Done! Image is saved as: %s"%loc)
sleep(5)
