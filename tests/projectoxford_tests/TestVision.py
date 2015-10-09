import copy
import inspect
import os
import sys
import unittest
import uuid

rootDirectory = os.path.dirname(os.path.realpath('__file__'))
if rootDirectory not in sys.path:
    sys.path.append(os.path.join(rootDirectory, '..'))

from test import test_support
from projectoxford.Client import Client
from projectoxford.Face import Face
from projectoxford.Person import Person
from projectoxford.PersonGroup import PersonGroup

class TestFace(unittest.TestCase):
    '''Tests the project oxford face API self.client'''

    @classmethod
    def setUpClass(cls):
        # set up self.client for tests
        cls.client = Client(os.environ['OXFORD_VISION_API_KEY'])
        cls.localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')
        cls.analyzeOptions = {
            'ImageType': True,
            'Color': True,
            'Faces': True,
            'Adult': True,
            'Categories': True
        }

        cls.thumbnailOptions = {
            'width': 100,
            'height': 100,
            'smartCropping': True
        }

        cls.ocrOptions = {
            'language': 'en',
            'detectOrientation': True
        }

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
        options = copy.copy(self.analyzeOptions)
        options['path'] = os.path.join(self.localFilePrefix, 'vision.jpg')
        result = self.client.vision.analyze(options)
        self._verify_analyze_result(result)

    def test_vision_analyze_url(self):
        options = copy.copy(self.analyzeOptions)
        options['url'] = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
        result = self.client.vision.analyze(options)
        self._verify_analyze_result(result)

    def test_vision_analyze_stream(self):
        options = copy.copy(self.analyzeOptions)
        with open(os.path.join(self.localFilePrefix, 'face1.jpg'), 'rb') as file:
            options['stream'] = file.read()
            result = self.client.vision.analyze(options)
        
        self._verify_analyze_result(result)

    #
    # test the thumbnail API
    #
    def _verify_thumbnail_result(self, result, fileName):
        outputPath = os.path.join(self.localFilePrefix, fileName)
        with open(outputPath, 'wb+') as file: file.write(result)
        self.assertTrue(True, 'file write succeeded for: {0}'.format(fileName))

    def test_vision_thumbnail_file(self):
        options = copy.copy(self.thumbnailOptions)
        options['path'] = os.path.join(self.localFilePrefix, 'vision.jpg')
        result = self.client.vision.thumbnail(options)
        self._verify_thumbnail_result(result, 'thumbnail_from_file.jpg')

    #def test_vision_thumbnail_url(self):
    #    options = copy.copy(self.thumbnailOptions)
    #    options['url'] = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
    #    result = self.client.vision.thumbnail(options)
    #    self._verify_thumbnail_result(result, 'thumbnail_from_url.jpg')

    #def test_vision_thumbnail_stream(self):
    #    options = copy.copy(self.thumbnailOptions)
    #    with open(os.path.join(self.localFilePrefix, 'face1.jpg'), 'rb') as file:
    #        options['stream'] = file.read()
    #        result = self.client.vision.thumbnail(options)
    #    self._verify_thumbnail_result(result, 'thumbnail_from_stream.jpg')

    #
    # test the OCR API
    #
    def _verify_ocr_result(self, result):
        self.assertIsNotNone(result['language'])
        self.assertIsNotNone(result['orientation'])

    def test_vision_ocr_file(self):
        options = copy.copy(self.ocrOptions)
        options['path'] = os.path.join(self.localFilePrefix, 'vision.jpg')
        result = self.client.vision.ocr(options)
        self._verify_ocr_result(result)

    def test_vision_ocr_url(self):
        options = copy.copy(self.ocrOptions)
        options['url'] = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
        result = self.client.vision.ocr(options)
        self._verify_ocr_result(result)

    def test_vision_ocr_stream(self):
        options = copy.copy(self.ocrOptions)
        with open(os.path.join(self.localFilePrefix, 'face1.jpg'), 'rb') as file:
            options['stream'] = file.read()
            result = self.client.vision.ocr(options)
        
        self._verify_ocr_result(result)