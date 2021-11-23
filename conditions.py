import hazprac
import buttons
import os
import Rules

combobox_value = ''
combobox1_value = ''
combobox2_value = ''
selected_folder_value = ''
date_widget_value = ''
line_edit_value = ''

files_to_process = dict()
def get_fileinfo(folder):
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            files_to_process[os.path.join(subdir, file)] = os.path.getsize(os.path.join(subdir, file))
def filter_size():
    for k,v in files_to_process.items():
        if v / 1000 < int(combobox1_value):
            Rules.original_path = k
            Rules.target_path = selected_folder_value
            action = combobox2_value.casefold()
            eval("Rules."+ action + "()")

