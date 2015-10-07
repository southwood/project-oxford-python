## Project Oxford for Python
[![Build Status](https://travis-ci.org/scsouthw/project-oxford-python.svg?branch=master)](https://travis-ci.org/scsouthw/project-oxford-python)
[![PyPI version](https://badge.fury.io/py/projectoxford.svg)](http://badge.fury.io/py/projectoxford)

This package contains a set of intelligent APIs understanding images: It can detect and analyze people's faces, their age, gender, and similarity. It can identify people based on a set of images. It can understand what is displayed in a picture and crop it according to where the important features are. It can tell you whether an image contains adult content, what the main colors are, and which of your images belong in a group. If your image features text, it will tell you the language and return the text as a string. It's basically magic. For more details on the Project Oxford API, please visit [projectoxford.ai](projectoxford.ai/demo/face#detection).

This python module implements all APIs available in the Face and Vision APIs of Project Oxford.

![](https://i.imgur.com/Zrsnhd3.jpg)

## Installation ##

To install the latest release you can use [pip](http://www.pip-installer.org/).

```
$ pip install projectoxford
```

## Usage ##

>**Note**: before you can send data to you will need an API key. There is are separate API keys for face and vision.

**Initialize a client**
```python
from projectoxford import Client
client = Client('<api_key>')
```

**Face detection**
```python
result = client.face.detect({'url': 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'})
print result['faceId']
print result['attributes']['age']
```

## Contributing
**Development environment**

* Install [python](https://www.python.org/downloads/), [pip](http://pip.readthedocs.org/en/stable/installing/), [Visual Studio](https://www.visualstudio.com/en-us/visual-studio-homepage-vs.aspx), [python tools for VS](https://www.visualstudio.com/en-us/features/python-vs.aspx)

* Get a [Project Oxford API key](https://www.projectoxford.ai/)

* Install dev dependencies
    
    ```
    pip install requests
    ```
* Set environment variable API key
    
    ```
    set OXFORD_API_KEY=<insert_your_key_here>
    ```
* Run tests
    
    ```
    python setup.py test
    ```
* Publishing
	- update version number in setup.py
	```
	git tag <version number> -m "update tag version"
	git push --tags origin master
	python setup.py register -r pypi
	python setup.py sdist upload
	```

## License
Licensed as MIT - please see LICENSE for details.
