from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import conditions


class PreviewDialog(QDialog):
    def __init__(self,  title, message, items, parent=None):
        super().__init__()
        form = QFormLayout(self)
        form.addRow(QLabel(message))
        self.listView = QListView(self)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        form.addRow(self.listView)
        model = QStandardItemModel(self.listView)
        self.setWindowTitle(title)
        for file in conditions.files:
            standardItem = QStandardItem(file)
            model.appendRow(standardItem)
        self.listView.setModel(model)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok,self)
        form.addRow(buttonBox)
        buttonBox.accepted.connect(self.accept)
