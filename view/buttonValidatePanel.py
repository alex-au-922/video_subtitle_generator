from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from view.guiUtils.guiComponents import QVSeparationLine

class ButtonValidateWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self._set_up_widget_utils()
        self._set_up_layout()
    
    def _set_up_widget_utils(self):
        pass
    
    def _set_up_layout(self):
        mainLayout = QHBoxLayout()
        btnLayout = self._set_up_btn_layout()
        mainLayout.addLayout(btnLayout)
        self.setLayout(mainLayout)
        
    def _set_up_btn_layout(self):
        btnLayout = QHBoxLayout()
        self.validateBtn = QPushButton("Validate", parent = self)
        self.runBtn = QPushButton("Run", parent = self)
        vSeparationLine = QVSeparationLine(parent = self)
        btnLayout.addWidget(self.validateBtn)
        btnLayout.addWidget(vSeparationLine)
        btnLayout.addWidget(self.runBtn)
        return btnLayout