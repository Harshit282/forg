from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
from PyQt5.QtGui import *
import buttons
import os


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('HAZEL')
        main_window_vbox = QVBoxLayout()
        # vbox = QVBoxLayout()     can be used later if needed....
        hbox = QHBoxLayout()
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
        icon1_hbox.addStretch(stretch=1)
        folders_label = QLabel("Folders")
        listbox = QListWidget()
        listbox.setMinimumHeight(20)
        panel1_vbox.addLayout(icon1_hbox)
        panel1_vbox.addWidget(folders_label)
        panel1_vbox.addWidget(listbox)

        # Panel 2 starts from here...

        icon2_hbox.addWidget(btn2)
        icon2_hbox.addStretch(stretch=1)
        panel2_vbox.addLayout(icon2_hbox)

        rules_label = QLabel("Rules")
        panel2_vbox.addWidget(rules_label)

        chk_vbox.addSpacerItem(QSpacerItem(150, 350))
        panel2_vbox.addLayout(chk_vbox)

        # Panel 3 starts from here...

        icon3_hbox.addStretch(stretch=1)
        icon3_hbox.addWidget(btn3)
        panel3_vbox.addLayout(icon3_hbox)

        label_panel3 = QLabel("NAME: ")
        line_edit = QLineEdit()
        panel3_hbox.addWidget(label_panel3)
        panel3_hbox.addWidget(line_edit)
        panel3_vbox.addLayout(panel3_hbox)

        listbox1 = QListWidget()
        listbox1.insertItem(0, "red")
        listbox1.insertItem(2, "blue")
        listbox1.insertItem(0, "green")
        listbox1.insertItem(0, "yellow")
        listbox1.setMinimumWidth(900)
        panel3_vbox.addWidget(listbox1)

        # bottom buttons...

        save_btn = QPushButton("Save")
        discard_btn = QPushButton("Discard")
        btm_hbox.addStretch(stretch=1)
        btm_hbox.addWidget(save_btn)
        btm_hbox.addWidget(discard_btn)

        # Buttons/Icons clicked actions are defined here...
        # They have been imported from buttons python file...
        def update_folder_list():
            listbox.insertItem(0, buttons.selected_folders)

        btn1.clicked.connect(buttons.add_folder_clicked)
        btn1.clicked.connect(update_folder_list)

        def update_rule_list():
            checkbox = QCheckBox('new rule')
            chk_vbox.addWidget(checkbox)

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

        listbox.itemClicked.connect(selectionChanged)

        # Packing layouts into the main window which is in vertical layout...

        all_panel_hbox.addLayout(panel1_vbox)
        all_panel_hbox.addLayout(panel2_vbox)
        all_panel_hbox.addLayout(panel3_vbox)
        main_window_vbox.addLayout(hbox)
        main_window_vbox.addLayout(all_panel_hbox)
        main_window_vbox.addLayout(btm_hbox)

        self.setLayout(main_window_vbox)
