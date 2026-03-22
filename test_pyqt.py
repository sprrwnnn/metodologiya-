import sys
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("PyQt5 работает!")
label.show()
sys.exit(app.exec_())
