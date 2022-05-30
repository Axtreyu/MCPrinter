import time
import pyautogui
from PIL import Image
from operator import attrgetter

time.sleep(2)
pyautogui.PAUSE = 0
COLOURS = []
class Colour:
    def __init__(self, strname, colour):
        self.strname = strname
        self.colour = colour
        COLOURS.append(self)
    def getdif(self, other):
        self.totaldif = 0
        for i in range(0,3):
            if self.colour[i] >= other[i]: self.totaldif += self.colour[i] - other[i]
            else: self.totaldif += other[i] - self.colour[i]
with open("colours.txt", "rt") as f:
    content = f.read()
    exec(content,globals())
def getPixels(filename):
    img = Image.open(filename)
    w, h = img.size
    pix = list(img.getdata())
    return [pix[n:n+w] for n in range(0, w*h, w)]

pixels = getPixels(f"{input('File_Path: ')}")
outputname = input("File Name: ")

CMDs = []

xoffset = 0
yoffset = -1
zoffset = 0
for x in pixels:
    for block in x:
        [i.getdif(block) for i in COLOURS]
        templist = []
        [templist.append(i.totaldif) for i in COLOURS]
        optimal = min(templist)
        optimal = templist.index(optimal)
        optimal = COLOURS[optimal].strname
        CMDs.append(f"setblock ~{xoffset}~{yoffset}~{zoffset} {optimal}")
        xoffset += 1
    xoffset = 0
    zoffset += 1
if len(CMDs) > 10000:
    print("CMD FUNCTION LIMIT REACHED : SEPERATING FILES")
    b = 0
    e = 10000
    filecontents = []
    tobreak = False
    while True:
        filecontents.append(CMDs[b:e])
        b = e
        if e+10000 >= len(CMDs):
            e = len(CMDs)-1
            tobreak = True
        else:
            e+=10000
        if tobreak: break
    for index_,i in enumerate(filecontents):
        i = "\n".join(i)
        with open(f"{outputname}{index_}.mcfunction","w") as f:
            f.write(i)
    print("BUILDING PACKER...")
    with open(f"{outputname}_PACKER.mcfunction","w") as f:
        for i in range(len(filecontents)):
            f.write(f"execute @s ~~~ function {outputname}{i}\n")
    print("PACKER BUILT.")
else:
    CMDs = "\n".join(CMDs)
    with open(f"{outputname}.mcfunction","w") as f:
        f.write(CMDs)
