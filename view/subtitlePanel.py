from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from view.guiUtils.guiComponents import LineEditSearchLockWidget, SpinBoxLockWidget, ComboBoxLockWidget, CollapsibleBox, ColorPickerLockWidget, AnimatedToggleCheckBoxLockWidget

class SubtitleConfigWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self._set_up_widget_utils()
        self._set_up_ui()
    
    def _set_up_widget_utils(self):
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy. Maximum)
    
    def _set_up_ui(self):
        mainLayout = self._set_up_layout()
        self.setLayout(mainLayout)
    
    def _set_up_layout(self):
        mainLayout = QVBoxLayout()
        basicFontLayout = self._set_up_basic_font_layout()
        advancedFontLayout = self._set_up_advanced_font_layout()
        mainLayout.addLayout(basicFontLayout)
        mainLayout.addLayout(advancedFontLayout)
        return mainLayout
    
    def _set_up_basic_font_layout(self):
        basicFontLayout = QFormLayout()
        self.fontSizeEditLock= SpinBoxLockWidget(0, 2160,parent = self)
        fontPositionInputLayout = self._set_font_position_widget()
        basicFontLayout.addRow(QLabel("Font Height (pixel): "), self.fontSizeEditLock)
        basicFontLayout.addRow(QLabel("Font Position (pixel) "), fontPositionInputLayout)
        return basicFontLayout

    def _set_font_position_widget(self):
        fontPositionWidget = QWidget()
        fontPositionLayout = QHBoxLayout()
        fontPositionLayout.setContentsMargins(0,0,0,0)
        fontPositionWidthLayout = self._set_font_position_width_layout()
        fontPositionHeightLayout = self._set_font_position_height_layout()
        fontPositionTypeLayout = self._set_font_position_type_layout()
        fontPositionLayout.addLayout(fontPositionWidthLayout)
        fontPositionLayout.addLayout(fontPositionHeightLayout)
        fontPositionLayout.addLayout(fontPositionTypeLayout)
        fontPositionWidget.setLayout(fontPositionLayout)
        return fontPositionWidget

    def _set_font_position_width_layout(self):
        fontPositionWidthLayout = QFormLayout()
        self.fontWidthEditLock = SpinBoxLockWidget(0, 3840,parent = self)
        fontPositionWidthLayout.addRow(QLabel("X: "), self.fontWidthEditLock)
        return fontPositionWidthLayout
        
    
    def _set_font_position_height_layout(self):
        fontPositionHeightLayout = QFormLayout()
        self.fontHeightEditLock = SpinBoxLockWidget(0, 2160, parent = self)
        fontPositionHeightLayout.addRow(QLabel("Y: "), self.fontHeightEditLock)
        return fontPositionHeightLayout
    
    def _set_font_position_type_layout(self):
        fontPositionTypeLayout = QFormLayout()
        self.fontPositionComboBoxLock = ComboBoxLockWidget(parent = self)
        self.fontPositionComboBoxLock.addItems(['Center', 'Top-left'])
        fontPositionTypeLayout.addRow(QLabel("Type: "), self.fontPositionComboBoxLock)
        return fontPositionTypeLayout
    
    def _set_up_advanced_font_layout(self):
        advancedFontLayout = QVBoxLayout()
        advancedFontLayout.setContentsMargins(0,10,0,0)
        box = CollapsibleBox("Advanced Subtitle Options", parent = self)
        expandLayout = self._set_up_expandable_section_layout()
        box.setContentLayout(expandLayout)
        advancedFontLayout.addWidget(box)
        return advancedFontLayout

    def _set_up_expandable_section_layout(self):
        expandLayout = QFormLayout()
        expandLayout.setContentsMargins(0,20,0, 10)
        self.fontColorPickerLock = ColorPickerLockWidget(initColor = "#ffffff", parent = self)
        self.fontBorderWidthSpinLock = SpinBoxLockWidget(0, 2160, parent = self)
        self.fontStyleEditLock = LineEditSearchLockWidget(fileFilters = "Text (*.ttf)", parent = self)
        self.addBannerCheckLock = AnimatedToggleCheckBoxLockWidget(width= 40, height = 30, parent = self)
        self.bannerColorPickerLock = ColorPickerLockWidget(initColor = "#000000", parent = self)
        self.bannerSizeEditLock = self._set_banner_dimension_widget()
        self.bannerPositionEditLock = self._set_banner_position_widget()
        expandLayout.addRow(QLabel("Font Color:"), self.fontColorPickerLock)
        expandLayout.addRow(QLabel("Font Border Width (pixel):"), self.fontBorderWidthSpinLock)
        expandLayout.addRow(QLabel("Font Source:"), self.fontStyleEditLock)
        expandLayout.addRow(QLabel("Add Banner: "), self.addBannerCheckLock)
        expandLayout.addRow(QLabel("Banner Background: "), self.bannerColorPickerLock)
        expandLayout.addRow(QLabel("Banner Dimesnion (pixel)"), self.bannerSizeEditLock)
        expandLayout.addRow(QLabel("Banner Position (pixel)"), self.bannerPositionEditLock)
        return expandLayout
    
    def _set_banner_dimension_widget(self):
        bannerWidget = QWidget()
        bannerLayout = QHBoxLayout()
        bannerLayout.setContentsMargins(0,0,0,0)
        bannerLayout.setSpacing(0)
        bannerWidthLayout = self._set_banner_width_layout()
        bannerHeightLayout = self._set_banner_height_layout()
        bannerLayout.addLayout(bannerWidthLayout, stretch = 1)
        bannerLayout.addLayout(bannerHeightLayout, stretch = 1)
        bannerWidget.setLayout(bannerLayout)
        return bannerWidget

    def _set_banner_width_layout(self):
        bannerWidthLayout = QFormLayout()
        self.bannerWidthEditLock = SpinBoxLockWidget(0, 3840,parent = self)
        bannerWidthLayout.addRow(QLabel("Width: "), self.bannerWidthEditLock)
        return bannerWidthLayout
        
    
    def _set_banner_height_layout(self):
        bannerHeightLayout = QFormLayout()
        self.bannerHeightEditLock = SpinBoxLockWidget(0, 2160, parent = self)
        bannerHeightLayout.addRow(QLabel("Height: "), self.bannerHeightEditLock)
        return bannerHeightLayout

    def _set_banner_position_widget(self):
        bannerPositionWidget = QWidget()
        bannerPositionLayout = QHBoxLayout()
        bannerPositionLayout.setContentsMargins(0,0,0,0)
        bannerPositionLayout.setSpacing(0)
        bannerPositionWidthLayout = self._set_banner_position_width_layout()
        bannerPositionHeightLayout = self._set_banner_position_height_layout()
        bannerPositionTypeLayout = self._set_banner_position_type_layout()
        bannerPositionLayout.addLayout(bannerPositionWidthLayout, stretch = 1)
        bannerPositionLayout.addLayout(bannerPositionHeightLayout, stretch = 1)
        bannerPositionLayout.addLayout(bannerPositionTypeLayout)
        bannerPositionWidget.setLayout(bannerPositionLayout)
        return bannerPositionWidget

    def _set_banner_position_width_layout(self):
        bannerPositionWidthLayout = QFormLayout()
        self.bannerPositionWidthEditLock = SpinBoxLockWidget(0, 3840,parent = self)
        bannerPositionWidthLayout.addRow(QLabel("X: "), self.bannerPositionWidthEditLock)
        return bannerPositionWidthLayout
        
    
    def _set_banner_position_height_layout(self):
        bannerPositionHeightLayout = QFormLayout()
        self.bannerPositionHeightEditLock = SpinBoxLockWidget(0, 2160, parent = self)
        bannerPositionHeightLayout.addRow(QLabel("Y: "), self.bannerPositionHeightEditLock)
        return bannerPositionHeightLayout
    
    def _set_banner_position_type_layout(self):
        bannerPositionTypeLayout = QFormLayout()
        self.bannerPositionComboBoxLock = ComboBoxLockWidget(parent = self)
        self.bannerPositionComboBoxLock.addItems(['Center', 'Top-left'])
        bannerPositionTypeLayout.addRow(QLabel("Type: "), self.bannerPositionComboBoxLock)
        return bannerPositionTypeLayout
        