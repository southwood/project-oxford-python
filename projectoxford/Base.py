import time
import requests

retryCount = 5


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

    def _invoke(self, method, url, json=None, data=None, headers={}, params={}, retries=0):
        """Attempt to invoke the a call to oxford. If the call is trottled, retry.
        Args:
            :param method: method for the new :class:`Request` object.
            :param url: URL for the new :class:`Request` object.
            :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
            :param json: (optional) json data to send in the body of the :class:`Request`.
            :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
            :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
            :param retries: The number of times this call has been retried.
        """

        response = requests.request(method, url, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:  # throttling response code
            if retries <= retryCount:
                delay = int(response.headers['retry-after'])
                print('The projectoxford API was throttled. Retrying after {0} seconds'.format(str(delay)))
                time.sleep(delay)
                return self._invoke(method, url, json=json, data=data, headers=headers, params=params, retries=retries + 1)
            else:
                raise Exception('retry count ({0}) exceeded: {1}'.format(str(retryCount), response.text))
        elif response.status_code == 200 or response.status_code == 201:
            result = response  # return the raw response if an unexpected content type is returned
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
            url (string). The url to invoke in the Oxford API
            options (Object). The Options dictionary describing features to extract
            options.url (string). The Url to image to be analyzed
            options.path (string). The Path to image to be analyzed
            options.stream (string). The image stream to be analyzed
            params (Object). The url parameters dictionary

        Returns:
            object. The resulting JSON
        """

        # The types of data that can be passed to the API
        json = None
        data = None

        # common header
        headers = {'Ocp-Apim-Subscription-Key': self.key}

        # detect faces in a URL
        if 'url' in options and options['url'] != '':
            headers['Content-Type'] = 'application/json'
            json={'url': options['url']}

        # detect faces from a local file
        elif 'path' in options and options['path'] != '':
            headers['Content-Type'] = 'application/octet-stream'
            data_file = open(options['path'], 'rb')
            data = data_file.read()
            data_file.close()

        # detect faces in an octect stream
        elif 'stream' in options:
            headers['Content-Type'] = 'application/octet-stream'
            data = options['stream']

        # fail if the options didn't specify an image source
        if not json and not data:
            raise Exception('Data must be supplied as either JSON or a Binary image data.')

        return self._invoke('post', url, json=json, data=data, headers=headers, params=params)
