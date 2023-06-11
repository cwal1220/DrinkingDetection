import sys
import signal
from MainWidget import MainWidget
from PyQt5.QtWidgets import *

signal.signal(signal.SIGINT, signal.SIG_DFL)
app = QApplication(sys.argv)
w = MainWidget()
w.show()
w.showFullScreen()
sys.exit(app.exec())
