import logging
from logging.handlers import RotatingFileHandler

from src.configs.config import get_settings

logger = logging.getLogger("MyClassApi")
logger.setLevel(level=get_settings().LOG_LEVEL)

formatter = logging.Formatter(get_settings().LOG_FORMAT)

if get_settings().LOG_WRITE_STATUS:
    filehandler = RotatingFileHandler(
        filename=get_settings().LOG_FILE,
        backupCount=get_settings().LOG_BACKUP_COUNT,
        mode='w'
    )
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

