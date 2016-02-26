#unittest.py - Run unit tests on various aspects of the client.

import unittest
import logging

log = logging.getLogger("test")

class TestPacketGeneration(unittest.TestCase):
	import packet
	
	id = {
	
	}
	
	def test_login_packet(self):
		import packet

		#comes with predefined values
		id = packet.ID()
		
		testcase = {
			"__type":"LoginRequest:#Messages.RequestMessages",
			"Identity":packet.id_packet(id),
			"ProcessLabel":"test",
			"ProcessType" :3
		}
		self.assertEqual(testcase,packet.login_request(id,plabel="test"))

class TestJsonDict(unittest.TestCase):

	#test that json and python dicts are equivalent
	def test_dict_json_equivalence(self):
		import json

		testdict = {
			"a":1,
			"b":2,
			"c":3,
			"sub": {"a":1}
		}
		for item in testdict:
			self.assertEqual(testdict[item],json.loads(json.dumps(testdict))[item])


class TestSocketCreation(unittest.TestCase):
	
	#create a local socket on an unused port
	def test_local_socket(self):
		import network

		try:
			a = network.create_socket()
			self.assertFalse(a == None) #Socket Creation Failed - Connection Refused
			b = network.create_socket()
			self.assertFalse(b == None)
			
			b.bind( ("0.0.0.0",25565) )
			a.sendto("Passed",("localhost",25565))
			data = b.recvfrom(4096)[0]
			
			log.debug("Packet test: "+ data)
			
			self.assertEqual(data,"Passed")
		except network.socket.error:
			self.assertTrue(False) #Socket creation failed - Exception Raised
		
		#close the socket - not part of the test
		try:
			a.close()
		except:
			pass

if __name__ == "__main__":
	unittest.main()
