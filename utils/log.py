import logging
import sys


class Log(object):

    @staticmethod
    def get_logger(name):
        log = logging.getLogger(name)
        Log()._format_logger(log)
        log.propagate = False
        return log

    @staticmethod
    def _format_logger(log, level=logging.DEBUG):
        log.setLevel(level)
        # log format
        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # log handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(log_format)
        log.addHandler(ch)
