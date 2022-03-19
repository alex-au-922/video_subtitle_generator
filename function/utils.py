import re
import cv2
from logger import LogFile
SRT_TIME_PATTERN = r'(\d{2}):(\d{2}):(\d{2}),(\d{3})'

def parse_srt_time(time_string):
    hour, minute, second, millisecond = re.findall(SRT_TIME_PATTERN, time_string)[0]
    return int(hour), int(minute), int(second), int(millisecond)

def get_video_frames(video):
    return round(video.get(cv2.CAP_PROP_FRAME_COUNT)), round(video.get(cv2.CAP_PROP_FPS), 0)

def get_video_dimension(video):
    return int(video.get(cv2. CAP_PROP_FRAME_WIDTH)), int(video.get(cv2. CAP_PROP_FRAME_HEIGHT))

def change_second_to_frame(second, fps):
    return round(second*fps)

def normal_time_to_second(hour, minute, second, millisecond):
    return (hour *60 + minute)*60 + second + millisecond / 1000

def color_string_to_rgb_tuple(color_string):
    rgb_string_pattern = r"^#([A-Fa-f0-9]{2})([A-Fa-f0-9]{2})([A-Fa-f0-9]{2})$"
    color_string_list = list(re.findall(rgb_string_pattern, color_string)[0])
    color_string_int_list = [int(color,16) for color in color_string_list]
    color_string_int_list.append(1)
    return tuple(color_string_int_list)

def add_banner(
        frame, 
        banner_color,
        banner_width, 
        banner_height, 
        banner_position_width,
        banner_position_height,
        banner_position_type,
    ):
    logger = LogFile()
    if banner_position_type == 0:
        start_point = (banner_position_width - banner_width // 2, banner_position_height - banner_height // 2)
        end_point = (banner_position_width + banner_width // 2, banner_position_height + banner_height // 2)
        logger.debug(f"Banner height start: {banner_position_height - banner_height // 2}")
        logger.debug(f"Banner height end: {banner_position_height + banner_height // 2}")
    else:
        start_point = (banner_position_width, banner_position_height)
        end_point = (banner_position_width + banner_width, banner_position_height + banner_height)
    banner_color_tuple = color_string_to_rgb_tuple(banner_color)
    cv2.rectangle(frame, start_point, end_point, banner_color_tuple, -1)

def add_text(
        draw,
        subtitle, 
        font_style, 
        font_position_width,
        font_position_height,
        font_position_type, 
        font_color
    ):
    logger = LogFile()
    font_width,font_height = draw.textsize(subtitle, font = font_style)
    logger.debug(f"{font_height = }")
    font_color_tuple = color_string_to_rgb_tuple(font_color)
    if font_position_type == 0:
        start_point = (font_position_width - font_width //2 , font_position_height - font_height//2)
        logger.debug(f"Font height start: {font_position_height - font_height//2}")
        logger.debug(f"Font height end: {font_position_height - font_height//2 + font_height}")
    else:
        start_point = (font_position_width, font_position_height)
        # logger.debug(f"{font_position_type = }, {start_point = }")
    draw.text(start_point,  subtitle, font = font_style, fill = font_color_tuple)

def progress_statistics(start_time, present_time, progress_count, total_len):
    iter_per_sec = round(progress_count / (present_time - start_time),1)
    eta = round((present_time - start_time) * (total_len / progress_count - 1),1)
    summarized_statistics = "{} / {}\nIteration: {}/s\nETA: {}s".format(
            progress_count, total_len,
            iter_per_sec,
            eta
    )
    return summarized_statistics