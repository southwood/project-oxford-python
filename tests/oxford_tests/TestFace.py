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

from oxford.Face import Face
from oxford.Person import Person

# local file path to test images
localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')

knownFaceIds = []
client = Face(os.environ['OXFORD_API_KEY'])

class TestFace(unittest.TestCase):
    '''Tests the oxford face API client'''

    def tearDown(self):
        # sleep to prevent throttling
        time.sleep(1)

    def test_constructor_throws_with_no_instrumentation_key(self):
        self.assertRaises(Exception, Face, None)

    def test_constructor_sets_instrumentation_key(self):
        face = Face('key')
        self.assertEqual('key', face.key)

    def test_constructor_sets_person_group_client(self):
        face = Face('key')
        self.assertIsInstance(face.person, Person)

    def test_return_throws_for_bad_request(self):
        self.assertRaises(Exception, client.detect, {'url': 'http://bing.com'});

    def _learnFaceIds(self):
        if not knownFaceIds:
            face1 = client.detect({'path': os.path.join(localFilePrefix, 'face1.jpg')})
            face2 = client.detect({'path': os.path.join(localFilePrefix, 'face2.jpg')})
            knownFaceIds.append(face1[0]['faceId'])
            knownFaceIds.append(face2[0]['faceId'])

    #
    # test the detect API
    #
    def _getDetectOptions(self):
        return {
            'analyzesFaceLandmarks': True,
            'analyzesAge': True,
            'analyzesGender': True,
            'analyzesHeadPose': True
        }

    def _verifyDetect(self, detectResult):
        faceIdResult = detectResult[0]
        
        self.assertIsInstance(faceIdResult['faceId'], str, 'face ID is returned')
        self.assertIsInstance(faceIdResult['faceRectangle'], object, 'faceRectangle is returned')
        self.assertIsInstance(faceIdResult['faceLandmarks'], object, 'faceLandmarks are returned')
        
        attributes = faceIdResult['attributes']
        self.assertIsInstance(attributes, object, 'attributes are returned')
        self.assertIsInstance(attributes['gender'], str, 'gender is returned')
        self.assertIsInstance(attributes['age'], int, 'age is returned')

    def test_detect_face_url(self):
        options = self._getDetectOptions();
        options['url'] = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
        detectResult = client.detect(options)
        self._verifyDetect(detectResult)

    def test_detect_face_file(self):
        options = self._getDetectOptions();
        options['path'] = os.path.join(localFilePrefix, 'face1.jpg')
        detectResult = client.detect(options)
        self._verifyDetect(detectResult)

    def test_detect_face_stream(self):
        options = self._getDetectOptions();
        options['stream'] = open(os.path.join(localFilePrefix, 'face1.jpg'), 'rb').read()
        detectResult = client.detect(options)
        self._verifyDetect(detectResult)

    def test_detect_face_throws_invalid_options(self):
        self.assertRaises(Exception, client.detect, {})

    #
    # test the similar API
    #
    def test_similar_faces(self):
        self._learnFaceIds()
        similarResult = client.similar(knownFaceIds[0], [knownFaceIds[1]])
        self.assertIsInstance(similarResult, list, 'similar result is returned')
        self.assertEqual(knownFaceIds[1], similarResult[0]['faceId'], 'expected similar face is returned')

    #
    # test the grouping API
    #
    def test_grouping_faces(self):
        faces = client.detect({'path': os.path.join(localFilePrefix, 'face-group.jpg')})

        faceIds = []
        for face in faces:
            faceIds.append(face['faceId'])

        groupingResult = client.grouping(faceIds)
        self.assertIsInstance(groupingResult, object, 'grouping result is returned')
        self.assertIsInstance(groupingResult['groups'], list, 'groups list is returned')
        self.assertIsInstance(groupingResult['messyGroup'], list, 'messygroup list is returned')

    #
    # test the verify API
    #
    def test_verify_faces(self):
        self._learnFaceIds()
        verifyResult = client.verify(knownFaceIds[0], knownFaceIds[1])
        self.assertIsInstance(verifyResult, object, 'grouping result is returned')
        self.assertEqual(verifyResult['isIdentical'], True, 'verify succeeded')
        self.assertGreaterEqual(verifyResult['confidence'], 0.5, 'confidence is returned')
