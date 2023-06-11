import sys
import os
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

from HomeWidget import HomeWidget
from LoginWidget import LoginWidget
from RegisterWidget import RegisterWidget
from IgnitionWidget import IgnitionWidget

# QT Keyboard 사용 환경
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('MainWidget.ui', self)
        self.homeWidget = HomeWidget()
        self.loginWidget = LoginWidget()
        self.registerWidget = RegisterWidget()
        self.ignitionWidget = IgnitionWidget()
        self.homeWidget.widgetMoveSignal.connect(self.widgetMoveSlot)
        self.loginWidget.widgetMoveSignal.connect(self.widgetMoveSlot)
        self.registerWidget.widgetMoveSignal.connect(self.widgetMoveSlot)
        self.ignitionWidget.widgetMoveSignal.connect(self.widgetMoveSlot)
        self.stackedWidget.insertWidget(0, self.homeWidget)
        self.stackedWidget.insertWidget(1, self.loginWidget)
        self.stackedWidget.insertWidget(2, self.registerWidget)
        self.stackedWidget.insertWidget(3, self.ignitionWidget)
        self.stackedWidget.setCurrentIndex(0)

    @pyqtSlot()
    def onNextButtonClicked(self):
        self.stackedWidget.setCurrentIndex(0)
    
    @pyqtSlot(int)
    def widgetMoveSlot(self, widgetIndex):
        self.stackedWidget.setCurrentIndex(widgetIndex)


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    w.showFullScreen()
    sys.exit(app.exec())
