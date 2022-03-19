from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from view.menuBar import MenuBar
from view.ioPanel import IoWidget
from view.subtitlePanel import SubtitleConfigWidget
from view.buttonValidatePanel import ButtonValidateWidget
from view.statusBar import StatusBar
from view.guiUtils.guiUtils import GuiUtils
from view.guiUtils.guiComponents import ConfirmationDialog, QHSeparationLine, ScrollArea, CloseWindowSaveProgressBar
from config.initConfig import store_config_values, init_config_values

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.menuBarWidget = MenuBar(self)
        self.ioWidget = IoWidget(self)
        self.subtitleWidget = SubtitleConfigWidget(self)
        self.btnValidateWidget = ButtonValidateWidget(self)
        self.statusBarWidget = StatusBar(self)
        self._set_up_init_window_utils()
        self._set_up_central_widget()
        self._set_up_final_window_utils()
        self._set_menu_bar()
        self._set_status_bar()
        self._initialize_config_values()
        self._start_saving_timer()
    
    def _set_up_init_window_utils(self):
        self.setWindowTitle('Testing')
        self.setFixedWidth(680)
        
    def _set_up_final_window_utils(self):
        currentHeight = self.layout().sizeHint().height()
        self.setFixedHeight(currentHeight + 60)
        GuiUtils.center_screen(self)
    
    def _set_up_central_widget(self):
        self.centerWidget = QWidget()
        mainLayout = self._set_up_layout()
        self.centerWidget.setLayout(mainLayout)
        self.setCentralWidget(self.centerWidget)
    
    def _set_up_layout(self):
        mainLayout = QVBoxLayout()
        self.scrollArea = ScrollArea(parent = self)
        self.scrollArea.addWidget(self.ioWidget)
        separator = QHSeparationLine(dimension = 10, parent = self)
        self.scrollArea.addWidget(separator)
        self.scrollArea.addWidget(self.subtitleWidget)
        self.scrollArea.finishSetUp()
        mainLayout.addWidget(self.scrollArea)
        mainLayout.addWidget(self.btnValidateWidget)
        return mainLayout
    
    def _set_menu_bar(self):
        self.setMenuBar(self.menuBarWidget)
    
    def _set_status_bar(self):
        self.setStatusBar(self.statusBarWidget)
    
    def _start_saving_timer(self):
        self.timer = QTimer(parent = self)
        self.timer.timeout.connect(self._save_config_values)
        self.timer.setInterval(300000)
        self.timer.start()
        
    def _initialize_config_values(self):
        timeStamp = init_config_values(self)
        self._update_save_status(timeStamp)
    
    def _save_config_values(self):
        saveTimer = QTimer(parent = self)
        timeStamp = store_config_values(self)
        self.statusBarWidget.showMessage("Saving...")
        saveTimer.timeout.connect(lambda: self._update_save_status(timeStamp))
        saveTimer.setSingleShot(True)
        saveTimer.start(1000)
    
    def _update_save_status(self, timeStamp):
        self.statusBarWidget._show_time_stamp(timeStamp, "Last Saved: {}")
    
    def contextMenuEvent(self, event) -> None:
        self.menuBarWidget.exec(event.globalPos())
    
    def closeEvent(self, event):
        if ConfirmationDialog(
            "Notice", 
            "Are you sure you want to leave?", 
            parent = self
        ).yes:
            self._save_config_values()
            CloseWindowSaveProgressBar(
                event, 
                labelText = "Saving locked values...", 
                sleepTime = 1.5,
                parent = self
            ).exec_()
        else:
            event.ignore()
        
        

        