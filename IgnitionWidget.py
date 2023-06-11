import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *
import os

class IgnitionWidget(QWidget):
    # 위젯 인덱스를 이동할때 방출하는 Signal
    widgetMoveSignal = pyqtSignal(int)

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('IgnitionWidget.ui', self)
        self.homeButton.clicked.connect(self.homeButtonClickSlot)
        self.deleteButton.clicked.connect(self.deleteButtonClickSlot)

    @pyqtSlot()
    def homeButtonClickSlot(self):
        self.widgetMoveSignal.emit(0)

    @pyqtSlot()
    def deleteButtonClickSlot(self):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to remove all user information?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print('yes')
            os.system("rm -rf faces/*.png")



if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    w = IgnitionWidget()
    w.show()
    # w.ui.showFullScreen()
    sys.exit(app.exec())
