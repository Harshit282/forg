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
    # \ on Windows, / on others
    os_path_separator = QDir.separator()
    tp = directory + os_path_separator + rename_text
    # Finally call rename
    os.rename(op, tp)
