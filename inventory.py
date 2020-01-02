import requests as r
import urllib
import json

import hosts
try:
    import creds
except ModuleNotFoundError:
    import creds_env as creds

def _get_auth_url(api_url, data=None):
	return r.get(api_url, headers={'Authorization': "Token %s" % creds.auth_token}, params=data)

def _do_req(path):
	api_url = urllib.parse.urljoin(creds.netbox_url, path)
	return _get_auth_url(api_url)

def _data_load(api_data):
	d = json.loads(api_data)

	data = d["results"]

	if not d["next"] is None:
		res = _get_auth_url(d["next"])
		data += _data_load(res.text)

	return data

devices = None
vms = None
ip_data = None
interface_data = None
role_data = None

def get_device_data(id=None):
	global devices

	if devices is None:
		res = _do_req("api/dcim/devices")
		devices = _data_load(res.text)

	if id is None:
		return devices
	else:
		for d in devices:
			if d["id"] == id:
				return d

def get_vm_data(id=None):
	global vms

	if vms is None:
		res = _do_req("api/virtualization/virtual-machines")
		vms = _data_load(res.text)

	if id is None:
		return vms
	else:
		for v in vms:
			if v["id"] == id:
				return v


def get_ip_data(id=None):
	global ip_data

	if ip_data is None:
		res = _do_req("api/ipam/ip-addresses")
		ip_data = _data_load(res.text)

	if id is None:
		return ip_data
	else:
		for i in ip_data:
			if i["id"] == id:
				return i


def get_interface_device_data():
	res = _do_req("api/dcim/interfaces")
	interface_data = _data_load(res.text)

	return interface_data

def get_interface_vm_data():
	res = _do_req("api/virtualization/interfaces")
	interface_data = _data_load(res.text)

	return interface_data

def get_interface_data(id=None):
	global interface_data

	if interface_data is None:
		interface_data = get_interface_device_data() + get_interface_vm_data()

	if id is None:
		return interface_data
	else:
		for i in interface_data:
			if i["id"] == id:
				return i

def get_role_data(id=None):
	global role_data

	if role_data is None:
		res = _do_req("api/dcim/device-roles")
		role_data = _data_load(res.text)

	if id is None:
		return role_data
	else:
		for i in role_data:
			if i["id"] == id:
				return i
