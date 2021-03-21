import configparser
import os

cnx_db = False
config = configparser.ConfigParser()
main_base = os.path.dirname(__file__)

try:
    config.read(os.path.join(main_base, "config.ini"))
except:
    print("Aucun fichier config.ini n'est présent")
    exit()

