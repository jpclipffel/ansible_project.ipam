# IP - Manage IPAM address(es)

The playbook `playbooks/ip.yaml` creates one or more IP address(es) on Infoblox
and register it/them on Device42.

## Setup

See [the general documentation](../README.md)

## Usage

### Tags

| Tag     | Description              |
|---------|--------------------------|
| `prepare` | Prepare the IP records (next IP(s) lookup, assertions, ...) |
| `setup` | Create the request IP(s) and register it/them |
| `debug` | Show debug information |
| `create` | Create records in Infoblox |
| `register` | Register records in Device42 |

When using the playbook, onw should use the following tags:

| Plateforme | Actions to perform                                   | Tags            | Skip tags         |
|------------|------------------------------------------------------|-----------------|-------------------|
| AWX        | Prepare the records **before** validation            | `preapre`       |                   |
| AWX        | Create and register the recrods **after** validation | `setup`         |                   |
| CLI        | Do everything at once                                | `prepare,setup` |                   |
| CLI        | Test without creating nor registering records        | `prepare,debug` | `create,register` |

### Variables

| Variable            | Type      | Description                                             |
|---------------------|-----------|---------------------------------------------------------|
| `request_view`      | `string`  | Infoblox view, e.g. `DT-internal`                       |
| `request_container` | `string`  | Container network's plateform ID, e.g. `49435400000001` |
| `request_network`   | `string`  | Network range, e.g `172.27.253.128/25`                  |
| `request_zone`      | `string`  | DNS zone, e.g. `dt.ept.lu`                              |
| `request_name`      | `string`  | Records name template, e.g. `server-{{ count }}`        |
| `request_count`     | `integer` | IP(s) count, e.g. `1`                                   |

### CLI example

```Bash
ansible-playbook playbooks/network.yaml
    -i <inventory> \
    -e '{\
        "request_view": "", \
        "request_container": "", \
        "request_network": "", \
        "request_zone": "", \
        "request_name": "", \
        "request_count": "", \

        "nios_username": "", \
        "nios_password"": "", \
        "d42_username": "", \
        "d42_password"": "", \
    }' \
    --tags 'setup'
```

## Example variables

You may use the following variables to test the playbook:

```JSON
{
    "request_view": "DT-internal",
    "request_container": "49435400000001",
    "request_network": "172.27.253.128/25",
    "request_zone": "dt.ept.lu",
    "request_name": "test-{{ count }}",
    "request_count": 4,
}
```
