import os


class ConfigurationFileException(Exception):
    def __init__(self, filename, message=None):
        self.filename = filename
        self.basename = os.path.basename(filename)
        self._message = str(message) if message is not None else "file error"

    def __str__(self):
        return "file: %s invalid, error: %s" % (self.basename, self.message)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
