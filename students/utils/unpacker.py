import os
import shutil
import zipfile

from django.conf import settings


def unpack_resolution_to_public_dir(resolution):
    coursename = "course%d" % resolution.task.course.id
    labname = "lab%d" % resolution.task.id
    username = resolution.student.get_short_name()
    labpath = os.path.join(settings.MEDIA_ROOT, "sites", coursename, labname, username)
    try:
        os.makedirs(labpath)
    except:
        pass
    try:
        shutil.rmtree(labpath)
    except:
        pass
    try:
        zip_ref = zipfile.ZipFile(resolution.file.path)
        zip_ref.extractall(labpath)
        zip_ref.close()
    except Exception as e:
        print "Error: " + repr(e)
    lab_url = os.path.join(settings.MEDIA_URL, "sites", coursename, labname, username, "index.html")
    return lab_url
