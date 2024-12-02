import logging
from pathlib import Path
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_dir = Path.cwd() / 'logs' 
logs_dir.mkdir(parents= True, exist_ok = True)

# Full path
LOG_FILE_PATH = logs_dir / LOG_FILE

# Configure logging
logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[%(asctime)s %(lineno)d %(name)s - %(levelname)s - %(message)s]",
    level = logging.INFO,
)


