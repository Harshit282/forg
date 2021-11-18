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

        listbox3 = QListWidget()
        panel3_vbox.addWidget(listbox3)

        # bottom buttons...
        save_btn = QPushButton("Save")
        discard_btn = QPushButton("Discard")
        btm_hbox.addStretch()
        btm_hbox.addWidget(save_btn)
        btm_hbox.addWidget(discard_btn)
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
            text, ok = QInputDialog.getText(self,'New rule', 'Enter name:')
            if ok and text:
                checkbox.setText(text)
                listbox2.addItem(checkbox)

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
        all_panel_hbox.setStretchFactor(panel1_vbox,1)
        all_panel_hbox.setStretchFactor(panel2_vbox,1)
        all_panel_hbox.setStretchFactor(panel3_vbox,3)
        main_window_vbox.addLayout(all_panel_hbox)
        main_window_vbox.addLayout(btm_hbox)

        self.setLayout(main_window_vbox)
