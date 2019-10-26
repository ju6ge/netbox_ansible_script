import inventory

from hosts import Host

def main():
	devices = inventory.get_device_data()
	vms = inventory.get_vm_data()
	ips = inventory.get_ip_data()

	for d in devices+vms:
		host = Host(d, ips)
		print(host.name, host.tags)
		if (len(host.interfaces) > 0):
			for i in host.interfaces:
				print("\t", i.name, i.ip, i.primary)


if __name__ == "__main__":
	main()
