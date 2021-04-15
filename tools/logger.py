"""read logger.yaml for logging the program"""
import os
import yaml
import logging.config
import logging


def setup_logging(
    default_path="logger.yaml", default_level=logging.INFO, env_key="osmose"
):
    """
    init logger
    :param default_path: default path/name logger.yaml file
    :param default_level: lvl by default for the logger
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print("Error in Logging Configuration. Using default configs")
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print("Failed to load configuration file. Using default configs")
