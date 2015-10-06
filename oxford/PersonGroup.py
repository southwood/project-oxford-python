import json
import requests

_personGroupUrl = 'https://api.projectoxford.ai/face/v0/persongroups';

class PersonGroup(object):
    """Client for using the Project Oxford person group APIs"""
    
    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """

        if key and isinstance(key, str):
            self.key = key
        else:
            raise Exception('Key is required but a string was not provided')
        
    def _return(self, response):
        if response.status_code < 200 or response.status_code >= 400:
            raise Exception(str(response.status_code) + response.text)

        return response.json() if response.content else None

    def create(self, personGroupId, name, userData):
        """Creates a new person group with a user-specified ID.
        A person group is one of the most important parameters for the Identification API.
        The Identification searches person faces in a specified person group.

        Args:
            personGroupId (str). Numbers, en-us letters in lower case, '-', '_'. Max length: 64
            name (str). Person group display name. The maximum length is 128.
            userData (str). User-provided data attached to the group. The size limit is 16KB.

        Returns:
            object. The resulting JSON
        """

        body = {
            'name': name,
            'userData': userData
        }
    
        uri = _personGroupUrl + '/' + personGroupId
        result = requests.put(uri, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})
        return self._return(result)

    def delete(self, personGroupId):
        """Deletes an existing person group.

        Args:
            personGroupId (str). Name of person group to delete

        Returns:
            object. The resulting JSON
        """

        uri = _personGroupUrl + '/' + personGroupId
        result = requests.delete(uri, headers={'Ocp-Apim-Subscription-Key': self.key})
        return self._return(result)

    def get(self, personGroupId):
        """Gets an existing person group.

        Args:
            personGroupId (str). Name of person group to get

        Returns:
            object. The resulting JSON
        """

        uri = _personGroupUrl + '/' + personGroupId
        result = requests.get(uri, headers={'Ocp-Apim-Subscription-Key': self.key})
        return self._return(result)

    def trainingStatus(self, personGroupId):
        """Retrieves the training status of a person group. Training is triggered by the Train PersonGroup API.
           The training will process for a while on the server side. This API can query whether the training
           is completed or ongoing.

        Args:
            personGroupId (str). Name of person group to get

        Returns:
            object. The resulting JSON
        """

        uri = _personGroupUrl + '/' + personGroupId + '/training'
        result = requests.get(uri, headers={'Ocp-Apim-Subscription-Key': self.key})
        return self._return(result)

    def trainingStart(self, personGroupId):
        """Starts a person group training.
        Training is a necessary preparation process of a person group before identification.
        Each person group needs to be trained in order to call Identification. The training
        will process for a while on the server side even after this API has responded.

        Args:
            personGroupId (str). Name of person group to get

        Returns:
            object. The resulting JSON
        """

        uri = _personGroupUrl + '/' + personGroupId + '/training'
        result = requests.post(uri, headers={'Ocp-Apim-Subscription-Key': self.key})
        return self._return(result)

    def update(self, personGroupId, name, userData):
        """Updates a new person group with a user-specified ID.
        A person group is one of the most important parameters for the Identification API.
        The Identification searches person faces in a specified person group.

        Args:
            personGroupId (str). Numbers, en-us letters in lower case, '-', '_'. Max length: 64
            name (str). Person group display name. The maximum length is 128.
            userData (str). User-provided data attached to the group. The size limit is 16KB.

        Returns:
            object. The resulting JSON
        """

        body = {
            'name': name,
            'userData': userData
        }
    
        uri = _personGroupUrl + '/' + personGroupId
        result = requests.patch(uri, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})
        return self._return(result)

    def list(self):
        """Lists all person groups in the current subscription.
           
        Returns:
            object. The resulting JSON
        """

        result = requests.get(_personGroupUrl, headers={'Ocp-Apim-Subscription-Key': self.key})
        return self._return(result)