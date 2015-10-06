## Project Oxford for Python
[![Build Status](https://travis-ci.org/scsouthw/project-oxford-python.svg?branch=master)](https://travis-ci.org/scsouthw/project-oxford-python)

This package contains a set of intelligent APIs understanding images: It can detect and analyze people's faces, their age, gender, and similarity. It can identify people based on a set of images. It can understand what is displayed in a picture and crop it according to where the important features are. It can tell you whether an image contains adult content, what the main colors are, and which of your images belong in a group. If your image features text, it will tell you the language and return the text as a string. It's basically magic. For more details on the Project Oxford API, please visit [projectoxford.ai](projectoxford.ai/demo/face#detection).

This python module implements all APIs available in the Face and Vision APIs of Project Oxford.

![](https://i.imgur.com/Zrsnhd3.jpg)

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

## License
Licensed as MIT - please see LICENSE for details.
