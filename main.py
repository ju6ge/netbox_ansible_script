#!/bin/python3
import inventory
import json

from ipaddress import IPv4Interface
from ipaddress import IPv6Interface

from hosts import Host
from service import Service

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
	services = inventory.get_service_data()


	ansible_inventory = {}
	ansible_inventory["_meta"] = {}

	hosts = {}

	groups = {}

	for d in devices+vms:
		host = Host(d, ips)
		hosts[host.name] = host
		role = host.hostrole
		if role not in groups.keys():
			groups[role] = {}
			groups[role]["hosts"] = []
			groups[role]["vars"] = {}
			groups[role]["children"] = []
		groups[role]["hosts"].append(host.name)
		tags = host.tags
		for tag in tags:
			tagstr = "tags_" + str(tag)
			if tagstr not in groups.keys():
				groups[tagstr] = {}
				groups[tagstr]["hosts"] = []
				groups[tagstr]["vars"] = {}
				groups[tagstr]["children"] = []
			groups[tagstr]["hosts"].append(host.name)

	for role in groups.keys():
		ansible_inventory[role] = groups[role]

	for s in services:
		serv = Service(s)
		host = hosts[serv.host]

		if host.services is None:
			host._data["services"] = []

		host._data["services"].append(serv)



	ansible_inventory["_meta"]["hostvars"] = hosts
	print(json.dumps(ansible_inventory, default=serialize))


if __name__ == "__main__":
	main()
