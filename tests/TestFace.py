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

from oxford import Face

# common test options
options = {
    'analyzesFaceLandmarks': True,
    'analyzesAge': True,
    'analyzesGender': True,
    'analyzesHeadPose': True
}

# local file path to test images
localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')

# face client for tests
faceClient = Face.Face(os.environ['OXFORD_API_KEY'])

knownFaceIds = []
personGroupId = uuid.uuid4()
personGroupId2 = uuid.uuid4()
knownPersonId = ""

class TestFace(unittest.TestCase):
    '''Tests the oxford API client'''

    def tearDown(self):
        # sleep 250 ms to prevent throttling
        time.sleep(0.25)

    def test_constructor_throws_with_no_instrumentation_key(self):
        self.assertRaises(Exception, Face.Face, None)

    def test_constructor_sets_instrumentation_key(self):
        face = Face.Face('key')
        self.assertEqual('key', face.key)

    def test_return_throws_for_bad_request(self):
        self.assertRaises(Exception, faceClient.detect, {'url': 'http://bing.com'});

    def _learnFaceIds(self):
        if not knownFaceIds:
            face1 = faceClient.detect({'path': os.path.join(localFilePrefix, 'face1.jpg')})
            face2 = faceClient.detect({'path': os.path.join(localFilePrefix, 'face2.jpg')})
            knownFaceIds.append(face1[0]['faceId'])
            knownFaceIds.append(face2[0]['faceId'])

    #
    # test the detect API
    #
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
        options['url'] = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
        detectResult = faceClient.detect(options)
        self._verifyDetect(detectResult)

    def test_detect_face_file(self):
        options['path'] = os.path.join(localFilePrefix, 'face1.jpg')
        detectResult = faceClient.detect(options)
        self._verifyDetect(detectResult)

    def test_detect_face_stream(self):
        options['stream'] = open(os.path.join(localFilePrefix, 'face1.jpg'), 'rb').read()
        detectResult = faceClient.detect(options)
        self._verifyDetect(detectResult)

    def test_detect_face_throws_invalid_options(self):
        self.assertRaises(Exception, faceClient.detect, {})

    #
    # test the similar API
    #
    def test_similar_faces(self):
        self._learnFaceIds()
        similarResult = faceClient.similar(knownFaceIds[0], [knownFaceIds[1]])
        self.assertIsInstance(similarResult, list, 'similar result is returned')
        self.assertEqual(knownFaceIds[1], similarResult[0]['faceId'], 'expected similar face is returned')

    #
    # test the grouping API
    #
    def test_grouping_faces(self):
        faces = faceClient.detect({'path': os.path.join(localFilePrefix, 'face-group.jpg')})

        faceIds = []
        for face in faces:
            faceIds.append(face['faceId'])

        groupingResult = faceClient.grouping(faceIds)
        self.assertIsInstance(groupingResult, object, 'grouping result is returned')
        self.assertIsInstance(groupingResult['groups'], list, 'groups list is returned')
        self.assertIsInstance(groupingResult['messyGroup'], list, 'messygroup list is returned')

    #
    # test the verify API
    #
    def test_verify_faces(self):
        self._learnFaceIds()
        verifyResult = faceClient.verify(knownFaceIds[0], knownFaceIds[1])
        self.assertIsInstance(verifyResult, object, 'grouping result is returned')
        self.assertEqual(verifyResult['isIdentical'], True, 'verify succeeded')
        self.assertGreaterEqual(verifyResult['confidence'], 0.5, 'confidence is returned')