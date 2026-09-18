from configs.config import GLOBAL_ECONOMY_LOG_DIR
import datetime
from pathlib import Path
from utils.logger import create_custom_logger, override_print_with_logger

now = datetime.datetime.now()
log_path = Path(GLOBAL_ECONOMY_LOG_DIR) / f"{now.year:04d}" / f"{now.month:02d}" / f"{now.day:02d}"
    
economy_logger = create_custom_logger(log_path, logger_name='economy')
original_print = print
override_print_with_logger(economy_logger)
economy_logger.info('Starting economy simulation at {}'.format(now.strftime("%Y-%m-%d %H:%M:%S")))

print_test_statements = True
if print_test_statements:
    # These are test lines to verify that the logger is working correctly. 
    # Set print_test_statements to False to disable them.
    economy_logger.debug("TEST: This is a DEBUG message (only in notebook)")
    economy_logger.info("TEST: This is an INFO message (in both file and notebook)")
    economy_logger.error("TEST: This is an ERROR message (in both file and notebook)")
    print("TEST: This is a test print statement (should appear in both file and notebook)")