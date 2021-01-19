  
"""
@author: Efe Osman ASLANOĞLU (PyroSoft)
@date: 8.10.2020
"""
import time
import socket

class Connection:
	def __init__(self, host, port):
		# Client connection variables
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host, self.port = host, port 
		self.conn.connect((self.host, self.port))
		self.state = True
		# Constant variables
		self.HEADER = 128
	def _send(self, data):
		self.conn.sendall(data)

	def _recv(self, buffer):
		return self.conn.recv(buffer)

	def start(self):
		while self.state:
			try:
			
				send_data = yield  # Get data from outside of function.
				try:
					self._send(send_data) # Short-cut for self.conn.send.
					yield self._recv(self.HEADER)
				except socket.error:

					connected = False

					while (not connected):
						try:
							self.conn.connect((self.host, self.port))
						except:
							time.sleep(2) 
						else:
							connected = True
			except GeneratorExit:
				self.conn.close()
