import json
import requests

_analyzeUrl = 'https://api.projectoxford.ai/vision/v1/analyses';
_thumbnailUrl = 'https://api.projectoxford.ai/vision/v1/thumbnails';
_ocrUrl = 'https://api.projectoxford.ai/vision/v1/ocr';

class Vision(object):
    """Client for using the Project Oxford vision APIs"""

    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """

        if key and isinstance(key, str):
            self.key = key
        else:
            raise Exception('Key is required but a string was not provided')
