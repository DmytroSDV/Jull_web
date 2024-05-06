import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
import inspect


# logging.CRITICAL = 50
# logging.ERROR = 40
# logging.WARNING = 30
# logging.INFO = 20
# logging.DEBUG = 10
# logging.NOTSET = 0


class CustomLogger:

    def __init__(
        self,
        log_file: str,
        log_file_errors: str,
        console_level: int = logging.DEBUG,
        file_level: int = logging.INFO,
        file_level_errors: int = logging.ERROR,
        logger_name: str = "custom_logger",
        file_size: int = 1024 * 1024,
        backup_count: int = 11,
    ) -> None:

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(console_level)

        self.logger_info = logging.getLogger(logger_name + "_info")
        self.logger_info.setLevel(console_level)

        self.logger_errors = logging.getLogger(logger_name + "_errors")
        self.logger_errors.setLevel(console_level)

        self.format_info = {
            logging.DEBUG: "%(levelname)s, %(asctime)s, message - %(message)s",
            logging.INFO: "%(levelname)s, %(asctime)s, Message - %(message)s",
            # logging.INFO: "%(levelname)s, %(asctime)s, module - '%(module)s', line - '%(lineno)d', message - %(message)s",
            logging.WARNING: "%(levelname)s, %(asctime)s, line - '%(lineno)d', Message - '%(message)s'",
            logging.ERROR: "%(levelname)s, %(asctime)s, Message - '%(message)s'",
            # logging.ERROR:  "%(levelname)s, %(asctime)s, module - '%(module)s', function - '%(funcName)s', line - '%(lineno)d'. Message - '%(message)s'",
            logging.CRITICAL: "%(levelname)s, %(asctime)s,  function - '%(funcName)s', Message - '%(message)s'",
        }

        # Log for console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_formatter = logging.Formatter(self.format_info[logging.INFO])
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Log for file
        file_handler = RotatingFileHandler(
            log_file,
            mode="a",
            maxBytes=file_size,
            backupCount=backup_count,
            encoding="utf8",
        )
        file_handler.setLevel(file_level)
        file_formatter = logging.Formatter(
            self.format_info[logging.ERROR], "%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        self.logger_info.addHandler(file_handler)

        # Log for file errors
        file_handler_errors = RotatingFileHandler(
            log_file_errors,
            mode="a",
            maxBytes=file_size,
            backupCount=backup_count,
            encoding="utf8",
        )
        file_handler_errors.setLevel(file_level_errors)
        file_formatter_errors = logging.Formatter(
            self.format_info[logging.ERROR], "%Y-%m-%d %H:%M:%S"
        )
        file_handler_errors.setFormatter(file_formatter_errors)
        self.logger_errors.addHandler(file_handler_errors)

        # Hooking error in handlers
        file_handler.handleError = self.handle_formatting_error
        file_handler_errors.handleError = self.handle_formatting_error
        console_handler.handleError = self.handle_formatting_error
        self.logger.addHandler(file_handler)
        self.logger.addHandler(file_handler_errors)
        self.logger.addHandler(console_handler)

    def handle_formatting_error(self, record):

        logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
        logging.error(f"while executing log command, wrong used format! {record}")

    def log(self, message: str = "", level: int = logging.INFO) -> None:
        frame = inspect.currentframe().f_back
        line_number = frame.f_lineno
        module_name = inspect.getmodule(frame).__name__
        method_name = frame.f_code.co_name
        make_message = f"Module - '{module_name}.py', method - '{method_name}', line - '{line_number}': '{message}'"

        if level == logging.INFO:
            self.logger_info.log(level, make_message)
        elif level == logging.ERROR:
            self.logger_errors.log(level, make_message)
        else:
            self.logger.log(level, make_message)

    def set_format(
        self,
        format_str: str,
        level: int = logging.ERROR,
        date_format: str = "%Y-%m-%d %H:%M:%S",
    ) -> None:

        try:
            for handler in self.logger.handlers:
                if handler.level == level:
                    formatter = logging.Formatter(format_str, datefmt=date_format)
                    handler.setFormatter(formatter)
            self.format_info[level] = format_str

        except Exception as ex:
            self.logger.error(f"while format overriding: {ex}")


current_date = datetime.now().date()
folder_name = current_date.strftime("%Y-%m")


folder_path_info = os.path.join(
    os.path.dirname(__file__), "..", "..", "Log", "INFO", folder_name
)
folder_path_errors = os.path.join(
    os.path.dirname(__file__), "..", "..", "Log", "ERROR", folder_name
)
os.makedirs(folder_path_info, exist_ok=True)
os.makedirs(folder_path_errors, exist_ok=True)

log_file_path = os.path.join(folder_path_info, f"logging_info_{current_date}.log")
log_file_path_errors = os.path.join(
    folder_path_errors, f"logging_errors_{current_date}.log"
)

my_logger = CustomLogger(log_file_path, log_file_path_errors)

if __name__ == "__main__":
    my_logger.log("Hello this is custom logger!")
