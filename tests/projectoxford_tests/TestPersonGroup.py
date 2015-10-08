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

class TestPersonGroup(unittest.TestCase):
    '''Tests the project oxford API client'''

    @classmethod
    def setUpClass(cls):
        # set up self.client for tests
        cls.client = Client(os.environ['OXFORD_FACE_API_KEY'])

        # detect two faces
        cls.knownFaceIds = [];
        cls.localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')
        face1 = cls.client.face.detect({'path': os.path.join(cls.localFilePrefix, 'face1.jpg')})
        face2 = cls.client.face.detect({'path': os.path.join(cls.localFilePrefix, 'face2.jpg')})
        cls.knownFaceIds.append(face1[0]['faceId'])
        cls.knownFaceIds.append(face2[0]['faceId'])

    def test_person_group_create_delete(self):
        personGroupId = str(uuid.uuid4())
        result = self.client.face.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        self.assertIsNone(result, "empty response expected")
        self.client.face.personGroup.delete(personGroupId)

    def test_person_group_list(self):
        personGroupId = str(uuid.uuid4())
        self.client.face.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        result = self.client.face.personGroup.list()
        match = next((x for x in result if x['personGroupId'] == personGroupId), None)

        self.assertEqual(match['personGroupId'], personGroupId)
        self.assertEqual(match['name'], 'python-test-group')
        self.assertEqual(match['userData'], 'test-data')
        self.client.face.personGroup.delete(personGroupId)

    def test_person_group_get(self):
        personGroupId = str(uuid.uuid4())
        self.client.face.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        result = self.client.face.personGroup.get(personGroupId)
        self.assertEqual(result['personGroupId'], personGroupId)
        self.assertEqual(result['name'], 'python-test-group')
        self.assertEqual(result['userData'], 'test-data')
        self.client.face.personGroup.delete(personGroupId)

    def test_person_group_update(self):
        personGroupId = str(uuid.uuid4())
        self.client.face.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        result = self.client.face.personGroup.update(personGroupId, 'python-test-group2', 'test-data2')
        self.assertIsNone(result, "empty response expected")
        self.client.face.personGroup.delete(personGroupId)

    def test_person_group_training(self):
        personGroupId = str(uuid.uuid4())
        self.client.face.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        result = self.client.face.personGroup.trainingStart(personGroupId)
        self.assertEqual(result['status'], 'running')

        countDown = 10
        while countDown > 0 and result['status'] == 'running':
            result = self.client.face.personGroup.trainingStatus(personGroupId)
            countdown = countDown - 1

        self.assertNotEqual(result['status'], 'running')
        self.client.face.personGroup.delete(personGroupId)

    def test_person_group_create_or_update(self):
        personGroupId = str(uuid.uuid4())
        self.client.face.personGroup.createOrUpdate(personGroupId, 'name1')
        result = self.client.face.personGroup.createOrUpdate(personGroupId, 'name2', 'user-data')
        result = self.client.face.personGroup.get(personGroupId)

        self.assertEqual(result['name'], 'name2')
        self.assertEqual(result['userData'], 'user-data')

        self.client.face.personGroup.delete(personGroupId)

    def test_person_group_train_and_poll(self):
        personGroupId = str(uuid.uuid4())
        self.client.face.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        result = self.client.face.personGroup.trainAndPollForCompletion(personGroupId)
        self.assertNotEqual(result['status'], 'running')
        self.client.face.personGroup.delete(personGroupId)