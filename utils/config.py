import json
import os

from utils.log import Log

log = Log().get_logger(__name__)


class Config(object):
    def __init__(self):
        self.config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "config.json")
        self._read_config()
        log.debug(self.cfg)

    def _read_config(self):
        log.debug("Reading config from: {}".format(self.config_path))
        with open(self.config_path) as config_file:
            self.cfg = json.load(config_file)
