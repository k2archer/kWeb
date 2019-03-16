# -*- coding: utf-8 -*

import logging
import logging.handlers


def get_logger():
    logger = logging.getLogger("")
    if not logger.handlers:
        try:
            logger.setLevel(logging.INFO)
            format_str = '[%(asctime)s][%(filename)s,%(funcName)s:%(lineno)s][%(name)s]:\n --> %(message)s'
            formatter = logging.Formatter(format_str)
            fh = logging.FileHandler("logger.log")
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        except Exception as e:
            print e
    return logger


def get_logger_to_console():
    logger = logging.getLogger("")
    if not logger.handlers:
        try:
            logger.setLevel(logging.INFO)
            format_str = '[%(asctime)s][%(filename)s,%(funcName)s:%(lineno)s][%(name)s]:\n --> %(message)s'
            formatter = logging.Formatter(format_str)
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        except Exception as e:
            print e
    return logger
