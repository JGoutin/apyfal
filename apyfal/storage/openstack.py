# coding=utf-8
"""OpenStack Swift"""

from apyfal.storage import _Storage


class SwiftStorage(_Storage):
    """OpenStack Swift Object _Storage

    Storage URL:
        - "https://Domain/v1/ProjectID/Container/Object"
        - "swift://Container/Object"

    Args:
        storage_type (str): Cloud service provider name. Default to "OpenStack".
        config (str or apyfal.configuration.Configuration or file-like object):
            Can be Configuration instance, apyfal.storage URL, paths, file-like
            object.
            If not set, will search it in current working directory, in current
            user "home" folder. If none found, will use default configuration
            values.
        client_id (str): OpenStack Access Key ID.
        secret_id (str): OpenStack Secret Access Key.
        region (str): OpenStack region.
        project_id (str): OpenStack Project
        auth_url (str): OpenStack auth-URL
        interface (str): OpenStack interface
    """
    #: Provider name
    NAME = 'OpenStack'

    #: Storage name
    STORAGE_NAME = 'swift'

    # Default OpenStack auth-URL to use (str)
    OPENSTACK_AUTH_URL = None

    # Default Interface to use (str)
    OPENSTACK_INTERFACE = None

    #: Extra URL prefix (For shorter URL)
    EXTRA_URL_PREFIX = 'swift://'

    #: Storage parameters template
    STORAGE_PARAMETERS = {
            'authurl': 'self._auth_url',
            'user': 'self._client_id',
            'key': 'self._secret_id',
            'auth_version': '3',
            'os_options': {
                'region_name': 'self._region',
                'project_id': 'self._project_id'}}

    def __init__(self, region=None, project_id=None, auth_url=None,
                 interface=None, **kwargs):
        _Storage.__init__(self, **kwargs)

        # Read configuration
        self._region = self._from_config('region', region)
        self._project_id = self._from_config('project_id', project_id)
        self._auth_url = (
            self._from_config('auth_url', auth_url) or
            self.OPENSTACK_AUTH_URL)
        self._interface = (
            self._from_config('interface', interface) or
            self.OPENSTACK_INTERFACE)
