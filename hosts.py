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
		self._data["interfaces"] = []
		self._data["hostrole"] = ""
		if "vmtype" in data["custom_fields"].keys():
			self._data["type"] = "virtual_machine"
		else:
			self._data["type"] = "device"
		for k in data.keys():
			self._data[k] = data[k]
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
						interface = Interface(inventory.get_ip_data(ip["id"]))

						if (interface.family == 4):
							if not self.primary_ip4 is None:
								if self.primary_ip4["address"] == str(interface.ip):
									interface.primary = True
						else:
							if not self.primary_ip6 is None:
								if self.primary_ip6["address"] == str(interface.ip):
									interface.primary = True

						self.interfaces.append(interface)

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
				to_print += "\t\t%s\t%s\t%s\n" % (i.name, i.ip, i.primary)
		to_print += "}"
		return to_print



class Interface:
	def __init__(self, ip_data):
		self.family = ip_data["family"]
		self.primary = False

		interface_data = inventory.get_interface_data(ip_data["interface"]["id"])
		self.name = interface_data["name"]

		if (self.family == 4):
			self.ip = ip.IPv4Interface(ip_data["address"])
		else:
			self.ip = ip.IPv6Interface(ip_data["address"])
		
