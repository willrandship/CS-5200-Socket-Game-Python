import socket
import logging

log = logging.getLogger("client.network")

def connect(address,port, timeout=10):
	#create a socket with the specified address and port (takes a tuple)
	try: 
		connection = socket.create_connection( (address,port), timeout)
	except socket.timeout:
		log.error("Connection timed out")
 
	#returns the socket so you can send and receive data
	return connection

#Takes a properly formatted dict, sending the appropriate serialized data.
def send(connection,packet):
	out = json.dumps(packet)
	try:
		connection.send(out)
	except socket.error:
		log.error("Something socket-y-bad happened")
 
