import re
from PIL import ImageFont, ImageDraw, Image
import subprocess
import numpy as np
from function.utils import (
    normal_time_to_second,
    change_second_to_frame
)
import cv2
from config.initConfig import read_io_widget_values, read_subtitle_widget_values
from function.utils import(
    parse_srt_time,
    get_video_frames,
    get_video_dimension,
    add_banner,
    add_text,
    progress_statistics
)
import time
from dataclasses import dataclass
import pathlib
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from logger import LogFile

class ParseSRTToFrames():
    SRT_BLOCK_PATTERN = r'\s*(\d+)\s*\n+\s*(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*\n+\s*(.*)\s*\n+'
    
    def __init__(self, srt_file_path, num_frames, fps, signal):
        self.srt_file_path = srt_file_path
        self.num_frames = num_frames
        self.fps = fps
        self.signal = signal
        
    def run(self):
        self.parse_srt()
        self.change_srt_to_srt_frame()
        self.change_srt_frame_to_list()
        
        self.signal.finished_parsing.emit()
        
        return self.subtitle_list
    
    def parse_srt(self):
        self.srt_blocks_list = []
        
        with open(self.srt_file_path, 'r') as f:
            content = f.read()
            
        _srt_blocks_list = re.findall(self.SRT_BLOCK_PATTERN, content)
        for block in _srt_blocks_list:
            order, start_time, end_time, subtitles = block
            start_hour, start_minute, start_second, start_milli = parse_srt_time(start_time)
            end_hour, end_minute, end_second, end_milli = parse_srt_time(end_time)
            buffer_dict = {
                'order': order,
                'start_hour': start_hour,
                'start_minute': start_minute,
                'start_second': start_second,
                'start_milli': start_milli,
                'end_hour': end_hour,
                'end_minute': end_minute,
                'end_second': end_second,
                'end_milli': end_milli,
                'subtitles': subtitles
            }
            self.srt_blocks_list.append(buffer_dict)

    def change_srt_to_srt_frame(self):
        
        def srt_block_time_to_frame(srt_block, start_end_string):
            hour = srt_block[f'{start_end_string}_hour']
            minute = srt_block[f'{start_end_string}_minute']
            second = srt_block[f'{start_end_string}_second']
            milli = srt_block[f'{start_end_string}_milli']
            time_in_second = normal_time_to_second(hour, minute, second, milli)
            time_in_frame = change_second_to_frame(time_in_second, self.fps)
            return time_in_frame
        
        self.srt_block_list_in_frame = []
        for srt_block in self.srt_blocks_list:
            buffer_dict = {
                'start_frame': srt_block_time_to_frame(srt_block,'start'),
                'end_frame': srt_block_time_to_frame(srt_block, 'end'),
                'subtitles': srt_block['subtitles']
            }
            self.srt_block_list_in_frame.append(buffer_dict)

    def change_srt_frame_to_list(self):
        self.subtitle_list = []
        srt_block_list_index = 0
        for frame_index in range(self.num_frames):
            if srt_block_list_index < len(self.srt_block_list_in_frame):
                if frame_index >= self.srt_block_list_in_frame[srt_block_list_index]['start_frame']:
                    self.subtitle_list.append(self.srt_block_list_in_frame[srt_block_list_index].get('subtitles',''))
                else:
                    self.subtitle_list.append('')
                if frame_index >= self.srt_block_list_in_frame[srt_block_list_index]['end_frame']:
                    srt_block_list_index += 1
            else:
                self.subtitle_list.append('')
@dataclass
class Font:
    font_size: int
    font_position_width: int
    font_position_height: int 
    font_position_type: int
    font_color: str
    font_border_width: int
    font_style_source: str
    font_add_banner: bool
    font_banner_color: str
    font_banner_width: int
    font_banner_height: int
    font_banner_position_width: int
    font_banner_position_height: int
    font_banner_position_type: int
    
@dataclass
class Video:
    input_src: str
    output_src: str
    num_frames: int 
    fps: int 
    frame_width: int 
    frame_height: int 


class GenerateSubtitleSignals(QObject):
    finished_parsing = pyqtSignal()
    finished_extract_audio = pyqtSignal()
    subtitle_progress = pyqtSignal(int, str)
    finished_add_subtitle = pyqtSignal()
    finished_rejoin_video = pyqtSignal()
    finished = pyqtSignal()

    
