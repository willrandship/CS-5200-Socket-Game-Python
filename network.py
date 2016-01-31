import socket
import logging
import json
import packet

#set up the local logger (inherits from root)
log = logging.getLogger("client.network")

def connect(endpoint, timeout=5):
	
	#only ipv4 for now. Splits port from IP
	(address, port) = endpoint.split(":")
	port = eval(port)
	
	#create a socket with the specified address and port (takes a tuple)
	try:
		log.info("Connecting to "+address+" on port "+str(port))
		connection = socket.create_connection( (address,port), timeout)
	except socket.timeout:
		connection = None
		log.error("Connection timed out")
	except ConnectionRefusedError:
		log.error("Connection refused")
		connection = None

	#returns the socket so you can send and receive data
	return connection

#Takes a properly formatted dict, sending the appropriate serialized data.
def send(session,data):
	out = bytes(json.dumps(data),'utf-8')
	try:
		log.debug("Sending " + str(out))
		session.socket.send(out)
	except socket.error:
		log.error("Something socket-y-bad happened")

#Takes a properly formatted dict, sending the appropriate serialized data.
def send_game(session,data):
	out = bytes(json.dumps(data),'utf-8')
	try:
		log.debug("Sending (game) " + str(out))
		session.gamesock.send(out)
	except socket.error:
		log.error("Something socket-y-bad happened")
 
#listen for data on the network. Also implicitly handles keep-alive.
#returns a message-format dict
def receive(session):
	
	try:
		data = session.socket.recv(4096).decode('utf-8')
		log.debug("Packet Received:\n"+data)
	except socket.timeout:
		log.error("Receive Timeout")
		data = None
	if data != None: return packet.parse(data,session)

#listen for data on the network. Also implicitly handles keep-alive.
#returns a message-format dict
def receive_game(session):
	try:
		data = str(session.gamesock.recv(4096))
		log.debug("Game Packet Received:\n"+data)
	except socket.timeout:
		log.error("Receive Timeout")
		data = None

	if data != None: return packet.parse(data,session)
