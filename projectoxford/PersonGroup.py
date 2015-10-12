import time

from .Base import Base

_personGroupUrl = 'https://api.projectoxford.ai/face/v0/persongroups'


class PersonGroup(Base):
    """Client for using the Project Oxford person group APIs"""

    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """
        Base.__init__(self, key)

    def create(self, personGroupId, name, userData=None):
        """Creates a new person group with a user-specified ID.
        A person group is one of the most important parameters for the Identification API.
        The Identification searches person faces in a specified person group.

        Args:
            personGroupId (str). Numbers, en-us letters in lower case, '-', '_'. Max length: 64
            name (str). Person group display name. The maximum length is 128.
            userData (str). Optional user-provided data attached to the group. The size limit is 16KB.

        Returns:
            object. The resulting JSON
        """

        body = {
            'name': name,
            'userData': userData
        }

        return self._invoke('put',
                            _personGroupUrl + '/' + personGroupId,
                            json=body,
                            headers={'Ocp-Apim-Subscription-Key': self.key})

    def delete(self, personGroupId):
        """Deletes an existing person group.

        Args:
            personGroupId (str). Name of person group to delete

        Returns:
            object. The resulting JSON
        """

        return self._invoke('delete',
                            _personGroupUrl + '/' + personGroupId,
                            headers={'Ocp-Apim-Subscription-Key': self.key})

    def get(self, personGroupId):
        """Gets an existing person group.

        Args:
            personGroupId (str). Name of person group to get

        Returns:
            object. The resulting JSON
        """

        return self._invoke('get',
                            _personGroupUrl + '/' + personGroupId,
                            headers={'Ocp-Apim-Subscription-Key': self.key})

    def trainingStatus(self, personGroupId):
        """Retrieves the training status of a person group. Training is triggered by the Train PersonGroup API.
           The training will process for a while on the server side. This API can query whether the training
           is completed or ongoing.

        Args:
            personGroupId (str). Name of person group under training

        Returns:
            object. The resulting JSON
        """

        return self._invoke('get',
                            _personGroupUrl + '/' + personGroupId + '/training',
                            headers={'Ocp-Apim-Subscription-Key': self.key})

    def trainingStart(self, personGroupId):
        """Starts a person group training.
        Training is a necessary preparation process of a person group before identification.
        Each person group needs to be trained in order to call Identification. The training
        will process for a while on the server side even after this API has responded.

        Args:
            personGroupId (str). Name of person group to train

        Returns:
            object. The resulting JSON
        """

        return self._invoke('post',
                            _personGroupUrl + '/' + personGroupId + '/training',
                            headers={'Ocp-Apim-Subscription-Key': self.key})

    def update(self, personGroupId, name, userData=None):
        """Updates a person group with a user-specified ID.
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

        return self._invoke('patch',
                            _personGroupUrl + '/' + personGroupId,
                            json=body,
                            headers={'Ocp-Apim-Subscription-Key': self.key})

    def createOrUpdate(self, personGroupId, name, userData=None):
        """Creates or updates a person group with a user-specified ID.
        A person group is one of the most important parameters for the Identification API.
        The Identification searches person faces in a specified person group.

        Args:
            personGroupId (str). Numbers, en-us letters in lower case, '-', '_'. Max length: 64
            name (str). Person group display name. The maximum length is 128.
            userData (str). User-provided data attached to the group. The size limit is 16KB.

        Returns:
            object. The resulting JSON
        """
        if self.get(personGroupId) is None:
            return self.create(personGroupId, name, userData)
        else:
            return self.update(personGroupId, name, userData)

    def trainAndPollForCompletion(self, personGroupId, timeoutSeconds=30):
        """Starts a person group training and polls until the status is not 'running'

        Args:
            personGroupId (str). Name of person group to train

        Returns:
            object. The resulting JSON
        """
        timeout = 0
        status = self.trainingStart(personGroupId)
        while status['status'] == 'running':
            time.sleep(1)
            status = self.trainingStatus(personGroupId)
            timeout += 1

            if timeout >= timeoutSeconds:
                raise Exception('training timed out after {0} seconds, last known status: {1}'.format(timeoutSeconds, status))

        return status

    def list(self):
        """Lists all person groups in the current subscription.

        Returns:
            object. The resulting JSON
        """
        return self._invoke('get', _personGroupUrl, headers={'Ocp-Apim-Subscription-Key': self.key})
