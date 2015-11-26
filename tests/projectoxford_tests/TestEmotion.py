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
from projectoxford.Emotion import Emotion


class TestEmotion(unittest.TestCase):
    '''Tests the project oxford Emotion API self.client'''

    @classmethod
    def setUpClass(cls):
        # set up self.client for tests
        cls.client = Client(os.environ['OXFORD_EMOTION_API_KEY'])

        cls.localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')

        # set common recognize options
        cls.recognizeOptions = {
            'faceRectangles': ''
        }

    #
    # test the recognize API
    #
    def _verifyRecognize(self, recognizeResult):
        for emotionResult in recognizeResult:
            self.assertIsInstance(emotionResult['faceRectangle'], object, 'face rectangle is returned')
            scores = emotionResult['scores']
            self.assertIsInstance(scores, object, 'scores are returned')

    def test_emotion_recognize_url(self):
        options = copy.copy(self.recognizeOptions)
        options['url'] = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
        recognizeResult = self.client.emotion.recognize(options)
        self._verifyRecognize(recognizeResult)

    def test_emotion_recognize_file(self):
        options = copy.copy(self.recognizeOptions)
        options['path'] = os.path.join(self.localFilePrefix, 'face1.jpg')
        recognizeResult = self.client.emotion.recognize(options)
        self._verifyRecognize(recognizeResult)

    def test_emotion_recognize_stream(self):
        options = copy.copy(self.recognizeOptions)
        with open(os.path.join(self.localFilePrefix, 'face1.jpg'), 'rb') as file:
            options['stream'] = file.read()
            recognizeResult = self.client.emotion.recognize(options)
        self._verifyRecognize(recognizeResult)

    def test_emotion_recognize_throws_invalid_options(self):
        self.assertRaises(Exception, self.client.emotion.recognize, {})
