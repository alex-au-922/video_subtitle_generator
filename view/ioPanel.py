from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from view.guiUtils.guiComponents import LineEditSearchWidget, LineEditSaveWidget

class IoWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self._set_up_widget_utils()
        self._set_up_ui()
    
    def _set_up_widget_utils(self):
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy. Minimum)
    
    def _set_up_ui(self):
        mainLayout = self._set_up_layout()
        self.setLayout(mainLayout)
    
    def _set_up_layout(self):
        mainLayout = QVBoxLayout()
        sectionLayout = self._set_up_section_layout()
        mainLayout.addLayout(sectionLayout)
        return mainLayout
    
    def _set_up_section_layout(self):
        formLayout = QFormLayout()
        self.inputVideoWidget = LineEditSearchWidget(fileFilters = "Videos (*.mp4)", parent = self)
        self.inputSRTWidget = LineEditSearchWidget(fileFilters = "Text (*.srt)", parent = self)
        self.outputVideoWidget = LineEditSaveWidget(fileFilters = "Videos (*.mp4)", parent = self)
        formLayout.addRow(QLabel("<h4>Video Source: </h4>"), self.inputVideoWidget)
        formLayout.addRow(QLabel("<h4>Subtitle Source: </h4>"), self.inputSRTWidget)
        formLayout.addRow(QLabel("<h4>Output Path: </h4>"), self.outputVideoWidget)
        return formLayout