import inspect
import os
import sys
import unittest
import uuid

rootDirectory = os.path.dirname(os.path.realpath('__file__'))
if rootDirectory not in sys.path:
    sys.path.append(os.path.join(rootDirectory, '..'))

from test import test_support
from oxford.Client import Client
from oxford.Face import Face
from oxford.Person import Person
from oxford.PersonGroup import PersonGroup

class TestFace(unittest.TestCase):
    '''Tests the oxford face API self.client'''

    @classmethod
    def setUpClass(cls):
        # set up self.client for tests
        cls.client = Client(os.environ['OXFORD_VISION_API_KEY'])
        cls.localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')
        return super().setUpClass()

    #
    # test the analyze API
    #
    def _verify_analyze_result(self, result):
        self.assertIsNotNone(result['imageType'])
        self.assertIsNotNone(result['color'])
        self.assertIsNotNone(result['faces'])
        self.assertIsNotNone(result['adult'])
        self.assertIsNotNone(result['categories'])

    def test_vision_analyze_file(self):
        options = {
            'path': os.path.join(self.localFilePrefix, 'vision.jpg'),
            'ImageType': True,
            'Color': True,
            'Faces': True,
            'Adult': True,
            'Categories': True
        }

        result = self.client.vision.analyze(options)
        self._verify_analyze_result(result)

    def test_vision_analyze_url(self):
        options = {
            'url': 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg',
            'ImageType': True,
            'Color': True,
            'Faces': True,
            'Adult': True,
            'Categories': True
        }

        result = self.client.vision.analyze(options)
        self._verify_analyze_result(result)

    def test_vision_analyze_stream(self):
        options = {
            'path': os.path.join(self.localFilePrefix, 'vision.jpg'),
            'ImageType': True,
            'Color': True,
            'Faces': True,
            'Adult': True,
            'Categories': True
        }

        with open(os.path.join(self.localFilePrefix, 'face1.jpg'), 'rb') as file:
            options['stream'] = file.read()
            result = self.client.vision.analyze(options)
        
        self._verify_analyze_result(result)