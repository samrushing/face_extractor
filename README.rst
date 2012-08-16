face_extractor
==============

Extract thumbnails from Aperture's Face Database.

Usage::

  $ mkdir jill_faces
  $ python extract_faces.py /Volumes/pics/ApertureLibrary.aplibrary/ jill jill_faces

That will fill the directory jill_faces with all the confirmed face thumbnails.

To plunk all those into a nice tiled image::

  $ python tile_faces.py jill_faces

It'd be nice to figure out how to use the SimilarFaces table to pull
in all the predicted matches...
