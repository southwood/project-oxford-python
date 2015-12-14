import os
import sys
import unittest
import uuid

rootDirectory = os.path.dirname(os.path.realpath('__file__'))
if rootDirectory not in sys.path:
    sys.path.append(os.path.join(rootDirectory, '..'))

from projectoxford.Client import Client

class TestPersonGroup(unittest.TestCase):
    '''Tests the project oxford API client'''

    @classmethod
    def setUpClass(cls):
        # set up self.client for tests
        cls.client = Client.face(os.environ['OXFORD_FACE_API_KEY'])

        # detect two faces
        cls.knownFaceIds = [];
        cls.localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')
        face1 = cls.client.detect({'path': os.path.join(cls.localFilePrefix, 'face1.jpg')})
        face2 = cls.client.detect({'path': os.path.join(cls.localFilePrefix, 'face2.jpg')})
        cls.knownFaceIds.append(face1[0]['faceId'])
        cls.knownFaceIds.append(face2[0]['faceId'])

    def test_person_group_create_delete(self):
        personGroupId = str(uuid.uuid4())
        result = self.client.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        self.assertIsNone(result, "empty response expected")
        self.client.personGroup.delete(personGroupId)

    def test_person_group_list(self):
        personGroupId = str(uuid.uuid4())
        self.client.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        result = self.client.personGroup.list()
        match = next((x for x in result if x['personGroupId'] == personGroupId), None)

        self.assertEqual(match['personGroupId'], personGroupId)
        self.assertEqual(match['name'], 'python-test-group')
        self.assertEqual(match['userData'], 'test-data')
        self.client.personGroup.delete(personGroupId)

    def test_person_group_get(self):
        personGroupId = str(uuid.uuid4())
        self.client.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        result = self.client.personGroup.get(personGroupId)
        self.assertEqual(result['personGroupId'], personGroupId)
        self.assertEqual(result['name'], 'python-test-group')
        self.assertEqual(result['userData'], 'test-data')
        self.client.personGroup.delete(personGroupId)

    def test_person_group_update(self):
        personGroupId = str(uuid.uuid4())
        self.client.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        result = self.client.personGroup.update(personGroupId, 'python-test-group2', 'test-data2')
        self.assertIsNone(result, "empty response expected")
        self.client.personGroup.delete(personGroupId)

    def test_person_group_training(self):
        personGroupId = str(uuid.uuid4())
        self.client.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        result = self.client.personGroup.trainingStart(personGroupId)
        self.assertEqual(result['status'], 'running')

        countDown = 10
        while countDown > 0 and result['status'] == 'running':
            result = self.client.personGroup.trainingStatus(personGroupId)
            countdown = countDown - 1

        self.assertNotEqual(result['status'], 'running')
        self.client.personGroup.delete(personGroupId)

    def test_person_group_create_or_update(self):
        personGroupId = str(uuid.uuid4())
        self.client.personGroup.createOrUpdate(personGroupId, 'name1')
        result = self.client.personGroup.createOrUpdate(personGroupId, 'name2', 'user-data')
        result = self.client.personGroup.get(personGroupId)

        self.assertEqual(result['name'], 'name2')
        self.assertEqual(result['userData'], 'user-data')

        self.client.personGroup.delete(personGroupId)

    def test_person_group_train_and_poll(self):
        personGroupId = str(uuid.uuid4())
        self.client.personGroup.create(personGroupId, 'python-test-group', 'test-data')
        result = self.client.personGroup.trainAndPollForCompletion(personGroupId)
        self.assertNotEqual(result['status'], 'running')
        self.client.personGroup.delete(personGroupId)