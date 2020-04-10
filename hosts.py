# This class will hold all the information needed to configure any host

import ipaddress as ip
import inventory

class Host:
	def __init__(self, host_data = None, ip_data=None):
		if not host_data is None:
			self._readin_host_data(host_data)
		if not ip_data is  None:
			self._readin_ip_data(ip_data)

	def _readin_host_data(self, data):
		self._data = {}
		self._data["interfaces"] = {}
		self._data["hostrole"] = ""

		if data["primary_ip"]:
			self._data["ansible_host"] = str(ip.ip_interface(data["primary_ip"]["address"]).ip)
		#self._data["ansible_host"] = data["primary_ip"]["address"]

		if "vmtype" in data["custom_fields"].keys():
			self._data["type"] = "virtual_machine"
		else:
			self._data["type"] = "device"
		for k in data.keys():
			self._data[k] = data[k]

		if self.data["primary_ip"]:
			self._data["primary_ip"] = str(ip.ip_interface(data["primary_ip"]["address"]).ip)
		if self.data["primary_ip4"]:
			self._data["primary_ip4"] = str(ip.ip_interface(data["primary_ip4"]["address"]).ip)
		if self.data["primary_ip6"]:
			self._data["primary_ip6"] = str(ip.ip_interface(data["primary_ip6"]["address"]).ip)

		self._get_role()

	def _get_role(self):
		role_id = 0
		if self.type == "device":
			role_id = self.device_role["id"]
		else:
			role_id = self.role["id"]

		self._data["hostrole"] = inventory.get_role_data(role_id)["name"]

	def _readin_ip_data(self, data):
		for ip in data:
			if not ip["interface"] is None:
				if not ip["interface"][self.type] is None:
					if ip["interface"][self.type]["id"] == self.id:
						interface_name = ip["interface"]["name"]
						if not interface_name in self.interfaces.keys():
							self.interfaces[interface_name] = Interface(inventory.get_interface_data(ip["interface"]["id"]))
						ip_struct = IP(ip)

						if (ip_struct.family == 4):
							if not self.primary_ip4 is None:
								if self.primary_ip4 == str(ip_struct.ip.ip):
									ip_struct.primary = True
						else:
							if not self.primary_ip6 is None:
								if self.primary_ip6 == str(ip_struct.ip.ip):
									ip_struct.primary = True

						self.interfaces[interface_name].add_ip(ip_struct)

	def __getattr__(self, key):
		if key == "data":
			return self._data
		return self._data.get(key)

	def __str__(self):
		to_print = "{ Host %s\n" % self.name
		to_print += "\tType: %s \n" % self.type
		to_print += "\tTags: %s \n" % self.tags
		to_print += "\tRole: %s \n" % self.hostrole
		if (len(self.interfaces) > 0):
			to_print += "\tInterfaces:\n"
			for i in self.interfaces:
				to_print += "\t\t%s\t%s\t%s\n" % (i.name, i.ip.ip, i.primary)
		to_print += "}"
		return to_print



class IP:
	def __init__(self, ip_data):
		self.family = ip_data["family"]["value"]
		self.primary = False

		if (self.family == 4):
			self.ip = ip.IPv4Interface(ip_data["address"])
		elif (self.family == 6):
			self.ip = ip.IPv6Interface(ip_data["address"])
		
class Interface:
	def __init__(self, interface_data):
		self.name = interface_data["name"]
		self.enabled = interface_data["enabled"]
		if interface_data["mode"]:
			self.vlan_mode = interface_data["mode"]["label"]
		if interface_data["untagged_vlan"]:
			self.vlan_untagged_id = interface_data["untagged_vlan"]["vid"]
			self.vlan_untagged_name = interface_data["untagged_vlan"]["name"]
		if interface_data["tagged_vlans"]:
			self.vlans_tagged = [{"id": i["vid"], "name": i["name"]} for i in interface_data["tagged_vlans"]]
		

		if interface_data["mac_address"]:
			self.mac_address  = interface_data["mac_address"]
		self.netbox_id = interface_data["id"]

		self.ips = []

	def add_ip(self, ip):
		self.ips.append(ip)
