import os


def remove_file(file):
    try:
        if hasattr(file, 'path'):
            os.remove(file.path)
        else:
            os.remove(file)
    except:
        pass