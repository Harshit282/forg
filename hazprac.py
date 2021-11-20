from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import buttons
import os


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1000, 500)
        self.setWindowTitle('File Organizer')
        main_window_vbox = QVBoxLayout()
        icon1_hbox = QHBoxLayout()
        icon2_hbox = QHBoxLayout()
        icon3_hbox = QHBoxLayout()
        panel1_vbox = QVBoxLayout()
        panel2_vbox = QVBoxLayout()
        panel3_vbox = QVBoxLayout()
        chk_vbox = QVBoxLayout()
        all_panel_hbox = QHBoxLayout()
        btm_hbox = QHBoxLayout()
        panel3_hbox = QHBoxLayout()
        panel3_grid = QGridLayout()
        model = QStandardItemModel()
        model1 = QStandardItemModel()

        btn1 = QPushButton()
        btn2 = QPushButton()
        btn3 = QPushButton()
        btn1.setIcon(QIcon('icons/add folder.png'))
        btn1.setToolTip('Add Folder')
        btn2.setIcon(QIcon('icons/add rule.png'))
        btn2.setToolTip('Add Rule')
        btn3.setIcon(QIcon('icons/pause.png'))
        btn3.setToolTip('Pause')

        # Panel 1 starts from here...

        icon1_hbox.addWidget(btn1)
        icon1_hbox.addStretch()
        folders_label = QLabel("Folders")
        listbox1 = QListWidget()
        panel1_vbox.addLayout(icon1_hbox)
        panel1_vbox.addWidget(folders_label)
        panel1_vbox.addWidget(listbox1)

        # Panel 2 starts from here...

        icon2_hbox.addWidget(btn2)
        icon2_hbox.addStretch()
        panel2_vbox.addLayout(icon2_hbox)

        rules_label = QLabel("Rules")
        panel2_vbox.addWidget(rules_label)

        listbox2 = QListWidget()
        panel2_vbox.addWidget(listbox2)
        listbox2.setLayout(chk_vbox)

        # Panel 3 starts from here...

        icon3_hbox.addStretch()
        icon3_hbox.addWidget(btn3)
        panel3_vbox.addLayout(icon3_hbox)

        label_panel3 = QLabel("NAME: ")
        line_edit = QLineEdit()
        panel3_hbox.addWidget(label_panel3)
        panel3_hbox.addWidget(line_edit)
        panel3_vbox.addLayout(panel3_hbox)

        # Added the third panel window here...
        # Also added the icon to add rules and conditions...
        # Used Grid Layout here...

        panel3_label_rule1 = QLabel('If all of the following conditions are met: ')
        condition_add_button = QPushButton()
        condition_add_button.setIcon(QIcon("icons/add icon.png"))
        condition_remove_button = QPushButton()
        condition_remove_button.setIcon(QIcon("icons/remove icon.png"))
        combobox = QComboBox()
        combobox.setModel(model)
        # combobox1 = QComboBox()
        # combobox1.addItem('is')
        # combobox1.addItem('was')
        combobox1 = QComboBox()
        combobox1.setModel(model)
        condition_combobox_data = {
            'Size': ['<1MB', '<5MB', '<10MB', '<50MB', '<100MB', '<512MB', '<1GB', '<3GB', '>3GB', 'all'],
            'Image Extension': ['.jpg', '.png', '.gif', 'all'],
            'Video Extension': ['.mp4', '.mkv', '.m4p', '.m4v', 'all'],
            'Audio Extension': ['mp3', 'mp4a', 'gig', 'all'],
            'Empty Files': ['0 bytes'],
            'Old Files': ['<1 Month', '<3 Months', '<6 Months', '<1 Year', '>1 Year'],
            'Date Added': []
        }
        for condition_combobox_key, condition_combobox_value in condition_combobox_data.items():
            combobox_item = QStandardItem(condition_combobox_key)
            model.appendRow(combobox_item)
            for value in condition_combobox_value:
                combobox1_item = QStandardItem(value)
                combobox_item.appendRow(combobox1_item)

        def update_combobox1(index):
            indx = model.index(index, 0, combobox.rootModelIndex())
            combobox1.setRootModelIndex(indx)
            combobox1.setCurrentIndex(0)

        combobox.currentIndexChanged.connect(update_combobox1)
        update_combobox1(0)
        # here int values are as row, column, row_span, column_span....
        # Same for the next grid layout...

        panel3_grid.addWidget(panel3_label_rule1, 0, 0, 1, 3)
        panel3_grid.addWidget(condition_remove_button, 1, 3)
        panel3_grid.addWidget(condition_add_button, 1, 4)
        panel3_grid.addWidget(combobox, 1, 0)
        # panel3_grid.addWidget(combobox1, 1, 1)
        panel3_grid.addWidget(combobox1, 1, 1)

        panel3_label_rule2 = QLabel('Do the following to the selected folder/files: ')
        rule_add_button = QPushButton()
        rule_add_button.setIcon(QIcon("icons/add icon.png"))
        rule_remove_button = QPushButton()
        rule_remove_button.setIcon(QIcon("icons/remove icon.png"))
        combobox2 = QComboBox()
        combobox2.setModel(model1)
        # combobox4 = QComboBox()
        # combobox4.addItem('Date Added')
        # combobox4.addItem('nafwn')
        # combobox4.addItem('ad')
        combobox3 = QComboBox()
        combobox3.setModel(model1)
        panel3_grid.addWidget(panel3_label_rule2, 2, 0, 1, 3)
        panel3_grid.addWidget(rule_remove_button, 4, 3)
        panel3_grid.addWidget(rule_add_button, 4, 4)
        panel3_grid.addWidget(combobox2, 4, 0)
        # panel3_grid.addWidget(combobox4, 4, 1)
        panel3_grid.addWidget(combobox3, 4, 1)
        # this dictionary will hold the data for rule combo-boxes...
        # SO CHANGE ACCORDINGLY...
        rule_combobox_data = {
            'Copy': [],
            'Move': [],
            'Delete': [],
            'Rename': [],
            'Trash Bin': []
        }
        for rule_combobox_key, rule_combobox_value in rule_combobox_data.items():
            combobox2_item = QStandardItem(rule_combobox_key)
            model1.appendRow(combobox2_item)
            for values in rule_combobox_value:
                combobox3_item = QStandardItem(values)
                combobox2_item.appendRow(combobox3_item)

        def update_combobox2(index1):
            indx1 = model1.index(index1, 0, combobox2.rootModelIndex())
            combobox3.setRootModelIndex(indx1)
            combobox3.setCurrentIndex(0)

        combobox2.currentIndexChanged.connect(update_combobox2)
        update_combobox2(0)

        panel3_vbox.addLayout(panel3_grid)

        # bottom buttons...

        save_btn = QPushButton("Save")
        discard_btn = QPushButton("Discard")
        btm_hbox.addStretch()
        btm_hbox.addWidget(save_btn)
        btm_hbox.addWidget(discard_btn)
        panel3_vbox.addLayout(btm_hbox)

        # Buttons/Icons clicked actions are defined here...
        # They have been imported from buttons python file...
        def update_folder_list():
            listbox1.insertItem(0, buttons.selected_folders)

        btn1.clicked.connect(buttons.add_folder_clicked)
        btn1.clicked.connect(update_folder_list)

        def update_rule_list():
            checkbox = QListWidgetItem()
            checkbox.setFlags(checkbox.flags() | Qt.ItemIsUserCheckable)
            checkbox.setCheckState(Qt.Unchecked)
            text, ok = QInputDialog.getText(self, 'New rule', 'Enter name:')
            if ok and text:
                checkbox.setText(text)
                listbox2.addItem(checkbox)

        def rule_item_clicked():
            i = listbox2.selectedItems()[0]
            line_edit.setText(i.text())

        listbox2.itemClicked.connect(rule_item_clicked)

        def update_rule_name():
            i = listbox2.selectedItems()[0]
            i.setText(line_edit.text())

        line_edit.editingFinished.connect(update_rule_name)

        btn2.clicked.connect(update_rule_list)
        btn3.clicked.connect(buttons.resume_pause_clicked)
        save_btn.clicked.connect(buttons.save_button_clicked)
        discard_btn.clicked.connect(buttons.discard_button_clicked)

        def selectionChanged(item):
            root_dir = buttons.a.get(item.text())
            for subdir, dirs, files in os.walk(root_dir):
                for file in files:
                    print(os.path.join(subdir, file), "Size of file is: ", os.path.getsize(os.path.join(subdir, file)),
                          "Bytes")

        listbox1.itemClicked.connect(selectionChanged)

        # Packing layouts into the main window which is in vertical layout...

        all_panel_hbox.addLayout(panel1_vbox)
        all_panel_hbox.addLayout(panel2_vbox)
        all_panel_hbox.addLayout(panel3_vbox)
        # Stretch factor of 1,1,3 leads to 20%, 20%, 60% used space
        # for panel 1,2,3 respectively
        all_panel_hbox.setStretchFactor(panel1_vbox, 1)
        all_panel_hbox.setStretchFactor(panel2_vbox, 1)
        all_panel_hbox.setStretchFactor(panel3_vbox, 3)
        main_window_vbox.addLayout(all_panel_hbox)

        self.setLayout(main_window_vbox)
