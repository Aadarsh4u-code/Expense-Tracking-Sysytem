import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Format to how log file is created
LOG_FILE_NAME = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
LOGS_DIR = 'logs'

ROOT_DIR = Path(__file__).resolve().parent.parent  # or .parent.parent if inside a subfolder

# Path for a log file
LOGS_FILE_PATH = os.path.join(ROOT_DIR, LOGS_DIR, LOG_FILE_NAME)

# Even there is file keep on appending
os.makedirs(LOGS_DIR, exist_ok=True)  



# If handlers is used inside basicConfig then filename and filemode is not used else vice-versa
logging.basicConfig(
    # filename=logs_file_path,
    # filemode='w',
    level=logging.DEBUG,
    format="[ %(asctime)s ] %(filename)s:%(lineno)d %(name)s - %(levelname)s - %(message)s",
    # format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOGS_FILE_PATH), # Output logs to the file 
        logging.StreamHandler(sys.stdout) # Output logs in the terminal/console
    ]
)


# # Logging with Multiple Loggers
logger = logging.getLogger('expense_tracking')

# Log message with different severity levels
'''
logging.debug("This is dubug message")
logging.info("This is info message")
logging.warning("This is warning message")
logging.error("This is error message")
logging.critical("This is critical message")
'''