import hazprac
import buttons
import os
import Rules
import datetime

combobox_value = ''
combobox1_value = ''
combobox2_value = ''
date_widget_value = ''
line_edit_value = ''
original_path = r''
target_path = r''


def conditions_applied():
    if combobox_value == 'Image Extension' or combobox_value == 'Audio Extension' or combobox_value == 'Video Extension':
        for subdir, dirs, files in os.walk(original_path):
            for file in files:
                a = os.path.join(subdir, file)
                if a.endswith(combobox1_value):
                    if combobox2_value == 'Copy':
                        Rules.copy(a, target_path)
                    elif combobox2_value == 'Move':
                        Rules.move(a, target_path)
                    elif combobox2_value == 'Delete':
                        Rules.delete(a)
                    elif combobox2_value == 'Trash Bin':
                        Rules.trash_bin(a)
                    elif combobox2_value == 'Rename':
                        Rules.rename(a)

    if combobox_value == 'Date Added':
        for subdir, dirs, files in os.walk(original_path):
            for file in files:
                a = os.path.join(subdir, file)
                if date_widget_value == datetime.datetime.fromtimestamp(os.path.getctime(a)).strftime('%d/%m/%Y'):
                    if combobox2_value == 'Copy':
                        Rules.copy(a, target_path)
                    elif combobox2_value == 'Move':
                        Rules.move(a, target_path)
                    elif combobox2_value == 'Delete':
                        Rules.delete(a)
                    elif combobox2_value == 'Trash Bin':
                        Rules.trash_bin(a)
                    elif combobox2_value == 'Rename':
                        Rules.rename(a)

    if combobox_value == 'Empty files':
        pass
    if combobox_value == 'Old Files':
        pass

