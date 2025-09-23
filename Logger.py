from enum import Enum
import subprocess
import os
import datetime
LOG_LEVEL = 0
log_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Befund-Tool")

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    NOTIFICATION = 5

def log(message, level=LogLevel.DEBUG):
    global LOG_LEVEL
    global log_path
    # get timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    loglevel = LOG_LEVEL if isinstance(LOG_LEVEL, LogLevel) else LogLevel(LOG_LEVEL)
    log_message = ""
    if level.value >= loglevel.value:
        if level == LogLevel.DEBUG:
            log_message = f"[DEBUG] {message}"
        elif level == LogLevel.INFO:
            log_message = f"[INFO]  {message}"
        elif level == LogLevel.WARNING:
            log_message = f"[WARNING] {message}"
        elif level == LogLevel.ERROR:
            log_message = f"[ERROR] {message}"
        elif level == LogLevel.NOTIFICATION:
            log_message = f"[NOTIFICATION] {message}"
            subprocess.run(['osascript', '-e', f'display notification "{message}" with title "Befund-Tool"'])
            
        print(log_message)
        write_log_to_file(f"{timestamp} {log_message}", os.path.join(log_path, "befund_tool.log"))
        
            
def set_log_level(level):
    global LOG_LEVEL
    LOG_LEVEL = level
    
def write_log_to_file(message, log_file="befund_tool.log"):
    try:
        with open(log_file, "a") as f:
            f.write(message + "\n")
    except Exception as e:
        print(f"[ERROR] Failed to write log to file: {e}")