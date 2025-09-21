from enum import Enum
import subprocess
LOG_LEVEL = 0

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    NOTIFICATION = 5

def log(message, level=LogLevel.DEBUG):
    global LOG_LEVEL
    loglevel = LOG_LEVEL if isinstance(LOG_LEVEL, LogLevel) else LogLevel(LOG_LEVEL)
    if level.value >= loglevel.value:
        if level == LogLevel.DEBUG:
            print("[DEBUG]  " + message)
        elif level == LogLevel.INFO:
            print("[INFO]   " + message)
        elif level == LogLevel.WARNING:
            print("[WARNING] " + message)
        elif level == LogLevel.ERROR:
            print("[ERROR]  " + message)
        elif level == LogLevel.NOTIFICATION:
            subprocess.run(['osascript', '-e', f'display notification "{message}" with title "Befund-Tool"'])
            
def set_log_level(level):
    global LOG_LEVEL
    LOG_LEVEL = level