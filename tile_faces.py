# -*- Mode: Python -*-

import Image
import ImageDraw

import os
import sys

W = sys.stderr.write

PJ = os.path.join

path = sys.argv[1]
imgs = []
for p in os.listdir (path):
    p0 = PJ (path, p)
    if os.path.isfile (p0):
        try:
            Image.open (p0)
            imgs.append (p0)
        except:
            pass

nimg = len(imgs)

W ('%d images...\n' % (nimg,))

# base size: 120x120
# 1800 wide will hold 15
base = 120
rows, left = divmod (nimg, 15)
# let's not make a partial row...
if left:
    rows += 1

work = imgs[:]

# now we know how many images we have to work with
index = Image.new ("RGB", (15 * base, rows * base), (255, 255, 255))
for y in range (rows):
    for x in range (15):
        try:
            name = work.pop(0)
            im = Image.open (os.path.join (path, name))
            im.thumbnail ((base, base))
            where = base*x, base*y
            W ('%r ' % (where,))
            index.paste (im, where)
        except IndexError:
            break
    W ('\n')

index.save ('tiled.jpg')
