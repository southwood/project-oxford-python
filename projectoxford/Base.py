import time
import requests

retryCount = 3

class Base(object):
    """The base class for oxford API clients"""

    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """
        if key and isinstance(key, str):
            self.key = key
        else:
            raise Exception('Key is required but a string was not provided')

    def _invoke(self, invocation, retries=0):
        """Attempt to invoke the a call to oxford. If the call is trottled, retry.
        Args:
            invocation (lambda). The oxford call to issue, should return an http response
            retries (int). The number of times this call has been retried.
        """
        response = invocation()
        if response.status_code == 429: # throttling response code
            if retries <= retryCount:
                delay = int(response.headers['retry-after'])
                time.sleep(delay)
                return Base._invoke(self, invocation, retries + 1)
            else:
                raise Exception('retry count ({0}) exceeded: {1}'.format(str(retryCount), response.text))
        elif response.status_code == 200 or response.status_code == 201:
            result = response # return the raw response if an unexpected content type is returned
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
            
            return result
        elif response.status_code == 404:
            return None
        else:
            raise Exception('status {0}: {1}'.format(str(response.status_code), response.text))

    def _postWithOptions(self, url, options, params={}):
        """Common options handler for vision / face detection

        Args:
            options (Object). The Options object describing features to extract
            options.url (string). The Url to image to be analyzed
            options.path (string). The Path to image to be analyzed
            options.stream (string). The image stream to be analyzed
            params (Object). The url parameters object

        Returns:
            object. The resulting JSON
        """

        # common header
        headers = { 'Ocp-Apim-Subscription-Key': self.key }

        # detect faces in a URL
        if 'url' in options and options['url'] != '':
            headers['Content-Type'] = 'application/json'
            call = lambda: requests.post(url, json={'url': options['url']}, headers=headers, params=params)
        
        # detect faces from a local file
        elif 'path' in options and options['path'] != '':
            headers['Content-Type'] = 'application/octet-stream'
            with open(options['path'], 'rb') as file:
                data = file.read()
                call = lambda: requests.post(url, data=data, headers=headers, params=params)

        # detect faces in an octect stream
        elif 'stream' in options:
            headers['Content-Type'] = 'application/octet-stream'
            call = lambda: requests.post(url, data=options['stream'], headers=headers, params=params)

        # fail if the options didn't specify an image source
        if call is None:
            raise Exception('either url, path, or stream must be specified')

        return Base._invoke(self, call)