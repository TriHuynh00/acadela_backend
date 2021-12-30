from os.path import dirname
import sys

this_folder = dirname(__file__)


# Hook (Http Hook)
class HttpTrigger:
    def __init__(self, on, url, method,
                 line_number,
                 failureMessage = None):
        self.on = on
        self.url = url
        self.method = method
        self.failureMessage = failureMessage
        self.line_number = line_number

