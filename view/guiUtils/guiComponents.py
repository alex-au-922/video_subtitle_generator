from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from abc import abstractmethod
from view.guiUtils.guiUtils import GuiUtils
import re
import os
import time

class BaseSeparationLine(QFrame):
    def __init__(self, dimension = 20, parent = None):
        super().__init__(parent = parent)
        self.dimension = dimension
        self._set_up_ui()
        
    @property
    @abstractmethod
    def frameShape(self):
        return NotImplemented
    
    @property
    @abstractmethod
    def setFixedDimensionMethod(self):
        return NotImplemented
    
    @property
    def frameShadow(self):
        return QFrame.Sunken
    
    @property
    @abstractmethod
    def widthSizePolicy(self):
        return NotImplemented
    
    @property
    @abstractmethod
    def heightSizePolicy(self):
        return NotImplemented
    
    def _set_up_ui(self):
        self.setFixedDimensionMethod(self.dimension)
        self.setFrameShape(self.frameShape)
        self.setFrameShadow(self.frameShadow)
        self.setSizePolicy(self.widthSizePolicy, self.heightSizePolicy)

class QHSeparationLine(BaseSeparationLine):
    @property
    def frameShape(self):
        return QFrame.HLine 
    
    @property
    def setFixedDimensionMethod(self):
        return self.setFixedHeight 
    
    @property
    def widthSizePolicy(self):
        return QSizePolicy.Minimum
    
    @property
    def heightSizePolicy(self):
        return QSizePolicy.Maximum

class QVSeparationLine(BaseSeparationLine):
    @property
    def frameShape(self):
        return QFrame.VLine 
    
    @property
    def setFixedDimensionMethod(self):
        return self.setFixedWidth
    
    @property
    def widthSizePolicy(self):
        return QSizePolicy.Maximum
    
    @property
    def heightSizePolicy(self):
        return QSizePolicy.Minimum  

class BaseDialogBox(QMessageBox):
    def __init__(self, windowTitle, initialText, parent = None):
        super().__init__(parent = parent)
        self.myWindowTitle = windowTitle
        self.initialText = initialText
        self._set_up_ui()
        self._set_up_widget_utils()
        self.returnValue = self.exec_()
    
    def _set_up_widget_utils(self):
        GuiUtils.center_screen(self)
    
    @property
    @abstractmethod
    def icon(self):
        return NotImplemented
    
    @property
    @abstractmethod
    def button(self):
        return NotImplemented
    
    def _set_up_ui(self):
        self.setWindowTitle(self.myWindowTitle)
        self.setText(self.initialText)
        self.setIcon(self.icon)
        self.addButton(self.button)
    
class NormalDialog(BaseDialogBox):
    @property
    def icon(self):
        return QMessageBox.Information
    
    @property
    def button(self):
        return QMessageBox.Ok

class ErrorBox(BaseDialogBox):
    @property
    def icon(self):
        return QMessageBox.Critical
    
    @property
    def button(self):
        return QMessageBox.Ok

class ConfirmationDialog(BaseDialogBox):
    @property
    def button(self):
        return False
    
    @property
    def icon(self):
        return QMessageBox.Information
    
    @property
    def yes(self):
        return self.returnValue == QMessageBox.Yes
    
    def _set_up_ui(self):
        super()._set_up_ui()
        self.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

class WarningConfirmationBox(BaseDialogBox):
    @property
    def icon(self):
        return QMessageBox.Critical
    
    @property
    def button(self):
        return False
    
    @property
    def yes(self):
        return self.returnValue == QMessageBox.Yes
    
    def _set_up_ui(self):
        super()._set_up_ui()
        self.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

