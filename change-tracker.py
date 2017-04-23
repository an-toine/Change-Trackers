#!/usr/bin/python

#Quick and dirty script used to replace a tracker adress by another for a list of torrents on a Transmission server.
#Adapt the parameters in the main section to your installation of Transmission.

import httplib
import base64
import json

def getAuthorization(user,password):
	credentials = base64.b64encode(b"{}:{}".format(user,password)).decode("ascii")
	return { 'Authorization':'Basic {}'.format(credentials) }

def getToken(server,port,authorization):
	headers = authorization
 	connection = httplib.HTTPConnection(server,port)
	connection.request("GET","/transmission/rpc",headers=headers)
	response = connection.getresponse()
	return response.getheader("x-transmission-session-id")

if __name__ == '__main__':
	#Adapt these parameters for your configuration !
	SERVER = "127.0.0.1"
	PORT = 9091
	USER = "XXXX"
	PASSWORD = "XXXX"
	#The old tracker adress to replace
	OLD_TRACKER = "XXXX"
	#The new tracker to use
	NEW_TRACKER = "XXXX"
	authorization = getAuthorization(USER,PASSWORD)
	token = getToken(SERVER,PORT,authorization)
	headers = authorization
	headers['X-Transmission-Session-Id'] = '{}'.format(token)
	data = {}
	data["method"] = "torrent-get"
	data["arguments"] = {}
	data["arguments"]["fields"] = ["id","trackers"]
	encoded_data = json.dumps(data)
	connection = httplib.HTTPConnection(SERVER,PORT)
	connection.request("POST","/transmission/rpc",encoded_data,headers)
	response = connection.getresponse()
	decoded_response = json.load(response)
	for torrent in decoded_response['arguments']['torrents']:
		for tracker in torrent["trackers"]:
			if tracker["announce"] == OLD_TRACKER:
				print("For torrent {}, change tracker {}".format(torrent["id"],tracker["id"]))
				data = {}
				data["method"] = "torrent-set"
				data["arguments"] = {}
				data["arguments"]["id"] = torrent['id']
				data["arguments"]["trackerReplace"] = (tracker["id"],NEW_TRACKER)
				encoded_data = json.dumps(data)
				print(encoded_data)
				connection = httplib.HTTPConnection(SERVER,PORT)
				connection.request("POST","/transmission/rpc",encoded_data,headers)
				response = connection.getresponse()
				print(str(response.read()))
