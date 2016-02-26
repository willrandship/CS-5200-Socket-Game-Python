#builtins
import json
import logging
import socket
import time

#local imports
import packet
import network

log = logging.getLogger("client")

class Session:
	id = packet.ID()
	socket = None
	registry = None
	gamemgr = None
	login = False
	gamelogin = False
	procinfo = None

#Log into the main server. Returns a player session that has not
#connected to any games yet.
def login(fname, lname, anumber, alias, endpoint, label=None):
	
	if label==None: label=alias
	
	id = packet.ID()

	id.fname = fname
	id.lname = lname
	id.alias = alias
	id.anumber = anumber
	
	session = Session()
	
	#only ipv4 for now. Splits port from IP
	(address, port) = endpoint.split(":")
	port = eval(port)
	
	session.registry = (address,port)
	
	session.id = id
	while session.socket == None:
		session.socket = network.create_socket()
	
	log.info("Logging in")
	
	#While we're still waiting on a login reply, keep listening
	status = 0
	while(session.login == False):
		network.send( session, packet.login_request(session.id, label) )
		time.sleep(1)
		data = network.receive(session)
		if data==None: continue

		if(data["__type"] == "LoginReply:#Messages.ReplyMessages"):
			if(data["Success"]):
				log.info("Login succeeded")
				session.procinfo = data["ProcessInfo"]
				session.login = True
			else:
				log.error("Login failed")
				log.error("Error message was: "+ data["Note"])
				return session
		else:
			log.warning("Unexpected packet received: " + str(data) )

	return session

#returns a list of games
def game_list(session):
	while(1):
		network.send( session, packet.gamelist_request())
		time.sleep(1)
		a = network.receive( session )
		if a==None: continue

		if a["__type"] ==  "GameListReply:#Messages.ReplyMessages":
			return session, a["GameInfo"]
		else:
			log.warning("Unexpected packet received: " + str(a) )
			return session, None

#Join a game. Returns the modified session. (Fail -> gamesock == None)
def join_game(session, game):
	
	session.gamemgr = game["GameManager"]
	
	while session.gamelogin == False:
		#Keep trying to join game until it works
		network.send_game(session, packet.joingame_request(game))
		time.sleep(1)
		data = network.receive(session)
		if data==None: continue

		if(data["__type"] == "JoinGameReply:#Messages.ReplyMessages"):
			if(data["Success"]):
				log.info("Login succeeded")
				session.gamelogin = True
			else:
				log.error("Login failed")
				log.error("Error message was: "+ data["Note"])
				return session
		else:
			log.warning("Unexpected packet received: " + str(data) )

	return session
