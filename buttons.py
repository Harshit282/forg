from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os

selected_folders = ''

a = dict()


def add_list_items(name, path):
    a[name] = path

def add_folder_clicked():
    global selected_folders
    folder_name = QDir(QFileDialog.getExistingDirectory())
    selected_folders = folder_name.dirName()
    add_list_items(selected_folders, folder_name.path())


def resume_pause_clicked():
    print("Hello u added me")


def save_button_clicked():
    print("Hello u added me")


def discard_button_clicked():
    print("Hello u added me")
