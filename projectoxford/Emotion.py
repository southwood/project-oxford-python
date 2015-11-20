from .Base import Base

_emotionRecognizeUrl = 'https://api.projectoxford.ai/emotion/v1.0/recognize'


class Emotion(Base):
    """Client for using the Project Oxford Emotion APIs"""

    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """
        Base.__init__(self, key)

    def recognize(self, options):
        """Recognizes the emotions expressed by one or more people in an image,
        as well as returns a bounding box for the face. The emotions detected are happiness,
        sadness, surprise, anger, fear, contempt, and disgust or neutral.

        Note: exactly one of url, path, or stream must be provided in the options object

        Args:
            options (Object). The Options object describing features to extract
            options.url (string). The Url to image to be thumbnailed
            options.path (string). The Path to image to be thumbnailed
            options.stream (stream). The stream of the image to be used

        Returns:
            object. The resulting image binary stream
        """
        params = {
            'faceRectangles': options['faceRectangles'] if 'faceRectangles' in options else ''
        }

        return Base._postWithOptions(self, _emotionRecognizeUrl, options, params)
