from .Face import Face
from .Vision import Vision
from .Emotion import Emotion


class Client(object):
    """Client for using project oxford APIs"""

    @staticmethod
    def face(key):
        """The face API interface.
        Returns:
            :class:`face`. the face API instance.
        Args:
            key (str). the API key to use for this client.
        """

        if key and isinstance(key, str):
            return Face(key)
        else:
            raise Exception('Key is required but a string was not provided')

    @staticmethod
    def vision(key):
        """The vision API interface.
        Returns:
            :class:`vision`. the vision API instance.
        Args:
            key (str). the API key to use for this client.
        """
        if key and isinstance(key, str):
            return Vision(key)
        else:
            raise Exception('Key is required but a string was not provided')

    @staticmethod
    def emotion(key):
        """The emotion API interface.
        Returns:
            :class:`emotion`. the emotion API instance.
        Args:
            key (str). the API key to use for this client.
        """
        if key and isinstance(key, str):
            return Emotion(key)
        else:
            raise Exception('Key is required but a string was not provided')
