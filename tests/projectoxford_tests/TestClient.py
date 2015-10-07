import unittest
import inspect
import json

from test import test_support

import sys, os, os.path

__file__ == '__file__'

rootDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
if rootDirectory not in sys.path:
    sys.path.append(rootDirectory)

from projectoxford.Client import Client

class TestClient(unittest.TestCase):
    """Tests the project oxford API client"""
    
    def test_constructor_throws_with_no_instrumentation_key(self):
        self.assertRaises(Exception, Client, None)

    def test_constructor_sets_instrumentation_key(self):
        oxford = Client('key')
        self.assertEqual('key', oxford.key)

    def test_face_return_throws_for_bad_request(self):
        client = Client('key')
        self.assertRaises(Exception, client.face.detect, {'url': 'http://bing.com'});