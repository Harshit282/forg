from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import Rules
import conditions

selected_folders = ''

a = dict()


def add_list_items(name, path):
    a[name] = path


def add_folder_clicked():
    global selected_folders
    folder_path = QFileDialog.getExistingDirectory()
    folder_name = QDir(folder_path)
    selected_folders = folder_name.dirName()
    Rules.original_path = folder_path
    add_list_items(selected_folders, folder_name.path())


def resume_pause_clicked():
    conditions.filter_size()


def save_button_clicked():
    print("Hello u added me")


def discard_button_clicked():
    print("Hello u added me")
