WEBDRIVER_REQUEST_LOGGING = False


def enable_webdriver_request_logging():
    """Enable and setting connection debug level for the remote WebDriver server"""
    global WEBDRIVER_REQUEST_LOGGING

    WEBDRIVER_REQUEST_LOGGING = True
