import json
import requests

_personGroupUrl = 'https://api.projectoxford.ai/face/v0/persongroups';

from .Base import Base

class PersonGroup(object):
    """Client for using the Project Oxford person group APIs"""
    
    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """
        Base.__init__(self, key)
        
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
        call = lambda: requests.put(uri, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})
        return Base._invoke(self, call)

    def delete(self, personGroupId):
        """Deletes an existing person group.

        Args:
            personGroupId (str). Name of person group to delete

        Returns:
            object. The resulting JSON
        """

        uri = _personGroupUrl + '/' + personGroupId
        call = lambda: requests.delete(uri, headers={'Ocp-Apim-Subscription-Key': self.key})
        return Base._invoke(self, call)

    def get(self, personGroupId):
        """Gets an existing person group.

        Args:
            personGroupId (str). Name of person group to get

        Returns:
            object. The resulting JSON
        """

        uri = _personGroupUrl + '/' + personGroupId
        call = lambda: requests.get(uri, headers={'Ocp-Apim-Subscription-Key': self.key})
        return Base._invoke(self, call)

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
        call = lambda: requests.get(uri, headers={'Ocp-Apim-Subscription-Key': self.key})
        return Base._invoke(self, call)

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
        call = lambda: requests.post(uri, headers={'Ocp-Apim-Subscription-Key': self.key})
        return Base._invoke(self, call)

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
        call = lambda: requests.patch(uri, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})
        return Base._invoke(self, call)

    def list(self):
        """Lists all person groups in the current subscription.
           
        Returns:
            object. The resulting JSON
        """

        call = lambda: requests.get(_personGroupUrl, headers={'Ocp-Apim-Subscription-Key': self.key})
        return Base._invoke(self, call)