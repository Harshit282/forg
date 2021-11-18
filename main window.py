import sys
import hazprac
from PyQt5.QtWidgets import *


app = QApplication(sys.argv)
window = hazprac.Window()
window.show()
sys.exit(app.exec_())
