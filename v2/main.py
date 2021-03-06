import client
import argparse
import sys
import logging
import network

#set up the base logger (This is the root logger)
log = logging.getLogger()
handler = logging.StreamHandler()
log.addHandler(handler)

#Set the "usage" name to match the script name as called.
parser = argparse.ArgumentParser(sys.argv[0])

#set up the arguments to log.
parser.add_argument(
	"-e", "--endpoint",
	dest='endpoint',action='store',
	default='52.3.213.61:12000',
	help='Define the endpoint to use (default: AWS registry IP)'
)

parser.add_argument(
	"-f", "--first",
	dest='fname',action='store',
	default='William',
	help='Set your first name (default: William)'
)

parser.add_argument(
	"-l", "--last",
	dest='lname',action='store',
	default='Shipley',
	help='Set your last name (default: Shipley)'
)

parser.add_argument(
	"-n", "--anumber",
	dest='anumber',action='store',
	default='A01514559',
	help='Set your A Number (default: A01514559)'
)

parser.add_argument(
	"-a", "--alias",
	dest='alias',action='store',
	default='Will',
	help='Set your alias (default: Will)'
)

parser.add_argument(
	"-v", "--verbose",
	dest='debug',action='store_true',
	help='Output debugging information'
)

args = parser.parse_args()

#set log level
if args.debug:
	log.setLevel(logging.DEBUG)
	handler.setLevel(logging.DEBUG)
else:
	log.setLevel(logging.INFO)
	handler.setLevel(logging.INFO)


log.debug("Parsed input arguments")

log.info(
"""
Logging in as:

{0} {1} ({2}, {3})

on

{4}
""".format(
		args.fname,
		args.lname,
		args.anumber,
		args.alias,
		args.endpoint
	)
)

#start up a session
session = client.login(
	args.fname,
	args.lname,
	args.anumber,
	args.alias,
	args.endpoint
)


while(session.gamemgr == None):
	log.info("Requesting Game List")

	#get the game list
	session, games = client.game_list(session)

	if(games != None):
		log.info("Game List Received")
		log.debug(str(games))
		
		#try joining some games
		for game in games:
			log.info("Joining game: "+game["Label"])
			session = client.join_game(session,game)
			if session.gamemgr != None: break

log.info("Successfully joined game.")

#Nothing left to do - in a game. Just check for keepalive packets
while(1):
	network.receive(session)
