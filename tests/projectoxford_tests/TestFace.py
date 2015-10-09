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
        cls.client = Client(os.environ['OXFORD_FACE_API_KEY'])

        # detect two faces
        cls.knownFaceIds = [];
        cls.localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')
        face1 = cls.client.face.detect({'path': os.path.join(cls.localFilePrefix, 'face1.jpg')})
        face2 = cls.client.face.detect({'path': os.path.join(cls.localFilePrefix, 'face2.jpg')})
        cls.knownFaceIds.append(face1[0]['faceId'])
        cls.knownFaceIds.append(face2[0]['faceId'])

        # set common detect options
        cls.detectOptions = {
            'analyzesFaceLandmarks': True,
            'analyzesAge': True,
            'analyzesGender': True,
            'analyzesHeadPose': True
        }

    #
    # test the detect API
    #
    def _verifyDetect(self, detectResult):
        faceIdResult = detectResult[0]
        
        self.assertIsInstance(faceIdResult['faceId'], object, 'face ID is returned')
        self.assertIsInstance(faceIdResult['faceRectangle'], object, 'faceRectangle is returned')
        self.assertIsInstance(faceIdResult['faceLandmarks'], object, 'faceLandmarks are returned')
        
        attributes = faceIdResult['attributes']
        self.assertIsInstance(attributes, object, 'attributes are returned')
        self.assertIsInstance(attributes['gender'], object, 'gender is returned')
        self.assertIsInstance(attributes['age'], int, 'age is returned')

    def test_face_detect_url(self):
        options = copy.copy(self.detectOptions)
        options['url'] = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
        detectResult = self.client.face.detect(options)
        self._verifyDetect(detectResult)

    def test_face_detect_file(self):
        options = copy.copy(self.detectOptions)
        options['path'] = os.path.join(self.localFilePrefix, 'face1.jpg')
        detectResult = self.client.face.detect(options)
        self._verifyDetect(detectResult)

    def test_face_detect_stream(self):
        options = copy.copy(self.detectOptions)
        with open(os.path.join(self.localFilePrefix, 'face1.jpg'), 'rb') as file:
            options['stream'] = file.read()
            detectResult = self.client.face.detect(options)
        self._verifyDetect(detectResult)

    def test_face_detect_throws_invalid_options(self):
        self.assertRaises(Exception, self.client.face.detect, {})

    #
    # test the similar API
    #
    def test_face_similar(self):
        similarResult = self.client.face.similar(self.knownFaceIds[0], [self.knownFaceIds[1]])
        self.assertIsInstance(similarResult, list, 'similar result is returned')
        self.assertEqual(self.knownFaceIds[1], similarResult[0]['faceId'], 'expected similar face is returned')

    #
    # test the grouping API
    #
    def test_face_grouping(self):
        faces = self.client.face.detect({'path': os.path.join(self.localFilePrefix, 'face-group.jpg')})


        faceIds = []
        for face in faces:
            faceIds.append(face['faceId'])

        groupingResult = self.client.face.grouping(faceIds)
        self.assertIsInstance(groupingResult, object, 'grouping result is returned')
        self.assertIsInstance(groupingResult['groups'], list, 'groups list is returned')
        self.assertIsInstance(groupingResult['messyGroup'], list, 'messygroup list is returned')

    #
    # test the verify API
    #
    def test_face_verify(self):
        verifyResult = self.client.face.verify(self.knownFaceIds[0], self.knownFaceIds[1])
        self.assertIsInstance(verifyResult, object, 'grouping result is returned')
        self.assertEqual(verifyResult['isIdentical'], True, 'verify succeeded')
        self.assertGreaterEqual(verifyResult['confidence'], 0.5, 'confidence is returned')

    #
    # test the identify API
    #
    def test_face_identify(self):
        self.client.face.personGroup.createOrUpdate('testgroup', 'name')
        faceId = self.client.face.detect({'path': os.path.join(self.localFilePrefix, 'face1.jpg')})[0]['faceId']
        personId = self.client.face.person.createOrUpdate('testgroup', [faceId], 'billG')['personId']
        self.client.face.personGroup.trainAndPollForCompletion('testgroup')
        faceId2 = self.client.face.detect({'path': os.path.join(self.localFilePrefix, 'face2.jpg')})[0]['faceId']
        identifyResult = self.client.face.identify('testgroup', [faceId2])

        self.assertIsInstance(identifyResult, object, 'identify result is returned')
        self.assertEqual(identifyResult[0]['candidates'][0]['personId'], personId)
        self.client.face.personGroup.delete('testgroup')