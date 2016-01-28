import unittest

class TestPacketGeneration(unittest.TestCase):
	import packet
	
	id = {
	
	}
	
	def test_login(self):
		testcase = {
			"__type":"LoginRequest:#Messages.RequestMessages",
			"Identity":id_dict(self.id),
			"ProcessLabel":"test",
			"ProcessType" :0
		}
		self.assertEqual(testcase,login_request(

if __name__ == "__main__":
	unittest.main()
