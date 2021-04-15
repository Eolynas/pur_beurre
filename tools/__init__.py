import logging
from tools.config_manager import ConfigManager
from tools.logger import setup_logging

config = ConfigManager()
setup_logging()
logger = logging.getLogger(__name__)