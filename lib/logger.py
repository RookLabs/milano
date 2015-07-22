import sys
from ConfigParser import SafeConfigParser
import logging


config = SafeConfigParser()
config.read('milano.cfg')

logging_level = config.get('logging', 'level')

logging_format_string_debug = config.get('logging', 'format_string_debug')
logging_format_string_info = config.get('logging', 'format_string_info')


def get_logger():
    if logging_level == 'debug':
        logging.basicConfig(format=logging_format_string_debug)
    else:
        logging.basicConfig(format=logging_format_string_info, stream=sys.stdout)

    logger = logging.getLogger()

    if logging_level == 'debug':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger
