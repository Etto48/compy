from enum import Enum

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

def log(msg: str, level: LogLevel = LogLevel.INFO):
    color = "\033[0m"
    match level:
        case LogLevel.DEBUG:
            color = "\033[94m"
        case LogLevel.INFO:
            color = "\033[92m"
        case LogLevel.WARNING:
            color = "\033[93m"
        case LogLevel.ERROR:
            color = "\033[91m"
    print(f"{color}{msg}\033[0m")

def log_debug(msg: str):
    log(msg, LogLevel.DEBUG)

def log_info(msg: str):
    log(msg, LogLevel.INFO)

def log_warning(msg: str):
    log(msg, LogLevel.WARNING)

def log_error(msg: str):
    log(msg, LogLevel.ERROR)
