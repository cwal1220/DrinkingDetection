import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import cv2
import time
from managers.FaceRecogManager import FaceRecogManager
from managers.FaceRecogManager import signUpDuplicatecheck
from managers.FaceRecogManager import signUp

class RegisterWidget(QWidget):
    # 위젯 인덱스를 이동할때 방출하는 Signal
    widgetMoveSignal = pyqtSignal(int)

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('RegisterWidget.ui', self)
        self.registerWorker = RegisterWorker(self)
        self.registerWorker.cvImageSignal.connect(self.cvImageSlot)
        self.registerWorker.userInfoSignal.connect(self.userInfoSlot)
        self.registerButton.clicked.connect(self.registerButtonClickSlot)
        self.cameraButton.clicked.connect(self.cameraButtonClickSlot)
        self.refreshButton.clicked.connect(self.refreshButtonClickSlot)
        self.homeButton.clicked.connect(self.homeButtonClickSlot)
        
        self.img = None
        self.id = None
        self.pw1 = None
        self.pw2 = None
        self.isFrameUpdate = True

    @pyqtSlot(list)
    def cvImageSlot(self, imageList):
        if self.isFrameUpdate:
            self.img = imageList[0]
            h, w ,c = self.img.shape
            qImg = QImage(self.img.data, w, h, w*c, QImage.Format.Format_BGR888)
            pixmap = QPixmap.fromImage(qImg)
            self.cvLabel.setPixmap(pixmap)
            self.cvLabel.resize(pixmap.width(),pixmap.height())

    @pyqtSlot(str)
    def userInfoSlot(self, id):
        self.id = id
        if id == '':
            self.messageLabel.setText('얼굴 미감지')
        elif id == 'Unknown':
            self.messageLabel.setText('회원가입 가능')
        else:
            self.messageLabel.setText('이미 등록된 사용자 [ ' + id + ' ]님!')

    @pyqtSlot()
    def registerButtonClickSlot(self):
        id = self.idEdit.text()
        pw1 = self.pw1Edit.text()
        pw2 = self.pw2Edit.text()

        if id == '':
            self.messageLabel.setText('아이디를 입력해 주세요')
            return
        if pw1 == '' or pw2 == '':
            self.messageLabel.setText('비밀번호를 입력해 주세요')
            return
        if pw1 != pw2:
            self.messageLabel.setText('두 비밀번호가 일치하지 않습니다.')
            return
        if signUpDuplicatecheck(id):
            self.messageLabel.setText('이미 사용중인 아이디 입니다')
            return
        faceRecogManager = FaceRecogManager()
        name, _ = faceRecogManager.getRegisterFrame(self.img)

        if name == 'Unknown':
            if signUp(self.img, id, pw1):
                self.messageLabel.setText('회원가입 성공')
            else:
                self.messageLabel.setText('얼굴이 감지되지 않았습니다. 다시 시도하세요')
        else:
            self.messageLabel.setText('이미 가입된 회원의 얼굴입니다 [ ' + name.split('_')[1] + ' ]')
    
    @pyqtSlot()
    def cameraButtonClickSlot(self):
        self.isFrameUpdate = False

    @pyqtSlot()
    def refreshButtonClickSlot(self):
        self.isFrameUpdate = True

    @pyqtSlot()
    def homeButtonClickSlot(self):
        self.widgetMoveSignal.emit(0)

    def showEvent(self, event):
        self.registerWorker.startRegisterWorker()
        return super().showEvent(event)

    def hideEvent(self, event):
        self.registerWorker.stopRegisterWorker()
        self.idEdit.setText('')
        self.pw1Edit.setText('')
        self.pw2Edit.setText('')
        self.messageLabel.setText('')
        self.cvLabel.setPixmap(QPixmap("resources/bg.png"))
        self.cvLabel.setText('Camera Initializing.....')
        return super().hideEvent(event)


class RegisterWorker(QThread):
    # 이미지가 발생하면 출력되는 Signal
    cvImageSignal = pyqtSignal(list)
    userInfoSignal = pyqtSignal(str)
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

    def startRegisterWorker(self):
        self.isThreadRunnable = True
        self.start()

    def stopRegisterWorker(self):
        self.isThreadRunnable = False
        time.sleep(2)

    def run(self):
        self.initCamera()
        while self.isThreadRunnable:
            ret, cameraFrame = self.videoCapture.read()
            self.cvImageSignal.emit([cameraFrame])
        self.releaseCamera()


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    w = RegisterWidget()
    w.show()
    # w.showFullScreen()
    sys.exit(app.exec())
