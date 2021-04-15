# IPAM

Ansible project for IPAM automation.

This project includes several Ansible playbooks, custom module and plugin:

| Component                     | Kind           | Description                                      |
|-------------------------------|----------------|--------------------------------------------------|
| `playbooks/create-ip.yaml`    | Playbook       | Register one or more IP on Infoblox and Device42 |
| `playbooks/notify-mail.yaml`  | Playbook       | Notify the caller user by mail                   |
| `library/device42_api.py`     | Module         | Low-level interface to Device42 REST API         |
| `plugins/httpapi/device42.py` | HTTPAPI plugin | Connection plugin for Device42 REST API          |

## Requirements

* This project requires the Python package `infoblox-client` [\[1\]][1]
    * On AWX or Ansible tower, add a new custom virtual environement as follow:
        ```YAML
        custom_venvs:
        - name: ipam
            python: python3
            python_ansible_version: 3.0.0
            python_modules:
            - infoblox-client
        ```
    * Otherwise, install the package `infoblox-client` BOTH on the host system
      and in the same virtual environment as Ansible*:
        ```Bash
        pip install 'infoblox-client'
        ```

\* The module needs to be installed on both the virtual environment and host's
Python path due to a bug in the `nios_*` plugins: the plugins attempt to load
their connector from host's Python path instead of the Ansible Python path:
* https://community.infoblox.com/t5/API-Integration/Issues-with-infoblox-client-in-Ansible/td-p/16300
* https://github.com/ansible/ansible/issues/50881

## Setup

### Inventory

Inventory example:

```YAML
all:
  children:
    # Infoblox nodes
    nios:
      hosts:
        ib_gridmaster:
          nios_provider:
            # Required parameters
            host: ib-gridmaster.dt.ept.lu
            username: "{{ nios_user | default(lookup('env', 'INFOBLOX_USERNAME')) }}"
            password: "{{ nios_password | default(lookup('env', 'INFOBLOX_PASSWORD')) }}"
            # Optional parameters
            http_request_timeout: 60
    # Device42 API servers
    device42:
      vars:
          ansible_network_os: device42
          ansible_connection: httpapi
          ansible_httpapi_port: 443
          ansible_httpapi_use_ssl: yes
          ansible_httpapi_validate_certs: no
          ansible_user: "{{ d42_user }}"
          ansible_password: "{{ d42_password }}"
      hosts:
        "d42.dt.ept.lu":
```

## Tests

One can test the project by running the following playbooks:

| Playbook                       | Description               |
|--------------------------------|---------------------------|
| `playbooks/test-infoblox.yaml` | Test Infoblox integration |
| `playbooks/test-device42.yaml` | Test Device42 integration |

### Test Infoblox integartion

The following variables **must** be provided, e.g. with `-e {...}`:

| Variable name   | Description       |
|-----------------|-------------------|
| `nios_user`     | Infoblox username |
| `nios_password` | Infoblox password |

The following tags **may** be used, e.g. with `--tags '...'`:

| Tags                 | Description                                           |
|----------------------|-------------------------------------------------------|
| `lookup`, `lookups`  | Assert several `nios` lookup methods                  |
| `setup`              | Assert the creation of resources                      |
| `teardown`, `remove` | Assert the deletion of resources created with `setup` |

### Test Device42

The following variables **must** be provided, e.g. with `-e {...}`:

| Variable name   | Description       |
|-----------------|-------------------|
| `d42_user`      | Device42 username |
| `d42_password`  | Device42 password |

The following tags **may** be used, e.g. with `--tags '...'`:

| Tags                 | Description         |
|----------------------|---------------------|
| `get`                | Test `GET` requests |

---

[1]: https://docs.ansible.com/ansible/latest/scenario_guides/guide_infoblox.html#prerequisites
