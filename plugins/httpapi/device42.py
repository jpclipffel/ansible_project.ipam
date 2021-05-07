import json

from ansible.errors import AnsibleConnectionFailure
from ansible.plugins.httpapi import HttpApiBase


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


class HttpApi(HttpApiBase):
    """Ansible's HTTPAPI plugin for Device42 API.

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
            # Normalize path
            path = f'/{path.strip("/")}/'
            method = method.upper()
            # Forge query parameters
            if method in ['GET',]:
                params = '&'.join([f'{k}={v}' for k, v in data.items()])
                path = f'{path}?{params}'
                data = json.dumps(data)
            elif method in ['POST',]:
                data = '&'.join([f'{k}={v}' for k, v in data.items()])
            # Forge and send request
            response, response_data = self.connection.send(
                path,
                data,
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
        # Raised when Ansible failed to connect to Device42
        except AnsibleConnectionFailure as error:
            raise Exception(f'Connection error: {str(error)}')
        # Unknown error
        except Exception as error:
            raise Exception(f'Error: {str(error)}')
