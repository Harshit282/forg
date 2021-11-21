import shutil
import os
from send2trash import send2trash

original_path = r''
target_path = r''
path = r''


def move():
    shutil.move(original_path, target_path)   # first file to be copied path... then destination path...


def copy():
    shutil.copy2(original_path, target_path)  # first file to be copied path... then destination path...


def delete():
    shutil.rmtree(path)  # Enter Path of file to be deleted permanently here...


def trash_bin():
    # deleting the file
    send2trash(path)  # pass file path name here...


def rename():
    os.chdir(path)  # path here...

    for count, f in enumerate(os.listdir()):
        f_name, f_ext = os.path.splitext(f)
        f_name = "geek" + str(count)  # here instead of geek pass the value of line edit...

        new_name = f'{f_name}{f_ext}'
        os.rename(f, new_name)
