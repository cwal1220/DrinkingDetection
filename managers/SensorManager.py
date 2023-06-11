import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *


class SensorManager(QThread):
    # Example Signal
    dataSignal = pyqtSignal(str, str)
    
    def __init__(self):
        pass

    def run(self):
        pass

    def getSensorValue(self):
        return 100

