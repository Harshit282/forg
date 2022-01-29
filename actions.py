import shutil
import os
import sys
from send2trash import send2trash
from PyQt5.QtCore import QDir, QFileInfo


def move(op, tp):
    shutil.move(op, tp)   # first file to be copied path... then destination path...


def copy(op, tp):
    shutil.copy2(op, tp)  # first file to be copied path... then destination path...


def delete(op):
    os.remove(op)  # Enter Path of file to be deleted permanently here...


def trash_bin(op):
    # deleting the file
    if sys.platform == 'win32':
        send2trash("\\".join(op.split("/")))  # pass file path name here...
    else:
        send2trash(op)


def rename(op, rename_text):
    fi = QFileInfo(op)
    directory = fi.dir().path()
    ext = fi.completeSuffix()
    # It omits '.', so add it if suffix wasn't empty
    if ext:
        ext = '.' + ext
    # \ on Windows, / on others
    os_path_separator = QDir.separator()
    tp = directory + os_path_separator + rename_text + ext
    counter = 1
    # Check whether such file already exists
    while os.path.exists(tp):
        # Add number in front if it does
        filepath = directory + os_path_separator + rename_text
        tp = filepath + "(" + str(counter) + ")" + ext
        counter += 1

    # Finally call rename
    os.rename(op, tp)
