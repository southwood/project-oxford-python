Project Oxford for Python
=========================

This package contains a set of intelligent APIs understanding images: It can detect and analyze people's faces, their age, gender, and similarity. It can identify people based on a set of images. It can understand what is displayed in a picture and crop it according to where the important features are. It can tell you whether an image contains adult content, what the main colors are, and which of your images belong in a group. If your image features text, it will tell you the language and return the text as a string. It's basically magic. For more details on the Project Oxford API, please visit projectoxford.ai.

This python module implements all APIs available in the Face and Vision APIs of Project Oxford.

.. image:: https://i.imgur.com/Zrsnhd3.jpg

Installation
------------

To install the latest release you can use `pip <http://www.pip-installer.org/>`_.

::

    $ pip install projectoxford

Usage
-----
	
	**Note**: before you can send data to you will need an API key. There is are separate API keys for face and vision.

**Initialize a client**

.. code:: python

from projectoxford import Client
client = Client('<api_key>')

**Face detection**

.. code:: python

result = client.face.detect({'url': 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'})
print result['faceId']
print result['attributes']['age']


License
-------
Licensed as MIT - please see LICENSE.txt for details.
