import stat
import os
import logging
import platform
import collections
import contextlib

from selenium.webdriver import Chrome, ChromeOptions as _ChromeOptions

from pylivingkit.selenium import common as pylibutils_selenium_common


if pylibutils_selenium_common.WEBDRIVER_REQUEST_LOGGING:
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.DEBUG)

CHROMEDRIVER_LOGLEVEL = ["ALL", "DEBUG", "INFO", "WARNING", "SERVER", "OFF"]
# https://www.chromium.org/developers/how-tos/run-chromium-with-flags
# https://chromium.googlesource.com/chromium/src/+/refs/heads/main/chrome/common/chrome_switches.h
# one of the .cc files corresponding to the *_switches.h files
CHROME_COMMAND_LINE_FLAGS = (
    os.getenv("CHROME_COMMAND_LINE_FLAGS", "--no-proxy-server, --ignore-certificates-error").replace(",", " ").split()
)


class ChromeOptions(_ChromeOptions):
    # https://chromedriver.chromium.org/capabilities: prefs: chrome://version/ -> Profile Path -> Preferences
    # self.add_experimental_option
    def __init__(self):
        super(__class__, self).__init__()
        collections.deque(map(self.add_argument, CHROME_COMMAND_LINE_FLAGS), maxlen=0)


chrome_options = ChromeOptions()


@contextlib.contextmanager
def chrome_driver(executable_path, chromedriver_loglevel="INFO", **kwargs):
    """Wrapper selenium.webdriver.Chrome for making a living.

    executable_path download from https://chromedriver.chromium.org/downloads
    """
    if chromedriver_loglevel not in CHROMEDRIVER_LOGLEVEL:
        raise ValueError("chromedriver do not support %r loglevel" % chromedriver_loglevel)
    executable_path = kwargs.pop("executable_path", executable_path)
    if platform.system() != "Windows":
        os.chmod(executable_path, stat.S_IRWXU, follow_symlinks=True)
    self_chrome_driver = Chrome(
        executable_path=executable_path,
        service_log_path=kwargs.pop("service_log_path", os.path.join(os.getcwd(), "chromedriver.log")),
        service_args=kwargs.pop(
            "service_args",
            [
                "--log-level=%s" % chromedriver_loglevel, "--append-log", "--readable-timestamp",
            ],
        ),
        options=chrome_options,
        **kwargs
    )
    try:
        yield self_chrome_driver
    finally:
        self_chrome_driver.close()
