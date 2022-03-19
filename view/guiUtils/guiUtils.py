from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class GuiUtils:
    @staticmethod
    def center_screen(qMainWindow):
        qtRectangle = qMainWindow.frameGeometry() 
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        qMainWindow.move(qtRectangle.topLeft())
