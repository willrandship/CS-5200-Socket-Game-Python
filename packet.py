import json
import logging

#gets a descendant to the root log
log = logging.getLogger("client.packet")

#generates a dict to convert to JSON on sending. Returns a python-style dictionary.
def login_dict(login):
	output = {
				"__type"		: "LoginRequest:#Messages.RequestMessages",
				"Identity"		: id_dict(identity),
				"ProcessLabel"	: PROCESS_LABEL_HERE,
				"ProcessType"	: PROCESS_TYPE_HERE
	}
	log.debug("Generated packet: " + json.dumps(output) )
	return output

#generates a dict to convert to JSON on sending. Returns a python-style dictionary.
def id_dict(id):
	output = {
				"ANumber"	: id.anumber,
				"Alias"		: id.alias,
				"FirstName"	: id.fname,
				"LastName"	: id.lname
	}
	log.debug("Generated packet: " + json.dumps(output) )
	return output

#Parse a received packet's data, returning based on the type of 
def parse(data):
	
	log.debug("Parsing: "+data)
	
	packet = json.loads(data)
	
	if(packet["__type"] == "LoginReply:#Messages.ReplyMessages"):
		if(packet["Success"]):
			log.info("Login succeeded")
		else:
			log.error("Login failed") 
	
