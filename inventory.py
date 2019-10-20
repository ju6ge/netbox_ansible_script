import requests as r
import urllib
import json

import hosts
import creds

def do_req(path):
	api_url = urllib.parse.urljoin(creds.netbox_url, path)
	return r.post(api_url, headers={'Authorization': "Token %s" % creds.auth_token})

def get_device_data():
	res = do_req("api/dcim/devices")

	api_data = json.loads(res.text)["results"]
	return api_data

def get_vm_data():
	res = do_req("api/virtualization/virtual-machines")

	api_data = json.loads(res.text)["results"]
	return api_data

def get_ip_data():
	res = do_req("api/ipam/ip-addresses")

	api_data = json.loads(res.text)["results"]
	return api_data
