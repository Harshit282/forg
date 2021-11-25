import hazprac
import buttons
import os
import Rules

combobox_value = ''
combobox1_value = ''
combobox2_value = ''
date_widget_value = ''
line_edit_value = ''
original_path = r''
target_path = r''


def conditions_applied():
    for subdir, dirs, files in os.walk(original_path):
        for file in files:
            a = os.path.join(subdir, file)
            if a.endswith(combobox1_value):
                # print(a)
                if combobox2_value == 'Copy':
                    Rules.copy(a, target_path)
                elif combobox2_value == 'Move':
                    Rules.move(a, target_path)
                elif combobox2_value == 'Delete':
                    Rules.delete(a)
                elif combobox2_value == 'Trash Bin':
                    Rules.trash_bin(a)

