import socket
import logging
import json
import packet
import select

#set up the local logger (inherits from root)
log = logging.getLogger("client.network")

def connect(endpoint, timeout=5):
	
	#only ipv4 for now. Splits port from IP
	(address, port) = endpoint.split(":")
	port = eval(port)
	
	#create a socket with the specified address and port (takes a tuple)
	try:
		log.info("Connecting to "+address+" on port "+str(port))

		#Create a UDP Socket
		connection = socket.socket(
			socket.AF_INET,
			socket.SOCK_DGRAM
		)

		connection.settimeout(3)

	except ConnectionRefusedError:
		log.error("Connection refused")
		connection = None

	#returns the socket so you can send and receive data
	return connection, (address, port)

#Takes a properly formatted dict, sending the appropriate serialized data.
def send(session,data):
	out = bytes(json.dumps(data),'utf-8')
	try:
		log.debug("Sending " + str(out))
		session.socket.sendto(out, session.registry)
	except socket.error:
		log.error("Something socket-y-bad happened")

#Takes a properly formatted dict, sending the appropriate serialized data.
def send_game(session,data):
	out = bytes(json.dumps(data),'utf-8')
	try:
		log.debug("Sending (game) " + str(out))
		session.socket.sendto(
			out,
			(
				session.gamemgr["EndPoint"]["Host"],
				session.gamemgr["EndPoint"]["Port"]
			)
		)
	except socket.error:
		log.error("Something socket-y-bad happened")
 
#listen for data on the network. Also implicitly handles keep-alive.
#returns a message-format dict
def receive(session):
	data = None

	try:
		recvpacket = session.socket.recvfrom(4096)
		
		
		data = recvpacket[0].decode('utf-8')
		addr = recvpacket[1]
		
		log.debug("Packet Received:\n"+data)
	except socket.timeout:
		log.error("Receive Timeout")
		data = None
	except BlockingIOError:
		data = None
	if data != None: return packet.parse(data, addr, session)
