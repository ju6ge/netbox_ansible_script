Netbox to Ansible Script
========================

This is a simple script to pull all info from a netbox instance and export it to a json format that can be used from ansible.
Host will be grouped by role and all fields from netbox will be availible as hostvars, including all interfaces with corresponding
ips.

# Usage
1. Copy creds.py.template to creds.py and fill in token and netbox url.
2. Start ansible and specify `main.py` as the inventory file.
