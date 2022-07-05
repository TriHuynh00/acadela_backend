from os.path import dirname
import sys

this_folder = dirname(__file__)


# Hook (Http Hook)
class HttpTrigger:
    def __init__(self, on, url, method,
                 lineNumber,
                 failureMessage = None):
        self.on = on
        self.url = url
        self.method = method
        self.failureMessage = failureMessage
        self.lineNumber = lineNumber

