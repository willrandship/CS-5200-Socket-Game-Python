#packet.py - Construct and deconstruct packets for network i/o

import json
import logging

#gets a descendant to the root log
log = logging.getLogger("client.packet")

#Identity structure
class ID:
	anumber = None
	alias = "Lazy Player"
	fname = "Lazy"
	lname = "Player"

#generates a dict to convert to JSON on sending. Returns a python-style dictionary.
def login_request(id, plabel=None):
	output = {
		"__type"		: "LoginRequest:#Messages.RequestMessages",
		"Identity"		: id_packet(id),
		"ProcessLabel"	: plabel,
		"ProcessType"	: 3
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
		"Note":"Yes, I am, in fact, alive",
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
		"GameId":game["GameId"],
		"Player":player_packet(game)
	}
	log.debug("Generated packet: " + json.dumps(out) )
	return out

#Generate the player packet for joining a game
def player_packet(game,label):
	out = {
		"PublicKey":null,
		"Draws":0,
		"EndPoint":{},
		"HasUmbrellaRaised":False,
		"NumberOfFilledBalloon":0,
		"NumberOfPennies":0,
		"NumberOfUnfilledBalloon":0,
		"NumberOfUnraisedUnbrellas":0,
		"ProcessId":0,
		"Status":0,
		"Type":0,
		"Wins":0
	}
	log.debug("Generated packet: " + json.dumps(out) )
	return out


#Parse a received packet's data into a dict
#Also implicitly handles keep-alive.
def parse(data,session):
	
	log.debug("Parsing: "+data)
	
	try:
		packet = json.loads(data)
	except json.decoder.JSONDecodeError:
		log.error("Bad JSON Packet: " + data)
		return None
	
	if( packet["__type"] == "AliveRequest:#Messages.RequestMessages" ):
		log.debug("Sending KeepAlive Reply")
		send(session,alive_reply())
	
	return packet
