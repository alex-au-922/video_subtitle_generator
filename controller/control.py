from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from view.ui import MainWindow
from function.generate_subtitle import MainExecution
from view.guiUtils.guiComponents import NormalDialog, WarningConfirmationBox, ProgressBar

class Controller:
    def __init__(self, window:MainWindow):
        self.window = window
        self.set_run_button_function()
        self.set_validate_button_function()
    
    def set_run_button_function(self):
        runBtn = self.window.btnValidateWidget.runBtn
        runBtn.clicked.connect(lambda: self.generate_subtitle_procedure())
    
    def generate_subtitle_procedure(self):
        mainExecution = MainExecution(self.window)
        if not mainExecution.font.font_add_banner:
            if not WarningConfirmationBox(
                "Warning!", 
                """
                As you have not selected creating a banner,
                the options for configuring the banner will
                be inactivated. 
                
                Are you sure to proceed?
                """
            ).yes:
                return
        progressBar = ProgressBar(parent = self.window)
        progressBar.set_no_length_mode('Parsing the .srt file...')
        mainExecution.signal.finished_parsing.connect(
            lambda: progressBar.update_text('Extracting audio from video...')
        )
        mainExecution.signal.finished_extract_audio.connect(
            lambda: progressBar.set_progress_mode(
                0, 
                mainExecution.video.num_frames,
                'Adding subtitles to video...'
            )
        )
        mainExecution.signal.subtitle_progress.connect(progressBar.update_progress_with_text)
        mainExecution.signal.finished_add_subtitle.connect(
            lambda: progressBar.set_no_length_mode(
                'Rejoining the audio and video together...'
            )
        )
        mainExecution.signal.finished_rejoin_video.connect(progressBar.close)
        mainExecution.signal.finished.connect(
            lambda: NormalDialog("Success", f"Finished outputing video to\n{mainExecution.video.output_src}", parent = self.window)
        )
        mainExecution.start()
        progressBar.show()
    
    def set_validate_button_function(self):
        pass