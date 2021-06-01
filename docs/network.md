# Network - Manage IPAM networks

The playbook `playbooks/network.yaml` creates a network on Infoblox and
register it on Device42.

## Setup

See [the general documentation](../README.md)

## Usage

### Tags

| Tag     | Description                |
|---------|----------------------------|
| `setup` | Create the request network |

### Variables

| Variable             | Type     | Description                                             |
|----------------------|----------|---------------------------------------------------------|
| `request_view`       | `string` | Infoblox view, e.g. `DT-internal`                       |
| `request_container`  | `string` | Container network's plateform ID, e.g. `49435400000001` |
| `request_network`    | `string` | New network range. e.g `172.27.253.128/25`              |
| `request_plateforme` | `string` | New network plateforme ID, e.g. `49435400000003`        |

### CLI example

```Bash
ansible-playbook playbooks/network.yaml
    -i <inventory> \
    -e '{\
        "request_view": "", \
        "request_container": "", \
        "request_network": "", \
        "request_plateforme": "", \

        "nios_username": "", \
        "nios_password"": "", \
        "d42_username": "", \
        "d42_password"": "", \
    }' \
    --tags 'setup'
```

### Variables example

You may use the following variables to test the playbook:

```JSON
{
    "request_view": "DT-internal",
    "request_container": "49435400000001",
    "request_network": "172.27.253.128/25",
    "request_plateforme": "49435400000003",
}
```
