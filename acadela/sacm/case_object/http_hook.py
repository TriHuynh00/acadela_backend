from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

# Hook (Http Hook)
class HttpTrigger:
    def __init__(self, on, url, method,
                 failureMessage = None):
        self.on = on
        self.url = url
        self.method = method
        self.failureMessage = failureMessage

