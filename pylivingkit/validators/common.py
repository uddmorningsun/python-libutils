import os
import typing
import collections

from pylivingkit.common import constants
from pylivingkit.common.exceptions import ConfigurationFileException


class CommonValidator(collections.namedtuple("CommonValidator", "filepath")):
    # https://docs.python.org/3.7/reference/datamodel.html#object.__getattribute__
    def __getattribute__(self, item):
        if item == "filepath":
            return os.path.realpath(object.__getattribute__(self, item))
        return object.__getattribute__(self, item)

    def __str__(self):
        return "<class %s> filepath: %r" % (self.__class__.__name__, self.filepath)

    def validate_size(self, filesize=None, message=None):
        message = message or "file: %s oversize default filesize(%s bytes)" % (
            self.filepath,
            constants.CONFIGFILE_MAX_FILESIZE,
        )
        if os.path.getsize(self.filepath) > filesize or constants.CONFIGFILE_MAX_FILESIZE:
            raise ConfigurationFileException(self.filepath, message=message)
        return self

    def validate_suffix(self, suffixes: typing.Union[typing.List, typing.Tuple], message=None):
        _, file_suffix = os.path.splitext(self.filepath)
        message = message or "file: %s suffix: %s is not valid" % (self.filepath, file_suffix)
        if file_suffix not in suffixes:
            raise ConfigurationFileException(self.filepath, message=message)
        return self

    def validate_exist(self, message=None):
        message = message or "file: %s not found"
        if not os.path.exists(self.filepath):
            raise ConfigurationFileException(self.filepath, message=message)
        return self