class CreateVideoWithSubtitle:
    def __init__(self, video:Video, font:Font, subtitle_list, signal:GenerateSubtitleSignals):
        self.video = video
        self.font = font
        self.subtitle_list = subtitle_list
        self.signal = signal
        self.logger = LogFile()
    
    def run(self):
        output_path_pathlib = pathlib.Path(self.video.output_src)
        output_path_parent = output_path_pathlib.parent
        output_path_stem = output_path_pathlib.stem
        output_path_name = output_path_pathlib.name
        self.temp_audio_output_path = str(output_path_parent / f'.audio_{output_path_stem}.mp3')
        self.temp_video_output_path = str(output_path_parent / f".video_{output_path_name}")
        
        self.extract_audio_from_video()
        self.signal.finished_extract_audio.emit()
        
        self.create_video_with_subtitle()
        self.signal.finished_add_subtitle.emit()
        
        self.reconstruct_video_with_audio()
        self.signal.finished_rejoin_video.emit()
        
    def extract_audio_from_video(self):
        audio_output = subprocess.Popen(
            f"ffmpeg -y -i {self.video.input_src} {self.temp_audio_output_path}", 
            shell = True)
        audio_output.wait()
    
    def create_video_with_subtitle(self):
        out = cv2.VideoWriter(self.temp_video_output_path, 
                              cv2.VideoWriter_fourcc(*'mp4v'), 
                              self.video.fps, 
                              (self.video.frame_width, self.video.frame_height))
        
        video = cv2.VideoCapture(self.video.input_src)
        
        start = time.perf_counter()
        for frame_count in range(self.video.num_frames):
            ret, frame = video.read()
            if not ret:
                break
            new_frame = self.put_subtitle(
                frame, 
                self.subtitle_list[frame_count]
            )
            out.write(new_frame)
            frame_count += 1
            present = time.perf_counter()
            
            summarized_statistics = progress_statistics(start, present, frame_count, self.video.num_frames)
            
            self.signal.subtitle_progress.emit(frame_count,summarized_statistics)
            
        video.release()
        out.release()
    
    def put_subtitle(self, frame, subtitle):
        font_style = ImageFont.truetype(self.font.font_style_source, self.font.font_size)
        
        if subtitle:
            if self.font.font_add_banner:
                add_banner(
                    frame, 
                    self.font.font_banner_color,
                    self.font.font_banner_width,
                    self.font.font_banner_height,
                    self.font.font_banner_position_width,
                    self.font.font_banner_position_height,
                    self.font.font_banner_position_type
                )
            
            
            frame_pillow = Image.fromarray(frame)
            draw = ImageDraw.Draw(frame_pillow)
            
            add_text(
                draw, 
                subtitle, 
                font_style,
                self.font.font_position_width, 
                self.font.font_position_height,
                self.font.font_position_type, 
                self.font.font_color
            )
            
            frame = np.array(frame_pillow)
        return frame
        
    def reconstruct_video_with_audio(self):
        ffmpeg_output = subprocess.Popen(
            f'ffmpeg -i {self.temp_audio_output_path} -i {self.temp_video_output_path} -c copy -y {self.video.output_src}', 
            shell=True
        )
        ffmpeg_output.wait()
        pathlib.Path(self.temp_audio_output_path).unlink()
        pathlib.Path(self.temp_video_output_path).unlink()
        
class MainExecution(QThread):
    def __init__(self, window):
        super(MainExecution, self).__init__()
        self.window = window
        self.signal = GenerateSubtitleSignals()
        self.ioWidgetValues = read_io_widget_values(window)
        self.subtitleWidgetValues = read_subtitle_widget_values(window)
        self.get_all_params()
        self.get_video_metadata()
        self.initialize_data_classes()
        
    def run(self):
        subtitle_list = ParseSRTToFrames(
            self.inputSRTSource,
            self.inputVideoNumFrames,
            self.inputVideoFPS,
            self.signal
        ).run()
        
        CreateVideoWithSubtitle(
            self.video,
            self.font,
            subtitle_list,
            self.signal,
        ).run()
        
        self.signal.finished.emit()
        
    
    def get_all_params(self):
        self.inputVideoSource = self.ioWidgetValues.inputVideoSource
        self.inputSRTSource = self.ioWidgetValues.inputSRTSource
        self.outputVideoSource = self.ioWidgetValues.outputVideoSource
        self.fontSizeValue = self.subtitleWidgetValues.fontSizeValue
        self.fontWidthValue = self.subtitleWidgetValues.fontWidthValue
        self.fontHeightValue = self.subtitleWidgetValues.fontHeightValue
        self.fontPositionTypeValue = self.subtitleWidgetValues.fontPositionTypeValue
        self.fontColorValue = self.subtitleWidgetValues.fontColorValue
        self.fontBorderWidthValue = self.subtitleWidgetValues.fontBorderWidthValue
        self.fontStyleValue = self.subtitleWidgetValues.fontStyleValue
        self.addBannerValue = self.subtitleWidgetValues.addBannerValue
        self.bannerColorValue = self.subtitleWidgetValues.bannerColorValue
        self.bannerWidthValue = self.subtitleWidgetValues.bannerWidthValue
        self.bannerHeightValue = self.subtitleWidgetValues.bannerHeightValue
        self.bannerPositionWidthValue = self.subtitleWidgetValues.bannerPositionWidthValue
        self.bannerPositionHeightValue = self.subtitleWidgetValues.bannerPositionHeightValue
        self.bannerPositionTypeValue = self.subtitleWidgetValues.bannerPositionTypeValue
    
    def get_video_metadata(self):
        inputVideo = cv2.VideoCapture(self.inputVideoSource)
        self.inputVideoNumFrames, self.inputVideoFPS = get_video_frames(inputVideo)
        self.inputVideoFrameWidth, self.inputVideoFrameHeight = get_video_dimension(inputVideo)
    
    def initialize_data_classes(self):
        self.font = Font(
            self.fontSizeValue,
            self.fontWidthValue,
            self.fontHeightValue,
            self.fontPositionTypeValue,
            self.fontColorValue,
            self.fontBorderWidthValue,
            self.fontStyleValue,
            self.addBannerValue,
            self.bannerColorValue,
            self.bannerWidthValue, 
            self.bannerHeightValue, 
            self.bannerPositionWidthValue,
            self.bannerPositionHeightValue,
            self.bannerPositionTypeValue,
        )
        self.video = Video(
            self.inputVideoSource,
            self.outputVideoSource,
            self.inputVideoNumFrames,
            self.inputVideoFPS,
            self.inputVideoFrameWidth,
            self.inputVideoFrameHeight
        )