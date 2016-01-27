import json
import logging

#gets a descendant to the root log
log = logging.getLogger("client.packet")

#Identity structure
class id:
	anumber = None
	alias = "Lazy Player"
	fname = "Lazy"
	lname = "Player"

class game:
	id = 0
	

class player:
	

#generates a dict to convert to JSON on sending. Returns a python-style dictionary.
def login_request(id, plabel=None, pid=0):
	output = {
		"__type"		: "LoginRequest:#Messages.RequestMessages",
		"Identity"		: id_packet(id),
		"ProcessLabel"	: plabel,
		"ProcessType"	: pid
	}
	log.debug("Generated packet: " + json.dumps(output) )
	return output

#generates a dict to convert to JSON on sending.
def id_packet(id):
	output = {
		"ANumber"	: id.anumber,
		"Alias"		: id.alias,
		"FirstName"	: id.fname,
		"LastName"	: id.lname
	}
	log.debug("Generated packet: " + json.dumps(output) )
	return output

def alive_reply():
	out = {
		"__type":"Reply:#Messages.ReplyMessages",
		"Note":"Yes, I am, in fact, alive"
		"Success":True
	}
	log.debug("Generated packet: " + json.dumps(out) )
	return out

def gamelist_request():
	out = {
		"__type":"GameListRequest:#Messages.RequestMessages",
		"StatusFilter":4
	}
	log.debug("Generated packet: " + json.dumps(out) )
	return out

def joingame_request(game):
	out = {
		"__type":"JoinGameRequest:#Messages.RequestMessages",
		"GameId":game["id"],
		"Player":player_packet(game,label)
	}
	log.debug("Generated packet: " + json.dumps(out) )
	return out

#Generate the player packet for joining a game
def player_packet(game,label):
	out = {
		"PublicKey":null,
		"Draws":0,
		"EndPoint":
		"HasUmbrellaRaised":False,
		"NumberOfFilledBalloon":0,
		"NumberOfPennies":0,
		"NumberOfUnfilledBalloon":0,
		"NumberOfUnraisedUnbrellas":0,
		"ProcessId":
		"Status":
		"Type":
		"Wins":0
	}
	log.debug("Generated packet: " + json.dumps(out) )
	return out


#Parse a received packet's data, returning based on the type of 
def parse(data,connection):
	
	log.debug("Parsing: "+data)
	
	packet = json.loads(data)
	
	if(packet["__type"] == "LoginReply:#Messages.ReplyMessages"):
		if(packet["Success"]):
			log.info("Login succeeded")
			return packet
		else:
			log.error("Login failed")
			log.error("Error message was: "+ packet["Note"])
			return packet 
	
	elif( packet["__type"] == "AliveRequest:#Messages.RequestMessages" ):
		log.debug("Sending KeepAlive Reply")
		network.send(connection,alive_reply())
