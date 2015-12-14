import os
import sys
import unittest
import uuid

rootDirectory = os.path.dirname(os.path.realpath('__file__'))
if rootDirectory not in sys.path:
    sys.path.append(os.path.join(rootDirectory, '..'))

from projectoxford.Client import Client

class TestPerson(unittest.TestCase):
    '''Tests the project oxford API client'''

    @classmethod
    def setUpClass(cls):
        # set up client for tests
        cls.client = Client.face(os.environ['OXFORD_FACE_API_KEY'])

        # detect two faces
        cls.knownFaceIds = [];
        localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')
        face1 = cls.client.detect({'path': os.path.join(localFilePrefix, 'face1.jpg')})
        face2 = cls.client.detect({'path': os.path.join(localFilePrefix, 'face2.jpg')})
        cls.knownFaceIds.append(face1[0]['faceId'])
        cls.knownFaceIds.append(face2[0]['faceId'])
        
        # create a person group
        cls.personGroupId = str(uuid.uuid4())
        cls.client.personGroup.create(cls.personGroupId, 'test-person-group')

    @classmethod
    def tearDownClass(cls):
        cls.client.personGroup.delete(cls.personGroupId)

    def test_person_create_update_get_delete(self):
        # create
        result = self.client.person.create(self.personGroupId, self.knownFaceIds, 'billg', 'test-person')
        personId = result['personId']
        self.assertIsInstance(personId, object, 'person id was returned')

        # update
        result = self.client.person.update(self.personGroupId, personId, self.knownFaceIds, 'bill gates', 'test-person')
        self.assertIsNone(result, 'person was updated')

        # get
        result = self.client.person.get(self.personGroupId, personId)
        personIdVerify = result['personId']
        self.assertEqual(personId, personIdVerify, 'person id was verified')

        # delete
        self.client.person.delete(self.personGroupId, personId)
        self.assertTrue(True, 'person was deleted')

    def test_person_face_add_update_delete(self):
        # create
        result = self.client.person.create(self.personGroupId, [self.knownFaceIds[0]], 'billg', 'test-person')
        personId = result['personId']
        self.assertIsInstance(personId, object, 'create succeeded')

        # add a new face ID
        self.client.person.addFace(self.personGroupId, personId, self.knownFaceIds[1])
        self.assertTrue(True, 'add succeeded')

        # delete the original face ID
        self.client.person.deleteFace(self.personGroupId, personId, self.knownFaceIds[0])
        self.assertTrue(True, 'delete succeeded')

        # verify expected face ID
        self.assertIsNone(self.client.person.getFace(self.personGroupId, personId, self.knownFaceIds[0]))
        face = self.client.person.getFace(self.personGroupId, personId, self.knownFaceIds[1])
        self.assertEqual(face['faceId'], self.knownFaceIds[1])

        # clean up
        self.client.person.delete(self.personGroupId, personId)

    def test_person_list(self):
        # create some people
        self.client.person.create(self.personGroupId, [self.knownFaceIds[0]], 'billg1', 'test-person')
        self.client.person.create(self.personGroupId, [self.knownFaceIds[1]], 'billg2', 'test-person')
        
        # list them
        listResult = self.client.person.list(self.personGroupId)
        self.assertEqual(len(listResult), 2)

        # remove them
        for person in listResult:
            self.client.person.delete(self.personGroupId, person['personId'])

    def test_person_create_or_update(self):
        self.client.person.createOrUpdate(self.personGroupId, [self.knownFaceIds[0]], 'billg1', 'test-person')
        result = self.client.person.createOrUpdate(self.personGroupId, [self.knownFaceIds[1]], 'billg1', 'test-person-updated')
        result = self.client.person.get(self.personGroupId, result['personId'])

        self.assertEqual(result['userData'], 'test-person-updated')

        self.client.person.delete(self.personGroupId, result['personId'])