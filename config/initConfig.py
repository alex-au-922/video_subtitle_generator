from configparser import ConfigParser
import datetime

def store_config_values(mainWindow):
    config = ConfigParser()
    config.add_section('TimeStamp')
    config.add_section('InputOutput')
    config.add_section("Subtitle")
    
    timeStamp = datetime.datetime.now()
    timeStampText = timeStamp.strftime("%Y/%m/%d %H:%M:%S")
    
    config['TimeStamp']['SavedTime'] = timeStampText
    
    ioConfig = config['InputOutput']
    ioWidget = mainWindow.ioWidget
    
    IOConfig(ioConfig, ioWidget).store_values()
        
    subtitleConfig = config['Subtitle']
    subtitleWidget = mainWindow.subtitleWidget
    
    SubtitleConfig(subtitleConfig, subtitleWidget).store_values()
    with open('config/config.ini', 'w') as configfile:
        config.write(configfile)
        
    return datetime.datetime.now()

def init_config_values(mainWindow):
    config = ConfigParser()
    try:
        with open("config/config.ini", "r") as file:
            pass
    except FileNotFoundError:
        return None
    else:
        config.read("config/config.ini")
        timeStamp = datetime.datetime.strptime(
            config['TimeStamp']['SavedTime'],
            "%Y/%m/%d %H:%M:%S"
        )
        
        ioConfig = config['InputOutput']
        ioWidget = mainWindow.ioWidget
        
        IOConfig(ioConfig, ioWidget).set_init_values()
        
        subtitleConfig = config['Subtitle']
        subtitleWidget = mainWindow.subtitleWidget
        
        SubtitleConfig(subtitleConfig, subtitleWidget).set_init_values()
        return timeStamp

def read_io_widget_values(mainWindow):
    ioWidget = mainWindow.ioWidget
    ioWidgetValues = IOConfig(ioWidget = ioWidget)
    ioWidgetValues.get_io_widgets()
    ioWidgetValues.get_io_widget_values()
    return ioWidgetValues
    
def read_subtitle_widget_values(mainWindow):
    subtitleWidget = mainWindow.subtitleWidget
    subtitleWidgetValues = SubtitleConfig(subtitleWidget = subtitleWidget)
    subtitleWidgetValues.get_subtitle_widgets()
    subtitleWidgetValues.get_subtitle_widget_values()
    return subtitleWidgetValues

class IOConfig:
    def __init__(self, ioConfig = None, ioWidget = None):
        self._ioConfig = ioConfig
        self._ioWidget = ioWidget
    
    def set_init_values(self):
        self.get_io_widgets()
        self.get_io_config_values()
        self.set_io_widget_values()
    
    def store_values(self):
        self.get_io_widgets()
        self.get_io_widget_values()
        self.set_io_config_values()
    
    def get_io_widgets(self):
        self._inputVideoWidget = self._ioWidget.inputVideoWidget
        self._inputSRTWidget = self._ioWidget.inputSRTWidget
        self._outputVideoWidget = self._ioWidget.outputVideoWidget
        
    def get_io_config_values(self):
        self.inputVideoSource = self._ioConfig.get('inputVideo')
        self.inputSRTSource = self._ioConfig.get('inputSRT')
        self.outputVideoSource = self._ioConfig.get('outputVideo')
    
    def set_io_widget_values(self):
        self._inputVideoWidget.setValue(self.inputVideoSource)
        self._inputSRTWidget.setValue(self.inputSRTSource)
        self._outputVideoWidget.setValue(self.outputVideoSource)
    
    def get_io_widget_values(self):
        self.inputVideoSource = self._inputVideoWidget.getValue()
        self.inputSRTSource = self._inputSRTWidget.getValue()
        self.outputVideoSource = self._outputVideoWidget.getValue()
    
    def set_io_config_values(self):
        self._ioConfig['inputVideo'] = str(self.inputVideoSource)
        self._ioConfig['inputSRT'] = str(self.inputSRTSource)
        self._ioConfig['outputVideo'] = str(self.outputVideoSource)

