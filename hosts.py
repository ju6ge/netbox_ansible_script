# This class will hold all the information needed to configure any host 

class Host:
	def __init__(self, host_data = None, ip_data=None):
		if not host_data is None:
			self._readin_host_data(host_data)
		if not ip_data is  None:
			self._readin_ip_data(ip_data)

	def _readin_host_data(self, data):
		self._data = {}
		self._data["interface"] = []
		for k in data.keys():
			self._data[k] = data[k]

	def _readin_ip_data(self, data):
		for ip in data:
			if not ip["interface"] is None:
				if not ip["interface"]["device"] is None:
					if ip["interface"]["device"]["id"] == self.id:
						self.interface.append(Interface(ip))

	def __getattr__(self, key):
		if key == "data":
			return self._data
		return self._data.get(key)



class Interface:
	def __init__(self, ip_data):
		self.family = ip_data["family"]
		self.addr_str = ip_data["addresses"]
		
