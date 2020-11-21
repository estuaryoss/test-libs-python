import datetime
import os
import platform

from fluentd_logger.about import properties


class Fluentd:

    def __init__(self, logger):
        self.logger = logger

    def emit(self, tag, msg):
        message = self.__enrichlog("INFO", msg)
        response = self.__send(tag, message)
        return {"emit": response,
                "message": message}

    @staticmethod
    def __enrichlog(level_code, msg):
        return {
            "name": properties.get('name'),
            "version": properties.get('version'),
            "uname": list(platform.uname()),
            "python": platform.python_version(),
            "pid": os.getpid(),
            "level_code": level_code,
            "msg": msg,
            "timestamp": str(datetime.datetime.now()),
        }

    def __send(self, tag, msg):
        return str(self.logger.emit(tag, msg)).lower()
