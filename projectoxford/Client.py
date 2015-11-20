from .Face import Face
from .Vision import Vision
from .Emotion import Emotion


class Client(object):
    """Client for using project oxford APIs"""

    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """

        if key and isinstance(key, str):
            self.key = key
        else:
            raise Exception('Key is required but a string was not provided')

        self._face = Face(key)
        self._vision = Vision(key)
        self._emotion = Emotion(key)

    @property
    def face(self):
        """The face API interface.
        Returns:
            :class:`face`. the face API instance.
        """
        return self._face

    @property
    def vision(self):
        """The vision API interface.
        Returns:
            :class:`vision`. the vision API instance.
        """
        return self._vision

    @property
    def emotion(self):
        """The emotion API interface.
        Returns:
            :class:`emotion`. the emotion API instance.
        """
        return self._emotion
