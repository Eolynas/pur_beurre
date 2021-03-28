import configparser
import logging
import os
from product.config.logger import setup_logging

cnx_db = False
config = configparser.ConfigParser()
main_base = os.path.dirname(__file__)
setup_logging()
logger = logging.getLogger(__name__)


try:
    config.read(os.path.join(main_base, "config.ini"))
except:
    print("Aucun fichier config.ini n'est présent")
    exit()

