import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

from managers.SensorManager import SensorManager

class HomeWidget(QWidget):
    # 위젯 인덱스를 이동할때 방출하는 Signal
    widgetMoveSignal = pyqtSignal(int)

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('HomeWidget.ui', self)
        self.loginButton.clicked.connect(self.loginButtonClickSlot)
        self.registerButton.clicked.connect(self.registerButtonClickSlot)
        self.measureButton.clicked.connect(self.measureButtonClickSlot)
        self.sensorManager = SensorManager()
        self.measureTimer = QTimer()
        self.measureTimer.timeout.connect(self.measureTimerSlot)
        self.measureCnt = 0
        self.measureValues = []

    @pyqtSlot()
    def loginButtonClickSlot(self):
        self.widgetMoveSignal.emit(1)

    @pyqtSlot()
    def registerButtonClickSlot(self):
        self.widgetMoveSignal.emit(2)

    @pyqtSlot()
    def measureButtonClickSlot(self):
        self.measureTimer.start(1000)
        pass

    @pyqtSlot()
    def measureTimerSlot(self):
        if(self.measureCnt >= 1):
            self.measureTimer.stop()
            if((sum(self.measureValues) / len(self.measureValues)) > 200):
                self.resultLabel.setText("Dranked!!")
            else:
                self.resultLabel.setText("Pass")
                self.loginButton.setEnabled(True)
                self.registerButton.setEnabled(True)
            self.measureCnt = 0
            self.measureValues = []

        else:
            self.measureValues.append(self.sensorManager.getSensorValue())
            self.valueLabel.setText(str(sum(self.measureValues) / len(self.measureValues)))
            self.resultLabel.setText("Measuring... {}s remained".format(10-self.measureCnt))
            self.measureCnt += 1

    def hideEvent(self, event):
        self.measureCnt = 0
        self.measureValues = []
        self.measureTimer.stop()
        self.valueLabel.setText("Wait")
        self.resultLabel.setText("Wait")
        self.loginButton.setEnabled(False)
        self.registerButton.setEnabled(False)

        return super().hideEvent(event)


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    w = HomeWidget()
    w.show()
    # w.ui.showFullScreen()
    sys.exit(app.exec())
