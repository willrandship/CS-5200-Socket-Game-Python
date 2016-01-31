#builtins
import json
import logging
import socket


#local imports
import packet
import network

class Session:
	id = packet.ID()
	socket = None
	login = False
	gamelogin = False
	procinfo = None

#Log into the main server. Returns a player session that has not
#connected to any games yet.
def login(fname, lname, anumber, alias, endpoint):
	
	id = packet.ID()

	id.fname = fname
	id.lname = lname
	id.alias = alias
	id.anumber = anumber
	
	session = Session()
	
	session.id = id
	while session.socket == None:
		session.socket = network.connect(endpoint)
	network.send( session, packet.login_request(session.id) )
	
	#While we're still waiting on a login reply, keep listening
	status = 0
	while(session.login == False):
		data = network.receive(session)
		if data==None: continue

		if(packet["__type"] == "LoginReply:#Messages.ReplyMessages"):
			if(packet["Success"]):
				log.info("Login succeeded")
				session.procinfo = packet["ProcessInfo"]
				session.login = True
			else:
				log.error("Login failed")
				log.error("Error message was: "+ packet["Note"])
				return session
		else:
			log.warning("Unexpected packet received: " + str(data) )

	return session

#returns a list of games
def game_list(session):
	network.send( session, packet.gamelist_request())
	while(1):
		a = network.receive( session )
		if a==None: continue

		if a["__type"] ==  "GameListReply:#Messages.ReplyMessages":
			return a["GameInfo"]
		else:
			log.warning("Unexpected packet received: " + str(data) )

#Join a game. Returns the modified session. (Fail -> gamesock == None)
def join_game(session, game):
	gamesock = network.connect(
		game["GameManager"]["Endpoint"]["Host"] +
		str(game["GameManager"]["Endpoint"]["Port"])
	)
	
	if gamesock==None:
		log.debug("Failed to connect to game: " + game["GameId"])
		return session
	
	session.gamesock = gamesock
	
	network.send_game(session, packet.joingame_request(game, session))
	
	while session.gamelogin == False:
		data = network.receive_game(session)
		if data==None: continue

		if(packet["__type"] == "JoinGameReply:#Messages.ReplyMessages"):
			if(packet["Success"]):
				log.info("Login succeeded")
				session.gamelogin = True
			else:
				log.error("Login failed")
				log.error("Error message was: "+ packet["Note"])
				return session
		else:
			log.warning("Unexpected packet received: " + str(data) )

	return session
