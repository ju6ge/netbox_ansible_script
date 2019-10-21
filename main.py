import inventory

from hosts import Host

def main():
	devices = inventory.get_device_data()
	vms = inventory.get_vm_data()
	ips = inventory.get_ip_data()

	for d in devices:
		host = Host(d, ips)
		print(host.id, host.name, host.tags)

if __name__ == "__main__":
	main()
