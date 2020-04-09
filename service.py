class Service:
	def __init__(self, service_json):
		self.name = service_json["name"]

		device = service_json["device"]
		if device is None:
			device = service_json["virtual_machine"]
		self.host = device["name"]
		self.post = service_json["port"]

		for k in service_json["custom_fields"].keys():
			self.__dict__[k] = service_json["custom_fields"][k]

