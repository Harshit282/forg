import shutil
import os
import sys
from send2trash import send2trash


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
    pass
    # print(op)
    # # os.chdir(op)  # path here...
    #
    # for count, f in enumerate(os.listdir()):
    #     f_name, f_ext = os.path.splitext(f)
    #     f_name = str(rename_text) + str(count)  # here instead of geek pass the value of line edit...
    #
    #     new_name = f'{f_name}{f_ext}'
    #     os.rename(f, new_name)