class SubtitleConfig:
    def __init__(self, subtitleConfig = None, subtitleWidget = None):
        self._subtitleConfig = subtitleConfig
        self._subtitleWidget = subtitleWidget
    
    def set_init_values(self):
        self.get_subtitle_widgets()
        self.get_subtitle_config_values()
        self.get_subtitle_config_read_only_values()
        self.set_subtitle_widget_values()
        self.set_subtitle_widget_read_only_values()
    
    def store_values(self):
        self.get_subtitle_widgets()
        self.get_subtitle_widget_values()
        self.get_subtitle_widget_read_only_values()
        self.set_subtitle_config_values()
        self.set_subtitle_config_read_only_values()
    
    def get_subtitle_widgets(self):
        self._fontSizeEditLock = self._subtitleWidget.fontSizeEditLock
        self._fontWidthEditLock = self._subtitleWidget.fontWidthEditLock
        self._fontHeightEditLock = self._subtitleWidget.fontHeightEditLock
        self._fontPositionComboBoxLock = self._subtitleWidget.fontPositionComboBoxLock
        self._fontColorPickerLock = self._subtitleWidget.fontColorPickerLock
        self._fontBorderWidthSpinLock = self._subtitleWidget.fontBorderWidthSpinLock
        self._fontStyleEditLock = self._subtitleWidget.fontStyleEditLock
        self._addBannerCheckLock = self._subtitleWidget.addBannerCheckLock
        self._bannerColorPickerLock = self._subtitleWidget.bannerColorPickerLock
        self._bannerWidthEditLock = self._subtitleWidget.bannerWidthEditLock
        self._bannerHeightEditLock = self._subtitleWidget.bannerHeightEditLock
        self._bannerPositionWidthEditLock = self._subtitleWidget.bannerPositionWidthEditLock
        self._bannerPositionHeightEditLock = self._subtitleWidget.bannerPositionHeightEditLock
        self._bannerPositionComboBoxLock = self._subtitleWidget.bannerPositionComboBoxLock

    def get_subtitle_config_values(self):
        self.fontSizeValue = self._subtitleConfig.getint('fontSize')
        self.fontWidthValue = self._subtitleConfig.getint('fontPositionWidth')
        self.fontHeightValue = self._subtitleConfig.getint('fontPositionHeight')
        self.fontPositionTypeValue = self._subtitleConfig.getint('fontPositionType')
        self.fontColorValue = self._subtitleConfig.get('fontColor')
        self.fontBorderWidthValue = self._subtitleConfig.getint('fontBorderWidth')
        self.fontStyleValue = self._subtitleConfig.get('fontStyle')
        self.addBannerValue = self._subtitleConfig.getboolean('addBanner')
        self.bannerColorValue = self._subtitleConfig.get('bannerColor')
        self.bannerWidthValue = self._subtitleConfig.getint('bannerWidth')
        self.bannerHeightValue = self._subtitleConfig.getint('bannerHeight')
        self.bannerPositionWidthValue = self._subtitleConfig.getint('bannerPositionWidth')
        self.bannerPositionHeightValue = self._subtitleConfig.getint('bannerPositionHeight')
        self.bannerPositionTypeValue = self._subtitleConfig.getint('bannerPositionType')

    def get_subtitle_config_read_only_values(self):
        self.fontSizeValueReadOnly = self._subtitleConfig.getboolean('fontSize_locked')
        self.fontWidthValueReadOnly = self._subtitleConfig.getboolean('fontPositionWidth_locked')
        self.fontHeightValueReadOnly = self._subtitleConfig.getboolean('fontPositionHeight_locked')
        self.fontPositionTypeReadOnly = self._subtitleConfig.getboolean('fontPositionType_locked')
        self.fontColorValueReadOnly = self._subtitleConfig.getboolean('fontColor_locked')
        self.fontBorderWidthValueReadOnly = self._subtitleConfig.getboolean('fontBorderWidth_locked')
        self.fontStyleValueReadOnly = self._subtitleConfig.getboolean('fontStyleEditLock_locked')
        self.addBannerValueReadOnly = self._subtitleConfig.getboolean('addBanner_locked')
        self.bannerColorValueReadOnly = self._subtitleConfig.getboolean('bannerColor_locked')
        self.bannerWidthValueReadOnly = self._subtitleConfig.getboolean('bannerWidth_locked')
        self.bannerHeightValueReadOnly = self._subtitleConfig.getboolean('bannerHeight_locked')
        self.bannerPositionWidthValueReadOnly = self._subtitleConfig.getboolean('bannerPositionWidth_locked')
        self.bannerPositionHeightValueReadOnly = self._subtitleConfig.getboolean('bannerPositionHeight_locked')
        self.bannerPositionTypeValueReadOnly = self._subtitleConfig.getboolean('bannerPositionType_locked')

    def set_subtitle_widget_values(self):
        self._fontSizeEditLock.setValue(self.fontSizeValue)
        self._fontWidthEditLock.setValue(self.fontWidthValue)
        self._fontHeightEditLock.setValue(self.fontHeightValue)
        self._fontPositionComboBoxLock.setValue(self.fontPositionTypeValue)
        self._fontColorPickerLock.setValue(self.fontColorValue)
        self._fontBorderWidthSpinLock.setValue(self.fontBorderWidthValue)
        self._fontStyleEditLock.setValue(self.fontStyleValue)
        self._addBannerCheckLock.setValue(self.addBannerValue)
        self._bannerColorPickerLock.setValue(self.bannerColorValue)
        self._bannerWidthEditLock.setValue(self.bannerWidthValue)
        self._bannerHeightEditLock.setValue(self.bannerHeightValue)
        self._bannerPositionWidthEditLock.setValue(self.bannerPositionWidthValue)
        self._bannerPositionHeightEditLock.setValue(self.bannerPositionHeightValue)
        self._bannerPositionComboBoxLock.setValue(self.bannerPositionTypeValue)

    def set_subtitle_widget_read_only_values(self):
        self._fontSizeEditLock.setReadOnly(self.fontSizeValueReadOnly)
        self._fontWidthEditLock.setReadOnly(self.fontWidthValueReadOnly)
        self._fontHeightEditLock.setReadOnly(self.fontHeightValueReadOnly)
        self._fontPositionComboBoxLock.setReadOnly(self.fontPositionTypeReadOnly)
        self._fontColorPickerLock.setReadOnly(self.fontColorValueReadOnly)
        self._fontBorderWidthSpinLock.setReadOnly(self.fontBorderWidthValueReadOnly)
        self._fontStyleEditLock.setReadOnly(self.fontStyleValueReadOnly)
        self._addBannerCheckLock.setReadOnly(self.addBannerValueReadOnly)
        self._bannerColorPickerLock.setReadOnly(self.bannerColorValueReadOnly)
        self._bannerWidthEditLock.setReadOnly(self.bannerWidthValueReadOnly)
        self._bannerHeightEditLock.setReadOnly(self.bannerHeightValueReadOnly)
        self._bannerPositionWidthEditLock.setReadOnly(self.bannerPositionWidthValueReadOnly)
        self._bannerPositionHeightEditLock.setReadOnly(self.bannerPositionHeightValueReadOnly)
        self._bannerPositionComboBoxLock.setReadOnly(self.bannerPositionTypeValueReadOnly)
    
    def get_subtitle_widget_values(self):
        self.fontSizeValue = self._fontSizeEditLock.getValue() 
        self.fontWidthValue = self._fontWidthEditLock.getValue() 
        self.fontHeightValue = self._fontHeightEditLock.getValue() 
        self.fontPositionTypeValue = self._fontPositionComboBoxLock.getValue() 
        self.fontColorValue = self._fontColorPickerLock.getValue() 
        self.fontBorderWidthValue = self._fontBorderWidthSpinLock.getValue() 
        self.fontStyleValue = self._fontStyleEditLock.getValue() 
        self.addBannerValue = self._addBannerCheckLock.getValue() 
        self.bannerColorValue = self._bannerColorPickerLock.getValue() 
        self.bannerWidthValue = self._bannerWidthEditLock.getValue() 
        self.bannerHeightValue = self._bannerHeightEditLock.getValue() 
        self.bannerPositionWidthValue = self._bannerPositionWidthEditLock.getValue()
        self.bannerPositionHeightValue = self._bannerPositionHeightEditLock.getValue()
        self.bannerPositionTypeValue = self._bannerPositionComboBoxLock.getValue() 

    def get_subtitle_widget_read_only_values(self):
        self.fontSizeValueReadOnly = self._fontSizeEditLock.isReadOnly()
        self.fontWidthValueReadOnly = self._fontWidthEditLock.isReadOnly()
        self.fontHeightValueReadOnly = self._fontHeightEditLock.isReadOnly()
        self.fontPositionTypeReadOnly = self._fontPositionComboBoxLock.isReadOnly()
        self.fontColorValueReadOnly = self._fontColorPickerLock.isReadOnly()
        self.fontBorderWidthValueReadOnly = self._fontBorderWidthSpinLock.isReadOnly()
        self.fontStyleValueReadOnly = self._fontStyleEditLock.isReadOnly()
        self.addBannerValueReadOnly = self._addBannerCheckLock.isReadOnly()
        self.bannerColorValueReadOnly = self._bannerColorPickerLock.isReadOnly()
        self.bannerWidthValueReadOnly = self._bannerWidthEditLock.isReadOnly()
        self.bannerHeightValueReadOnly = self._bannerHeightEditLock.isReadOnly()
        self.bannerPositionWidthValueReadOnly = self._bannerPositionWidthEditLock.isReadOnly()
        self.bannerPositionHeightValueReadOnly = self._bannerPositionHeightEditLock.isReadOnly()
        self.bannerPositionTypeValueReadOnly = self._bannerPositionComboBoxLock.isReadOnly()
        
    def set_subtitle_config_values(self):
        self._subtitleConfig['fontSize'] = str(self.fontSizeValue)  
        self._subtitleConfig['fontPositionWidth'] = str(self.fontWidthValue)  
        self._subtitleConfig['fontPositionHeight'] = str(self.fontHeightValue)  
        self._subtitleConfig['fontPositionType'] = str(self.fontPositionTypeValue)  
        self._subtitleConfig['fontColor'] = str(self.fontColorValue)  
        self._subtitleConfig['fontBorderWidth'] = str(self.fontBorderWidthValue)  
        self._subtitleConfig['fontStyle'] = str(self.fontStyleValue)  
        self._subtitleConfig['addBanner'] = str(self.addBannerValue)  
        self._subtitleConfig['bannerColor'] = str(self.bannerColorValue)  
        self._subtitleConfig['bannerWidth'] = str(self.bannerWidthValue)
        self._subtitleConfig['bannerHeight'] = str(self.bannerHeightValue)
        self._subtitleConfig['bannerPositionWidth'] = str(self.bannerPositionWidthValue)  
        self._subtitleConfig['bannerPositionHeight'] = str(self.bannerPositionHeightValue)  
        self._subtitleConfig['bannerPositionType'] = str(self.bannerPositionTypeValue)  
    
    def set_subtitle_config_read_only_values(self):
        self._subtitleConfig['fontSize_locked'] = str(self.fontSizeValueReadOnly) 
        self._subtitleConfig['fontPositionWidth_locked'] = str(self.fontWidthValueReadOnly) 
        self._subtitleConfig['fontPositionHeight_locked'] = str(self.fontHeightValueReadOnly) 
        self._subtitleConfig['fontPositionType_locked'] = str(self.fontPositionTypeReadOnly) 
        self._subtitleConfig['fontColor_locked'] = str(self.fontColorValueReadOnly) 
        self._subtitleConfig['fontBorderWidth_locked'] = str(self.fontBorderWidthValueReadOnly) 
        self._subtitleConfig['fontStyleEditLock_locked'] = str(self.fontStyleValueReadOnly) 
        self._subtitleConfig['addBanner_locked'] = str(self.addBannerValueReadOnly) 
        self._subtitleConfig['bannerColor_locked'] = str(self.bannerColorValueReadOnly) 
        self._subtitleConfig['bannerWidth_locked'] = str(self.bannerWidthValueReadOnly)
        self._subtitleConfig['bannerHeight_locked'] = str(self.bannerHeightValueReadOnly)
        self._subtitleConfig['bannerPositionWidth_locked'] = str(self.bannerPositionWidthValueReadOnly) 
        self._subtitleConfig['bannerPositionHeight_locked'] = str(self.bannerPositionHeightValueReadOnly) 
        self._subtitleConfig['bannerPositionType_locked'] = str(self.bannerPositionTypeValueReadOnly) 