from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class StatusBar(QStatusBar):
    def __init__(self, parent = None):
        super().__init__()
        self.setStyleSheet("font-size: 12px")
    
    def _show_time_stamp(self, timeStamp, text = '{}'):
        try:
            timeStampText = timeStamp.strftime("%Y/%m/%d %H:%M:%S")
        except Exception:
            timeStampText = timeStamp
        self.showMessage(text.format(timeStampText))
        
    
        
        