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
from oxford.Person import Person

class TestPerson(unittest.TestCase):
    '''Tests the oxford API client'''

    @classmethod
    def setUpClass(cls):
        # set up client for tests
        cls.client = Client(os.environ['oxford_api_key'])

        # detect two faces
        cls.knownFaceIds = [];
        localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')
        face1 = cls.client.face.detect({'path': os.path.join(localFilePrefix, 'face1.jpg')})
        face2 = cls.client.face.detect({'path': os.path.join(localFilePrefix, 'face2.jpg')})
        cls.knownFaceIds.append(face1[0]['faceId'])
        cls.knownFaceIds.append(face2[0]['faceId'])
        
        # create a person group
        cls.personGroupId = str(uuid.uuid4())
        cls.client.face.personGroup.create(cls.personGroupId, 'test-person-group')
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.client.face.personGroup.delete(cls.personGroupId)
        return super().tearDownClass()

    def test_person_create_update_get_delete(self):
        # create
        result = self.client.face.person.create(self.personGroupId, self.knownFaceIds, 'billg', 'test-person')
        personId = result['personId']
        self.assertIsInstance(personId, str, 'person id was returned')

        # update
        result = self.client.face.person.update(self.personGroupId, personId, self.knownFaceIds, 'bill gates', 'test-person')
        self.assertIsNone(result, 'person was updated')

        # get
        result = self.client.face.person.get(self.personGroupId, personId)
        personIdVerify = result['personId']
        self.assertEqual(personId, personIdVerify, 'person id was verified')

        # delete
        self.client.face.person.delete(self.personGroupId, personId)
        self.assertTrue(True, 'person was deleted')

    def test_person_face_add_update_delete(self):
        # create
        result = self.client.face.person.create(self.personGroupId, [self.knownFaceIds[0]], 'billg', 'test-person')
        personId = result['personId']
        self.assertIsInstance(personId, str, 'create succeeded')

        # add a new face ID
        self.client.face.person.addFace(self.personGroupId, personId, self.knownFaceIds[1])
        self.assertTrue(True, 'add succeeded')

        # delete the original face ID
        self.client.face.person.deleteFace(self.personGroupId, personId, self.knownFaceIds[0])
        self.assertTrue(True, 'delete succeeded')

        # verify expected face ID
        self.assertRaises(Exception, self.client.face.person.getFace, self.personGroupId, personId, self.knownFaceIds[0])
        face = self.client.face.person.getFace(self.personGroupId, personId, self.knownFaceIds[1])
        self.assertEqual(face['faceId'], self.knownFaceIds[1])

    def test_person_list(self):
        # create some people
        result1 = self.client.face.person.create(self.personGroupId, [self.knownFaceIds[0]], 'billg1', 'test-person')
        result2 = self.client.face.person.create(self.personGroupId, [self.knownFaceIds[1]], 'billg2', 'test-person')
        
        # list them
        listResult = self.client.face.person.list(self.personGroupId)
        self.assertEqual(len(listResult), 2)
