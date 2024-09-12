import logging as lg
import os
from configparser import RawConfigParser
from datetime import date


def today() -> str:
    date_today = date.today()
    return date_today.strftime("%Y-%m-%d")


def get_config(filename: str, section: str) -> dict:
    # create a parser
    parser = RawConfigParser()
    # read config file
    parser.read(filename)

    # get section
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1].replace('[current_date]', today())
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return config


config_filename = "config.ini"

DB_CONFIG = get_config(config_filename, section='db')

LOGGING_CONFIG = get_config(config_filename, section='logging')
lg.basicConfig(**LOGGING_CONFIG)
logger = lg.getLogger()
logger.addHandler(lg.StreamHandler())  # Write log also in stdout
