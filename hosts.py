
class Host:
	def __init__(self, host_data = None, ip_data=None):
		if not host_data is None:
			_readin_host_data(host_data)
		if not ip_data in  None:
			_readin_ip_data(ip_data)

	def _readin_host_data(self, data):
		pass

	def _readin_ip_data(self, data):
		pass
