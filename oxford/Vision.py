import re
import requests

_analyzeUrl = 'https://api.projectoxford.ai/vision/v1/analyses'
_thumbnailUrl = 'https://api.projectoxford.ai/vision/v1/thumbnails'
_ocrUrl = 'https://api.projectoxford.ai/vision/v1/ocr'

from .Base import Base

class Vision(Base):
    """Client for using the Project Oxford face APIs"""
    
    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """
        Base.__init__(self, key)

    def analyze(self, options):
        """This operation does a deep analysis on the given image and then extracts a
        set of rich visual features based on the image content.

        Args:
            options (Object). The Options object describing features to extract
            options.url (string). The Url to image to be analyzed
            options.path (string). The Path to image to be analyzed
            options.ImageType (boolean). The Detects if image is clipart or a line drawing.
            options.Color (boolean). The Determines the accent color, dominant color, if image is black&white.
            options.Faces (boolean). The Detects if faces are present. If present, generate coordinates, gender and age.
            options.Adult (boolean). The Detects if image is pornographic in nature (nudity or sex act). Sexually suggestive content is also detected.
            options.Categories (boolean). The Image categorization; taxonomy defined in documentation.

        Returns:
            object. The resulting JSON
        """
        
        flags = [];
        for option in options:
            match = re.match(r'(ImageType)|(Color)|(Faces)|(Adult)|(Categories)', option)
            if match and options[option]:
                flags.append(option)

        params = { 'visualFeatures': ','.join(flags) } if flags else {}
        return Base._postWithOptions(self, _analyzeUrl, options, params)