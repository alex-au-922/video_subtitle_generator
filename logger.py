
import pathlib
import enum
import os
import logging
from logging.handlers import RotatingFileHandler

class Mode(enum.Enum):
    DEBUG = 0
    PRODUCTION = 1

if os.environ.get("DEBUG", 0):
    EXEC_MODE = Mode.DEBUG
else:
    EXEC_MODE = Mode.PRODUCTION

class LoggingConstants:
    LOG_PARENT_PATH = pathlib.Path('logging')
    if EXEC_MODE == Mode.DEBUG:
        LOG_DEBUG_PATH = LOG_PARENT_PATH / 'debug_debug.log'
        LOG_WARNING_PATH = LOG_PARENT_PATH / 'debug_warning.log'
    else:
        LOG_DEBUG_PATH = LOG_PARENT_PATH / 'production_debug.log'
        LOG_WARNING_PATH = LOG_PARENT_PATH / 'production_warning.log'
    LOG_FILE_FORMAT= '%(asctime)s (%(name)s) [%(levelname)s] > %(message)s'
    LOG_CONSOLE_FORMAT = '%(asctime)s [%(levelname)s] > %(message)s'
    PAGESOURCE_FILE_PATH = LOG_PARENT_PATH/'pagesource.html'
    ERROR_PNG_PATH = LOG_PARENT_PATH/'error.png'

class TerminalColors:
    GREY = "\x1b[38;20m"
    GREEN = "\x1b[32:20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class CustomFormatter(logging.Formatter):
    def __init__(self, format, timeFormat):
        super().__init__(fmt = format, datefmt = timeFormat)
        self.timeFormat = timeFormat
        self.formats = {
            logging.DEBUG: TerminalColors.GREY + format + TerminalColors.RESET,
            logging.INFO: TerminalColors.GREEN + format + TerminalColors.RESET,
            logging.WARNING: TerminalColors.YELLOW + format + TerminalColors.RESET,
            logging.ERROR: TerminalColors.RED + format + TerminalColors.RESET,
            logging.CRITICAL: TerminalColors.BOLD_RED + format + TerminalColors.RESET
        }
        
    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt, self.timeFormat)
        return formatter.format(record)
    
class LogFile(metaclass=Singleton):          
    def __init__(self):
        self.logger = logging.getLogger('main')
        LoggingConstants.LOG_PARENT_PATH.mkdir(parents = True, exist_ok = True)
        
        expFileHandler = RotatingFileHandler(LoggingConstants.LOG_DEBUG_PATH, maxBytes=10**6, backupCount=10)
        expFileHandler.setLevel(logging.DEBUG)
        expFileHandler.setFormatter(CustomFormatter(LoggingConstants.LOG_FILE_FORMAT, "%Y-%m-%d %H:%M:%S"))
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(CustomFormatter(LoggingConstants.LOG_CONSOLE_FORMAT, "%Y-%m-%d %H:%M:%S"))

        expErrorsFileHandler = RotatingFileHandler(LoggingConstants.LOG_WARNING_PATH, maxBytes=10**6, backupCount=10)
        expErrorsFileHandler.setLevel(logging.WARNING)
        expErrorsFileHandler.setFormatter(CustomFormatter(LoggingConstants.LOG_FILE_FORMAT, "%Y-%m-%d %H:%M:%S"))
        
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(expFileHandler) 
        self.logger.addHandler(consoleHandler)
        self.logger.addHandler(expErrorsFileHandler)        
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
       
    def error(self, message):
        self.logger.error(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def critical(self, message):
        self.logger.critical(message)