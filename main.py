import inventory
import json

from ipaddress import IPv4Interface
from ipaddress import IPv6Interface

from hosts import Host

def serialize(obj):
	if isinstance(obj, Host):
		return obj.__dict__["_data"]
	if isinstance(obj, IPv4Interface):
		return str(obj)
	if isinstance(obj, IPv6Interface):
		return str(obj)
	return obj.__dict__

def main():
	devices = inventory.get_device_data()
	vms = inventory.get_vm_data()
	ips = inventory.get_ip_data()

	hosts = {}

	for d in devices+vms:
		host = Host(d, ips)
		hosts[host.name] = host
	print(json.dumps(hosts, default=serialize))


if __name__ == "__main__":
	main()
