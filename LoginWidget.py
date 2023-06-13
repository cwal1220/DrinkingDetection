import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import cv2
from managers.FaceRecogManager import FaceRecogManager
import time

class LoginWidget(QWidget):
    # 위젯 인덱스를 이동할때 방출하는 Signal
    widgetMoveSignal = pyqtSignal(int)
    
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('LoginWidget.ui', self)
        self.loginWorker = LoginWorker(self)
        self.loginWorker.cvImageSignal.connect(self.cvImageSlot)
        self.loginWorker.userInfoSignal.connect(self.userInfoSlot)
        self.loginButton.clicked.connect(self.loginButtonClickSlot)
        self.homeButton.clicked.connect(self.homeButtonClickSlot)
        self.id = None
        self.pw = None

    @pyqtSlot(list)
    def cvImageSlot(self, imageList):
        img = imageList[0]
        h, w ,c = img.shape
        qImg = QImage(img.data, w, h, w*c, QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(qImg)
        self.cvLabel.setPixmap(pixmap)
        self.cvLabel.resize(pixmap.width(),pixmap.height())

    @pyqtSlot(str, str)
    def userInfoSlot(self, id, pw):
        self.idEdit.setText(id)
        self.id = id
        self.pw = pw

    @pyqtSlot()
    def loginButtonClickSlot(self):
        id = self.idEdit.text()
        pw = self.pwEdit.text()

        if id == '':
            self.messageLabel.setText('얼굴을 인식해 주세요')
            return
        if pw == '':
            self.messageLabel.setText('비밀번호를 입력해 주세요')
            return
        if id != self.id or pw != self.pw:
            self.messageLabel.setText('아이디와 비밀번호를 확인해 주세요')
        else:
            self.messageLabel.setText('로그인 성공')
            self.widgetMoveSignal.emit(3)

    @pyqtSlot()
    def homeButtonClickSlot(self):
        self.widgetMoveSignal.emit(0)

    def showEvent(self, event):
        self.loginWorker.startLoginWorker()
        return super().showEvent(event)

    def hideEvent(self, event):
        self.loginWorker.stopLoginWorker()
        self.idEdit.setText('')
        self.pwEdit.setText('')
        self.messageLabel.setText('')
        self.cvLabel.setPixmap(QPixmap("resources/bg.png"))
        self.cvLabel.setText('Camera Initializing.....')
        return super().hideEvent(event)


class LoginWorker(QThread):
    # 이미지가 발생하면 출력되는 Signal
    cvImageSignal = pyqtSignal(list)
    userInfoSignal = pyqtSignal(str, str)
    def __init__(self, parent):
        super().__init__(parent)
        self.videoCapture = None
        self.isThreadRunnable = True

    def initCamera(self):
        self.videoCapture = cv2.VideoCapture(0)

    def releaseCamera(self):
        if self.videoCapture:
            self.videoCapture.release()
            self.videoCapture = None

    def startLoginWorker(self):
        self.isThreadRunnable = True
        self.start()

    def stopLoginWorker(self):
        self.isThreadRunnable = False
        time.sleep(2)

    def run(self):
        self.initCamera()
        faceRecogManager = FaceRecogManager()
        faceRecogManager.updateKnownFaces()
        while self.isThreadRunnable:
            ret, cameraFrame = self.videoCapture.read()
            name, frame = faceRecogManager.getLoginFrame(cameraFrame)
            self.cvImageSignal.emit([frame])
            if name != 'Unknown':
                self.userInfoSignal.emit(name.split('_')[1], name.split('_')[-1])
                break
        self.releaseCamera()


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    w = LoginWidget()
    w.show()
    # w.showFullScreen()
    sys.exit(app.exec())
