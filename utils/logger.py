import builtins
import logging
from pathlib import Path
import sys

def override_print_with_logger(logger: logging.Logger):
    """
    Override the builtin print function to log messages
    to the provided logger, as well as printing to the 
    stdout (the notebook console).

    Args:
        logger (logging.Logger): The logger to which print statements will be logged.

    Notes:
        - This will log all print statements as INFO level in the logger
        - The notebook console will still show the print output as normal
        - You need to create a custom logger <see create_custom_logger> and pass it to this function to use it.
        - You also need to capture the original print function. see the #usage section for an example
    Usage:
        ```python
        custom_logger = create_custom_logger(log_path, logger_name='custom')
        original_print = print
        override_print_with_logger(custom_logger)
        ```
    """
    def new_print(*args, **kwargs):
        message = ' '.join(str(arg) for arg in args)
        logger.info(message)
    builtins.print = new_print


def create_custom_logger(log_path: Path, logger_name) -> logging.Logger:
    """
    Create a logger for the that logs to the notebook console, 
    and to the file defined in `log_path` with a timestamped 
    directory structure.

    Notes:
        - The logger will log INFO and above
        - The notebook console will show DEBUG and above

    Args:
        log_path (Path): The path where the log file will be stored. 
                         The logger will create the necessary directories if they do not exist.
    Returns:
        logging.Logger: Configured custom logger for the .
    """
    custom_logger = logging.getLogger(logger_name)
    custom_logger.setLevel(logging.DEBUG) # Set the lowest level you want to capture

    # Clear existing handlers to prevent duplicate logs when re-running cells
    if custom_logger.hasHandlers():
        custom_logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_path.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path / '__economy_log.txt.log')
    file_handler.setLevel(logging.INFO) # File gets INFO and above
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG) # Notebook gets DEBUG and above
    stream_handler.setFormatter(formatter)

    custom_logger.addHandler(file_handler)
    custom_logger.addHandler(stream_handler)

    return custom_logger