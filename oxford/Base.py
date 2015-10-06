import time

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
            return response.json() if response.content else None
        else:
            raise Exception('status {0}: {1}'.format(str(response.status_code), response.text))

        