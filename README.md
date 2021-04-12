# IPAM

Ansible project for IPAM automation.

## Installation & requirements

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

This project requires at least one inventory which targets `localhost` which
will contains the Infoblox configuration (as Infoblox is reached from the
Ansible controller).

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
            username: "{{ nios_user }}"
            password: "{{ nios_password }}"
            # Optional parameters
            http_request_timeout: 60
```

Compatible playbook example:

```YAML
- name: Tests - Lookups
  hosts: nios
  connection: local
  tasks:

  - name: Return the list of network views
    debug:
      msg: "{{ lookup('nios', 'networkview', provider=nios_provider) }}"
```

## Test

One can test the project by running the `playbooks/test.yaml` playbook.

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

Example to test everything at once:

```Bash
ansible-playbook projects/ipam/playbooks/test.yaml \
-i inventories/ipam-ict \
-e '{"nios_user": "foo", "nios_password": "***"}' \
--tags 'lookup,setup,teardown'
```

---

[1]: https://docs.ansible.com/ansible/latest/scenario_guides/guide_infoblox.html#prerequisites
