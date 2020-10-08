import json
import time
import socket


class Connection:
	"""Connection class for Client Connection"""
	def __init__(self, host, port, encode_format ):
		
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.host, self.port = host, port 
		self.conn.connect((self.host, self.port))

		self.encode_format = encode_format
		self.HEADER = 128

	def send(self, data):
		self.conn.send(bytes(data, self.encode_format))

	def recv(self, buffer):
		return json.loads(self.conn.recv(buffer).encode(self.encode_format))

	def start(self): # isim bulcam start olmasın ama ya

		while self.state:
			

			send_data = yield  # Get data from outside of function

			try:

				self.send(send_data) # Short-cut for self.conn.send()

				yield self.recv(self.HEADER)

			except socket.error:

				connected = False

				while (not connected):

					try:
						self.conn.connect((self.host, self.port))
					except:
						time.sleep(2) 
					else:
						connected = True