class ClickableButton(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
    

class _NoTextButton(ClickableButton):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setText('')
        self.setStyleSheet("border: none;")

class IconOnlyToggleButton(_NoTextButton):
    def __init__(self, firstSource, secondSource, parent = None):
        super().__init__(parent = parent)
        self._iconSources = [firstSource, secondSource]
        self.readOnly = False
        self._cursorStyle = [
            QCursor(Qt.PointingHandCursor),
            QCursor(Qt.ArrowCursor)
        ]
        self.setToggleIcon()
    
    def setToggleIcon(self):
        self.setIcon(QIcon(QPixmap(self._iconSources[self.readOnly])))
    
    def isReadOnly(self):
        return self.readOnly
    
    def setReadOnly(self, readOnly):
        self.readOnly = readOnly
        self.setCursor(self._cursorStyle[self.readOnly])
        self.setToggleIcon()
    
    def mousePressEvent(self, event):
        if not self.readOnly:
            self.clicked.emit()

class SearchFileButton(IconOnlyToggleButton):
    def __init__(self, *args,  setText = None, filter = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText = setText
        self.filter = filter
        self.setClickAction()
    
    def setOpenFile(self):
        fileDirectory = QFileDialog.getOpenFileName(filter = self.filter, directory = os.getcwd())[0]
        if self.setText is not None:
            self.setText(fileDirectory)
    
    def setClickAction(self):
        self.clicked.connect(self.setOpenFile)   

class SaveFileButton(IconOnlyToggleButton):
    def __init__(self, *args,  setText = None, filter = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText = setText
        self.filter = filter
        self.setClickAction()
    
    def setSaveFile(self):
        fileDirectory = QFileDialog.getSaveFileName(filter= self.filter, directory = os.getcwd())[0]
        if self.setText is not None:
            self.setText(fileDirectory)
    
    def setClickAction(self):
        self.clicked.connect(self.setSaveFile)  

class LockButton(IconOnlyToggleButton):
    def __init__(self, *args, isReadOnly = None, setReadOnly = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.isReadOnly = isReadOnly
        self.setReadOnly = setReadOnly
        self.setClickAction()
    
    def setInputReadOnly(self, readOnly):
        self.readOnly = readOnly
        self._toggleState()
    
    def _toggleState(self):
        self.setReadOnly(self.readOnly)
        self.setToggleIcon()
    
    def toggleInputReadOnly(self):
        self.readOnly = self.isReadOnly()
        self.readOnly = not self.readOnly
        self._toggleState()

    def setClickAction(self):
        self.clicked.connect(self.toggleInputReadOnly)
    
    def mousePressEvent(self, event):
        self.clicked.emit()

class ClickableFrame(QFrame):
    clicked = pyqtSignal()
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.readOnly = False
        self._cursorTypes = [QCursor(Qt.PointingHandCursor),
                             QCursor(Qt.ArrowCursor)]
        self.setCursor(self._cursorTypes[self.readOnly])
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(2)
        
    def isReadOnly(self):
        return self.readOnly
    
    def setReadOnly(self, readOnly):
        self.readOnly = readOnly
        self.setCursor(self._cursorTypes[self.readOnly])
    
    def event(self, event):
        if event.type() == QEvent.MouseButtonRelease:
            if not self.readOnly:
                self.clicked.emit()
            return True
        return False
    
class ToggledReadOnlyWidget:        
    @property
    @abstractmethod
    def baseWidgetClass(self):
        return NotImplemented
    
    @property
    @abstractmethod
    def readOnlyMethod(self):
        return NotImplemented
    
    def mousePressEvent(self, event):
        if self.readOnlyMethod():
            self.clearFocus()
        else:
            self.baseWidgetClass.mousePressEvent(self, event)

    def keyPressEvent(self, event):
        if not self.readOnlyMethod():
            self.baseWidgetClass.keyPressEvent(self, event)

    def wheelEvent(self, event):
        if not self.readOnlyMethod():
            self.baseWidgetClass.wheelEvent(self, event)
    
    def mouseDoubleClickEvent(self, event):
        if self.readOnlyMethod():
            self.clearFocus()
        else:
            self.baseWidgetClass.mouseDoubleClickEvent(self, event)

class ToggledReadOnlyLineEdit(ToggledReadOnlyWidget, QLineEdit):  
    def __init__(self, initText = '', parent = None):
        QLineEdit.__init__(self, initText, parent = parent)
        ToggledReadOnlyWidget.__init__(self)
        self.setText(initText)
        self.setStyleSheet("%s:read-only{color: grey;}"%(self.baseWidgetClass.__name__))

    @property
    def baseWidgetClass(self):
        return QLineEdit
    
    @property
    def readOnlyMethod(self):
        return self.isReadOnly

class ToggledReadOnlySpinBox(ToggledReadOnlyWidget, QSpinBox):  
    def __init__(self, parent = None):
        QSpinBox.__init__(self, parent = parent)
        ToggledReadOnlyWidget.__init__(self)
        self.setStyleSheet("QSpinBox::read-only{color: grey;}")

    @property
    def baseWidgetClass(self):
        return QSpinBox
    
    @property
    def readOnlyMethod(self):
        return self.isReadOnly
    
    def setReadOnly(self, readOnly):
        super(QSpinBox, self).setReadOnly(readOnly)
        self.lineEdit().setReadOnly(readOnly)
        if readOnly:
            self.lineEdit().setFocusPolicy(Qt.NoFocus)
        else:
            self.lineEdit().setFocusPolicy(Qt.StrongFocus)
    
    def wheelEvent(self, event):
        self.clearFocus()
    
class ToggledReadOnlyComboBox(ToggledReadOnlyWidget, QComboBox):
    def __init__(self, parent = None):
        QComboBox.__init__(self, parent = parent)
        ToggledReadOnlyWidget.__init__(self)
        self.readOnlyState = 0
       
    @property
    def baseWidgetClass(self):
        return QComboBox

    def isReadOnly(self):
        return self.readOnlyState
    
    def setReadOnly(self, readOnly):
        self.readOnlyState = readOnly
        if self.readOnlyState:
             self.setStyleSheet("%s {color: grey;}"%(self.baseWidgetClass.__name__))
        else:
             self.setStyleSheet("%s {color: black;}"%(self.baseWidgetClass.__name__))
        
    @property
    def readOnlyMethod(self):
        return self.isReadOnly

    def wheelEvent(self, event):
        pass

class ToggledReadOnlyCheckBox(ToggledReadOnlyWidget, QCheckBox):
    def __init__(self,initText= '', parent = None):
        QComboBox.__init__(self, initText, parent = parent)
        ToggledReadOnlyWidget.__init__(self)
        self.readOnlyState = 0
        self.setText(initText)
       
    @property
    def baseWidgetClass(self):
        return QCheckBox

    def isReadOnly(self):
        return self.readOnlyState
    
    def setReadOnly(self, readOnly):
        self.readOnlyState = readOnly
        if self.readOnlyState:
             self.setStyleSheet("%s {color: grey;}"%(self.baseWidgetClass.__name__))
        else:
             self.setStyleSheet("%s {color: black;}"%(self.baseWidgetClass.__name__))
        
    @property
    def readOnlyMethod(self):
        return self.isReadOnly

    def wheelEvent(self, event):
        pass

class AnimatedToggleCheckBox(QCheckBox):

    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self,
        parent=None,
        barUncheckedColor=Qt.gray,
        barCheckedColor = "#008000",
        handleUnCheckedColor=Qt.white,
        handleCheckedColor = Qt.white,
        width = 58,
        height = 40
        ):
        super().__init__(parent)

        self.barUncheckedBrush = QBrush(QColor(barUncheckedColor))
        self.barCheckedBrush = QBrush(QColor(barCheckedColor))

        self.handleUnCheckedBrush = QBrush(QColor(handleUnCheckedColor))
        self.handleCheckedBrush = QBrush(QColor(handleCheckedColor))

        self.setContentsMargins(0, 0, 0, 0)
        self.handlePosition = 0

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)  # time in ms

        self.animationsGroup = QSequentialAnimationGroup()
        self.animationsGroup.addAnimation(self.animation)
        
        self.widgetWidth = width
        self.widgetHeight = height

        self.stateChanged.connect(self.setup_animation)

    def sizeHint(self):
        return QSize(self.widgetWidth, self.widgetHeight)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @pyqtSlot(int)
    def setup_animation(self, value):
        self.animationsGroup.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animationsGroup.start()

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        handleRadius = round(0.3 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.6 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2
        
        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self.handlePosition

        if self.isChecked():
            p.setBrush(self.barCheckedBrush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self.handleCheckedBrush)

        else:
            p.setBrush(self.barUncheckedBrush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self.handleUnCheckedBrush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @pyqtProperty(float)
    def handle_position(self):
        return self.handlePosition

    @handle_position.setter
    def handle_position(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self.handlePosition = pos
        self.update()
    
class ToggledReadOnlyAnimatedToggleCheckBox(ToggledReadOnlyWidget, AnimatedToggleCheckBox):
    def __init__(self,*args, parent = None, **kwargs):
        AnimatedToggleCheckBox.__init__(self, *args, **kwargs, parent = parent)
        ToggledReadOnlyWidget.__init__(self)
        self.readOnlyState = 0
               
    @property
    def baseWidgetClass(self):
        return AnimatedToggleCheckBox

    def isReadOnly(self):
        return self.readOnlyState
    
    def setReadOnly(self, readOnly):
        self.readOnlyState = readOnly
        if self.readOnlyState:
             self.setStyleSheet("%s {color: grey;}"%(self.baseWidgetClass.__name__))
        else:
             self.setStyleSheet("%s {color: black;}"%(self.baseWidgetClass.__name__))
        
    @property
    def readOnlyMethod(self):
        return self.isReadOnly

class ColorPicker(QWidget):
    def __init__(self, initColor, parent = None):
        super().__init__(parent = parent)
        self.color = QColor(initColor)
        self._set_up_ui()
    
    def _set_up_ui(self):
        mainLayout = self._set_up_layout()
        self.setLayout(mainLayout)
        
    def isReadOnly(self):
        return self.colorLineEdit.isReadOnly() and self.penColorFrame.isReadOnly()
    
    def setReadOnly(self, readOnly):
        self.colorLineEdit.setReadOnly(readOnly)
        self.penColorFrame.setReadOnly(readOnly)
         
    def _set_up_layout(self):
        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        self.colorLineEdit = ToggledReadOnlyLineEdit(self.color.name(),parent = self)
        self.pen = QPen(self.color, 2, Qt.SolidLine)
        self.penColorFrame = ClickableFrame()
        self.penColorFrame.setFixedSize(20, 20)
        self.penColorFrame.setAutoFillBackground(True)
        self.penColorFrame.setPalette(QPalette(self.color))
        self.colorLineEdit.textChanged.connect(self.manual_set_color)
        self.penColorFrame.clicked.connect(self.handle_color_dialog_clicked)
        self.colorDialog = QColorDialog()
        mainLayout.addWidget(self.colorLineEdit)
        mainLayout.addWidget(self.penColorFrame)
        return mainLayout
    
    def handle_color_dialog_clicked(self):
        self.colorDialog.exec()
        color = self.colorDialog.selectedColor()
        self.set_color(color)
        
    def set_color(self, color):
        if color.isValid():
            self.penColorFrame.setPalette(QPalette(color))
            self.pen.setColor(color)
            self.colorLineEdit.setText(color.name())
    
    def manual_set_color(self):
        colorText = self.colorLineEdit.text()
        _colorPattern = r"^#[A-Fa-f0-9]{6}$"
        if re.search(_colorPattern, colorText):
            color = QColor(colorText)
            self.set_color(color)
    
class ToggledReadOnlyColorPicker(ToggledReadOnlyWidget, ColorPicker):
    def __init__(self, initColor, parent = None):
        ColorPicker.__init__(self, initColor ,parent = parent)
        ToggledReadOnlyWidget.__init__(self)
       
    @property
    def baseWidgetClass(self):
        return ColorPicker
 
    @property
    def readOnlyMethod(self):
        return self.isReadOnly

class BaseCustomWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self._set_up_ui()
        
    def _set_up_ui(self):
        mainLayout = self._set_up_layout()
        self.setLayout(mainLayout)
    
    @abstractmethod
    def _set_up_layout(self):
        return NotImplementedError

class LineEditSearchWidget(BaseCustomWidget):
    def __init__(self, fileFilters = None, parent = None):
        if fileFilters is None:
            self._fileFilters = "All Files (*.*)"
        else:
            self._fileFilters = fileFilters
        super().__init__(parent = parent)
    
    def getValue(self):
        return self.lineEdit.text()
    
    def setValue(self, text):
        self.lineEdit.setText(text)
    
    def _set_up_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.lineEdit = ToggledReadOnlyLineEdit(parent = self)
        self.button = SearchFileButton("view/icons/search_icon.png",
                                       "view/icons/search_icon_invalid.png",
                                    setText = self.lineEdit.setText,
                                    filter = self._fileFilters,
                                    parent = self)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        return layout 
    
    def isReadOnly(self):
        return self.lineEdit.isReadOnly() and self.button.isReadOnly()

    def setReadOnly(self, readOnly):
        self.lineEdit.setReadOnly(readOnly)
        self.button.setReadOnly(readOnly)
                

class LineEditSaveWidget(BaseCustomWidget):
    def __init__(self, fileFilters = None, parent = None):
        if fileFilters is None:
            self._fileFilters = "All Files (*.*)"
        else:
            self._fileFilters = fileFilters
        super().__init__(parent = parent)
    
    def getValue(self):
        return self.lineEdit.text()

    def setValue(self, text):
        self.lineEdit.setText(text)
    
    def _set_up_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.lineEdit = ToggledReadOnlyLineEdit(parent = self)
        self.button = SaveFileButton("view/icons/search_icon.png", 
                                     "view/icons/search_icon_invalid.png",
                                    setText = self.lineEdit.setText,
                                    filter = self._fileFilters,
                                    parent = self)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        return layout 

    def isReadOnly(self):
        return self.lineEdit.isReadOnly() and self.button.isReadOnly()

    def setReadOnly(self, readOnly):
        self.lineEdit.setReadOnly(readOnly)
        self.button.setReadOnly(readOnly)

class LineEditLockWidget(BaseCustomWidget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        
    def isReadOnly(self):
        return self.lock.isReadOnly()
    
    def setReadOnly(self, readOnly):
        self.lock.setInputReadOnly(readOnly)
    
    def setValue(self, text):
        self.lineEdit.setText(text)
    
    def getValue(self):
        return self.lineEdit.text()
        
    def _set_up_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.lineEdit = ToggledReadOnlyLineEdit(parent = self)
        self.lock = LockButton("view/icons/new_open_lock2.png", 
                                       "view/icons/lock2.png", 
                                       isReadOnly=self.lineEdit.isReadOnly,
                                       setReadOnly= self.lineEdit.setReadOnly)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.lock)
        return layout

class LineEditSearchLockWidget(LineEditSearchWidget):
    def __init__(self, *args,  parent = None, **kwargs):
        super().__init__(*args, parent = parent, **kwargs)
    
    def setReadOnly(self, readOnly):
        self.lock.setInputReadOnly(readOnly)
    
    def _set_up_layout(self):
        layout = super()._set_up_layout()
        self.lock = LockButton("view/icons/new_open_lock2.png", 
                                       "view/icons/lock2.png", 
                                       isReadOnly=super().isReadOnly,
                                       setReadOnly= super().setReadOnly)
        layout.addWidget(self.lock)
        return layout

class SpinBoxLockWidget(BaseCustomWidget):
    def __init__(self, lowLimit = None, upLimit = None, parent = None):
        self.lowLimit = lowLimit
        self.upLimit = upLimit
        super().__init__(parent = parent)
    
    def isReadOnly(self):
        return self.lock.isReadOnly()
    
    def setReadOnly(self, readOnly):
        self.lock.setInputReadOnly(readOnly)
    
    def getValue(self):
        return self.spinBox.value()
    
    def setValue(self, value):
        self.spinBox.setValue(value)
        
    def _set_up_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.spinBox = ToggledReadOnlySpinBox(parent = self)
        self.spinBox.setRange(self.lowLimit, self.upLimit)
        self.lock = LockButton("view/icons/new_open_lock2.png", 
                                       "view/icons/lock2.png",  
                                       isReadOnly=self.spinBox.isReadOnly,
                                       setReadOnly= self.spinBox.setReadOnly)
        layout.addWidget(self.spinBox, stretch = 1)
        layout.addWidget(self.lock)
        return layout

class ColorPickerLockWidget(BaseCustomWidget):
    def __init__(self, initColor = "#000000", parent = None):
        self.initColor = initColor
        super().__init__(parent = parent)
    
    def isReadOnly(self):
        return self.lock.isReadOnly()

    def setReadOnly(self, readOnly):
        self.lock.setInputReadOnly(readOnly)
    
    def getValue(self):
        return self.colorPicker.colorLineEdit.text()
    
    def setValue(self, colorText):
        self.colorPicker.colorLineEdit.setText(colorText)
        
    def _set_up_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.colorPicker = ToggledReadOnlyColorPicker(initColor = self.initColor, parent = self)
        self.lock = LockButton("view/icons/new_open_lock2.png", 
                                       "view/icons/lock2.png",  
                                       isReadOnly=self.colorPicker.isReadOnly,
                                       setReadOnly= self.colorPicker.setReadOnly)
        layout.addWidget(self.colorPicker)
        layout.addWidget(self.lock)
        return layout

class ComboBoxLockWidget(BaseCustomWidget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
    
    def isReadOnly(self):
        return self.lock.isReadOnly()
    
    def setReadOnly(self, readOnly):
        self.lock.setInputReadOnly(readOnly)
    
    def getValue(self):
        return self.comboBox.currentIndex()

    def setValue(self, index):
        self.comboBox.setCurrentIndex(index)
    
    def addItems(self, items):
        self.comboBox.addItems(items)
    
    def _set_up_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.comboBox = ToggledReadOnlyComboBox(parent = self)
        self.lock = LockButton("view/icons/new_open_lock2.png", 
                                       "view/icons/lock2.png",  
                                       isReadOnly=self.comboBox.isReadOnly,
                                       setReadOnly= self.comboBox.setReadOnly)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.lock)
        return layout

class CheckBoxLockWidget(BaseCustomWidget):
    def __init__(self, initText = '', parent = None):
        self.initText = initText
        super().__init__(parent = parent)
    
    def isReadOnly(self):
        return self.lock.isReadOnly()
    
    def setReadOnly(self, readOnly):
        self.lock.setInputReadOnly(readOnly)

    def getValue(self):
        return self.checkBox.isChecked()
    
    def setValue(self, checked):
        self.checkBox.setChecked(checked)
        
    def _set_up_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.checkBox = ToggledReadOnlyCheckBox(self.initText, parent = self)
        self.lock = LockButton("view/icons/new_open_lock2.png", 
                                       "view/icons/lock2.png", 
                                       isReadOnly=self.checkBox.isReadOnly,
                                       setReadOnly= self.checkBox.setReadOnly)
        layout.addWidget(QLabel(''), stretch = 1)
        layout.addWidget(self.checkBox)
        layout.addWidget(self.lock)
        return layout      

class AnimatedToggleCheckBoxLockWidget(BaseCustomWidget):
    def __init__(self, *args, parent = None, **kwargs):
        self._args = args
        self._kwargs = kwargs
        super().__init__(parent = parent)
    
    def isReadOnly(self):
        return self.lock.isReadOnly()
    
    def setReadOnly(self, readOnly):
        self.lock.setInputReadOnly(readOnly)

    def getValue(self):
        return self.checkBox.isChecked()
    
    def setValue(self, checked):
        self.checkBox.setChecked(checked)
        
    def _set_up_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.checkBox = ToggledReadOnlyAnimatedToggleCheckBox(*self._args, **self._kwargs, parent = self)
        self.lock = LockButton("view/icons/new_open_lock2.png", 
                                       "view/icons/lock2.png",  
                                       isReadOnly=self.checkBox.isReadOnly,
                                       setReadOnly= self.checkBox.setReadOnly)
        layout.addWidget(QLabel(''), stretch = 1)
        layout.addWidget(self.checkBox)
        layout.addWidget(self.lock)
        return layout      

class CollapsibleBox(QWidget):
    def __init__(self, title="", toolTip = '', parent=None):
        super(CollapsibleBox, self).__init__(parent)
        
        self.toggle_button = QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("QToolButton { border: none; };")
        self.toggle_button.setToolTip(toolTip)
        self.toggle_button.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea(
            maximumHeight = 0, minimumHeight=0
        )
        self.content_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Maximum
        )
        self.content_area.setFrameShape(QFrame.NoFrame)
        self.content_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                
        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)
        
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    @pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        if checked:
            self.toggle_button.setArrowType(Qt.RightArrow)
            self.toggle_animation.setDirection(QAbstractAnimation.Backward)
        else:
            self.toggle_button.setArrowType(Qt.DownArrow)
            self.toggle_animation.setDirection(QAbstractAnimation.Forward)
        self.toggle_animation.start()
    
    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(750)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)
            animation.setEasingCurve(QEasingCurve.OutQuad)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(750)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

class ScrollArea(QScrollArea):
    def __init__(self, hScroll = False, parent = None):
        super().__init__(parent = parent)
        self.hScrollMode = hScroll
        self._set_up_widget_utils()
        self._set_up_ui()
        
    def _set_up_widget_utils(self):
        self.setFrameShape(QFrame.NoFrame)
        self.setAlignment(Qt.AlignHCenter)
        self.setWidgetResizable(True)
        if self.hScrollMode:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        else:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    
    def addWidget(self, *args, **kwargs):
        self.mainLayout.addWidget( *args, **kwargs)
    
    def addStretch(self, stretch):
        self.mainLayout.addStretch(stretch)
    
    def finishSetUp(self):
        self.addStretch(1)
        self.scrollWidget.setLayout(self.mainLayout)
        self.setWidget(self.scrollWidget)
    
    def _set_up_ui(self):
        self.scrollWidget = QWidget(parent = self)
        self.scrollWidget.setFixedWidth(self.parent().width() - 40)
        if self.hScrollMode:
            self.mainLayout = QHBoxLayout()
        else:
            self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0,0,0,0)   

class SleepProgressWorkerSignal(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

class SleepProgress(QThread):
    def __init__(self, sleepTime = 0):
        super(SleepProgress, self).__init__()
        self.sleepTime = sleepTime
        self.signal = SleepProgressWorkerSignal()
    
    def run(self):
        for i in range(100):
            time.sleep(self.sleepTime / 100)
            self.signal.progress.emit(i)
        self.signal.finished.emit()    

class SaveProgressBar(QProgressDialog):
    def __init__(self, labelText = "", sleepTime = 0, parent = None):
        super().__init__(parent = parent)
        self.setLabelText(labelText)
        self.setWindowTitle("Saving...")
        self.sleepTime = sleepTime
        self.sleepProgress = SleepProgress(self.sleepTime)
        self.sleepProgress.signal.finished.connect(self.close)
        self.setCancelButton(None)
        self.setRange(0,0)
    
    def show(self):
        self.sleepProgress.start()
        super().show()
    
    def exec_(self):
        self.sleepProgress.start()
        super().exec_()

class CloseWindowSaveProgressBar(SaveProgressBar):
    def __init__(self, event, *args, parent = None, labelText = '', sleepTime = 0, **kwargs):
        super().__init__(*args, labelText = labelText, sleepTime = sleepTime, parent = parent,**kwargs)
        self._event = event
    
    def exec_(self):
        self.sleepProgress.signal.finished.connect(self.close_window)
        super().exec_()
    
    def close_window(self):
        self._event.setAccepted(True)

class ProgressBar(QProgressDialog):
    def __init__(self, windowTitle = "Progress", cancellable = False, parent = None):
        super().__init__(parent = parent)
        self.setWindowTitle(windowTitle)
        self.setCancelButton(True if cancellable else None)
        self.inNoLengthMode = NotImplemented
    
    def set_no_length_mode(self, labelText = ''):
        self.inNoLengthMode = True
        self.setLabelText(labelText)
        self.setRange(0,0)
    
    def update_text(self, labelText= ''):
        if self.inNoLengthMode:
            self.setLabelText(labelText)
    
    def set_progress_mode(self, lowRange, upRange, labelText = ''):
        self.inNoLengthMode = False
        self.setLabelText(labelText)
        self.setRange(lowRange, upRange)
    
    def update_progress_with_text(self, progress, labelText= ''):
        if not self.inNoLengthMode:
            self.setValue(progress)     
            self.setLabelText(labelText)
    
    def update_progress(self, progress):
        if not self.inNoLengthMode:
            self.setValue(progress)     
