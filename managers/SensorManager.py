import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import Adafruit_ADS1x15

class SensorManager(QThread):
    # Example Signal
    dataSignal = pyqtSignal(str, str)
    
    def __init__(self):
        self.adc = Adafruit_ADS1x15.ADS1015(address=0x48, busnum=1)

    def run(self):
        pass

    def getSensorValue(self):
        ret = []
        for i in range(4):
            ret.append(self.adc.read_adc(i, gain=1))
        return ret[0]


