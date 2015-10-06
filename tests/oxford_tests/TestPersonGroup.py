import inspect
import json
import os
import time
import unittest
import uuid

from test import test_support

import sys, os, os.path

rootDirectory = os.path.dirname(os.path.realpath('__file__'))
if rootDirectory not in sys.path:
    sys.path.append(os.path.join(rootDirectory, '..'))

from oxford.PersonGroup import PersonGroup

# local file path to test images
localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')

knownFaceIds = []
knownPersonId = ""
client = PersonGroup(os.environ['OXFORD_API_KEY'])

class TestFace(unittest.TestCase):
    '''Tests the oxford API client'''

    def tearDown(self):
        # sleep to prevent throttling
        time.sleep(1)

    def test_constructor_throws_with_no_instrumentation_key(self):
        self.assertRaises(Exception, PersonGroup, None)

    def test_constructor_sets_instrumentation_key(self):
        personGroup = PersonGroup('key')
        self.assertEqual('key', personGroup.key)

    def _learnFaceIds(self):
        if not knownFaceIds:
            from oxford.Face import Face
            faceClient = Face(os.environ['OXFORD_API_KEY'])
            face1 = faceClient.detect({'path': os.path.join(localFilePrefix, 'face1.jpg')})
            face2 = faceClient.detect({'path': os.path.join(localFilePrefix, 'face2.jpg')})
            knownFaceIds.append(face1[0]['faceId'])
            knownFaceIds.append(face2[0]['faceId'])
    
    def _cleanUp(self):
        result = client.list()
        for pg in result:
            client.delete(pg['personGroupId'])

    def test_person_group_create(self):
        personGroupId = str(uuid.uuid4())
        result = client.create(personGroupId, 'python-test-group', 'test-data')
        self.assertIsNone(result, "empty response expected")
        client.delete(personGroupId)

    def test_person_group_list(self):
        personGroupId = str(uuid.uuid4())
        client.create(personGroupId, 'python-test-group', 'test-data')
        result = client.list()
        match = next((x for x in result if x['personGroupId'] == personGroupId), None)

        self.assertEqual(match['personGroupId'], personGroupId)
        self.assertEqual(match['name'], 'python-test-group')
        self.assertEqual(match['userData'], 'test-data')
        client.delete(personGroupId)

    def test_person_group_get(self):
        personGroupId = str(uuid.uuid4())
        client.create(personGroupId, 'python-test-group', 'test-data')
        result = client.get(personGroupId)
        self.assertEqual(result['personGroupId'], personGroupId)
        self.assertEqual(result['name'], 'python-test-group')
        self.assertEqual(result['userData'], 'test-data')
        client.delete(personGroupId)

    def test_person_group_update(self):
        personGroupId = str(uuid.uuid4())
        client.create(personGroupId, 'python-test-group', 'test-data')
        result = client.update(personGroupId, 'python-test-group2', 'test-data2')
        self.assertIsNone(result, "empty response expected")
        client.delete(personGroupId)

    def test_person_group_training(self):
        personGroupId = str(uuid.uuid4())
        client.create(personGroupId, 'python-test-group', 'test-data')
        result = client.trainingStart(personGroupId)
        self.assertEqual(result['status'], 'running')

        countDown = 10
        while countDown > 0 and result['status'] == 'running':
            time.sleep(0.5) # 500ms
            result = client.trainingStatus(personGroupId)
            countdown = countDown - 1

        self.assertNotEqual(result['status'], 'running')
        client.delete(personGroupId)