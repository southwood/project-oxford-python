import json
import requests

_detectUrl = 'https://api.projectoxford.ai/face/v0/detections';
_similarUrl = 'https://api.projectoxford.ai/face/v0/findsimilars';
_groupingUrl = 'https://api.projectoxford.ai/face/v0/groupings';
_identifyUrl = 'https://api.projectoxford.ai/face/v0/identifications';
_verifyUrl = 'https://api.projectoxford.ai/face/v0/verifications';
_personGroupUrl = 'https://api.projectoxford.ai/face/v0/persongroups';
_personUrl = 'https://api.projectoxford.ai/face/v0/persongroups';

class Face(object):
    """Client for using the Project Oxford face APIs"""
    
    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """

        if key and isinstance(key, str):
            self.key = key
        else:
            raise Exception('Key is required but a string was not provided')
