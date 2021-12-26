import shutil
import os
from send2trash import send2trash

rules_list = []


def move(op, tp):
    shutil.move(op, tp)   # first file to be copied path... then destination path...


def copy(op, tp):
    shutil.copy2(op, tp)  # first file to be copied path... then destination path...


def delete(op):
    os.remove(op)  # Enter Path of file to be deleted permanently here...


def trash_bin(op):
    # deleting the file
    send2trash(op)  # pass file path name here...


def rename(op):
    os.chdir(op)  # path here...

    for count, f in enumerate(os.listdir()):
        f_name, f_ext = os.path.splitext(f)
        f_name = "geek" + str(count)  # here instead of geek pass the value of line edit...

        new_name = f'{f_name}{f_ext}'
        os.rename(f, new_name)
