from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class EmptyLabel(QLabel):
    def __init__(self,  message, picture, parent=None):
        super().__init__()
        form = QFormLayout(self)
        image = QLabel()
        art = QPixmap(picture)
        image.setPixmap(art)
        image.setAlignment(Qt.AlignCenter)
        form.addRow(image)
        bottom_text = QLabel(message)
        bottom_text.setAlignment(Qt.AlignCenter)
        form.addRow(bottom_text)
