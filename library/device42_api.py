ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = r'''
---
module: device42_api

short_description: Low-level interface to Device42 REST API

version_added: "3.0"

description:
    - "Low-level interface to Device42 REST API"

options:
    method:
        description:
            - HTTP method (e.g. 'GET', 'POST', etc.)
        required: true
        type: str
    path:
        description:
            - API path (defaults to API v1.0, e.g. '/api/1.0/<path>')
        required: true
        type: str
    data:
        description:
            - Request payload (will be merged in formData or query)
        required: false
        type: dict

author:
    - Jean-Philippe Clipffel (@jpclipffel)
'''

EXAMPLES = r'''
- name: Query resource
  device42_api:
    meth: GET
    path: devices
'''

RETURN = r'''
msg:
    description: Device42's response's 'msg' field
    type: str
    returned: always
code:
    description: Device42's response's 'code' field
    type: int
    returned: always
data:
    description: Device42's response
    type: complex
    returned: always
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection


def run_module():
    """Ansible module entry point.
    """
    # Modules arguments
    module_args = {
        'meth': {'type': str,  'required': True},
        'path': {'type': str,  'required': True},
        'data': {'type': dict, 'required': False, 'default': {}}
    }
    # Initializes module, connection and API helper
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
    connection = Connection(module._socket_path)
    # Run module
    module.exit_json(**{
        'msg': 'Done',
        'code': 0,
        'data': connection.send_request(
            data=module.params['data'],
            path=module.params['path'],
            method=module.params['meth']
        )
    })


def main():
    run_module()


if __name__ == '__main__':
    main()
