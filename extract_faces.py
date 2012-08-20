# -*- Mode: Python -*-

# Aperture Face Extractor.
# got some great tips on the Aperture Database Layout from here:
#   http://code.google.com/p/extract-aperture-faces/

import sqlite3
import os
import sys
import time

if len(sys.argv) < 4:
    sys.stderr.write ('Usage: %s <ApertureRoot> <FaceName> <DestinationDirectory>\n' % (sys.argv[0],))
    sys.exit (-1)

lib_root = sys.argv[1]
name = sys.argv[2]
dest = sys.argv[3]

if not os.path.isdir (dest):
    sys.stderr.write ('destination is not a directory?\n')
    sys.exit (-1)

PJ = os.path.join

# unfortunately at this time python cannot use sqlite3_open_v2 which allows read-only access.
faces_db = sqlite3.connect (PJ (lib_root, 'Database/Faces.db'))
main_db  = sqlite3.connect (PJ (lib_root, 'Database/Library.apdb'))

cf = faces_db.cursor()
cm = main_db.cursor()

# At this time (Aperture 3.3.2), the face thumbnails are stored
#  in the 'Previews' subdirectory.  Each thumbnail is recorded as
#  a non-original version of a master image, and is present along
#  with the preview thumbnail in a predictable path: thumb_IMGNAME_faceN.jpg

master_uuids = cf.execute (
    "SELECT a.masterUuid,faceIndex"
    " FROM RKDetectedFace AS a, RKFaceName AS b"
    " WHERE a.faceKey = b.faceKey AND name = '%s'" % name
    )

faces = []
for muuid, face_index in master_uuids:
    for image_date, uuid, path in cm.execute (
            "SELECT b.imageDate, a.uuid, b.imagePath"
            " FROM RKVersion AS a, RKMaster AS b"
            " WHERE a.isOriginal = 0"
            " AND a.masterUuid = b.uuid"
            " AND a.masterUuid = '%s'" % (muuid,)):
        faces.append ((image_date, muuid, face_index, path, uuid))

# for some reason "ORDER BY b.imageDate" doesn't work...
faces.sort()

def get_face_path (p, uuid, index):
    parts = p.split ('/')
    img_path = parts[-1]
    img_base, ext = os.path.splitext (img_path)
    base = '/'.join (parts[:4])
    return PJ (base, uuid, 'thumb_%s_face%d.jpg' % (img_base, index))

previews_root = PJ (lib_root, 'Previews')

i = 0
for _, muuid, face_index, path, uuid in faces:
    p0 = get_face_path (path, uuid, face_index)
    p = PJ (previews_root, p0)
    print p0, os.path.isfile (p)
    p1 = PJ (dest, '%05d.jpg' % (i,))
    open (p1, 'wb').write (open (p).read())
    i += 1
    
sys.stderr.write ("found %d faces...\n" % len(faces),)
