from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


# Mpdule documentation
DOCUMENTATION = '''
---
author:
    - Jean-Philippe Clipffel (@jpclipffel)
httpapi : contrail
short_description: Httpapi Plugin for Juniper Contrail REST API
description:
  - This httpapi plugin provides methods to connect to Juniper Contrail via REST API
version_added: "3.0"
'''

import json
import base64

from ansible.errors import AnsibleConnectionFailure
from ansible.plugins.httpapi import HttpApiBase
from ansible.module_utils.basic import to_text
from ansible.module_utils.connection import ConnectionError
# pylint: disable = no-name-in-module, import-error
from ansible.module_utils.six.moves.urllib.error import HTTPError


class HttpApi(HttpApiBase):
    """Ansible's HTTPAPI interface for Device42 API.

    :ivar headers:  Default request headers
    """

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def __init__(self, connection):
        super(HttpApi, self).__init__(connection)

    def send_request(self, data: dict, path: str, method: str) -> dict:
        """Handles Device42 API requests and responses.

        :param data:        Request data
        :param path:        API path
        :param method:      HTTP method

        :return:    Tuple as `(status_code: int, content: dict)`
        """
        try:
            # Forge query parameters
            if method.lower() == 'get':
                params = '&'.join([f'{k}={v}' for k, v in data.items()])
                path = f'{path}?{params}'
            # Forge and send request
            response, response_data = self.connection.send(
                path,
                json.dumps(data),
                method=method,
                headers=self.headers
            )
            # Decode response and returns
            return response.getcode(), json.loads(response_data.getvalue())
        # Raised when `data` cannot be JSON-encoded
        except TypeError as error:
            raise Exception(f'Failed to encode Device42 request: {str(error)}')
        # Raised when Device42 response cannot be decoded to a `dict`
        except json.JSONDecodeError as error:
            raise Exception(f'Failed to decode Device42 response: {str(error)}: {response_data.getvalue()}')
        # Raised when a generic HTTP error occurs
        except HTTPError as error:
            raise Exception(f'HTTP error: {str(error)}')
        # Raised when Ansible failed to connect to Device42
        except AnsibleConnectionFailure as error:
            raise Exception(f'Connection error: {str(error)}')
        # Unknown error
        except Exception as error:
            raise Exception(f'Error: {str(error)}')
