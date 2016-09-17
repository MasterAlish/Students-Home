import os, sys
from PIL import Image
from django.conf import settings


def image_is_big(media_path, image_len=256):
    infile = os.path.join(settings.MEDIA_ROOT, media_path)
    im = Image.open(infile)
    return im.size[0] > image_len or im.size[1] > image_len


def get_aspect_ratio_size(size, image_len=256):
    max_side = float(max(size[0], size[1]))
    return int(size[0]/max_side * image_len), int(size[1]/max_side * image_len)


def make_image_small(media_path, image_len=256):
    outfile_path = os.path.splitext(media_path)[0]+"_thumb.jpg"
    infile = os.path.join(settings.MEDIA_ROOT, media_path)
    outfile = os.path.join(settings.MEDIA_ROOT, outfile_path)
    if infile != outfile:
        try:
            im = Image.open(infile)
            size = get_aspect_ratio_size(im.size, image_len)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outfile, "JPEG")
            os.remove(infile)
            return outfile_path
        except IOError:
            print "cannot create thumbnail for '%s'" % infile
