#
#	Created by Efe Osman Aslanoğlu (pyroman) on 2.7.20.
#

from hashlib import sha256
from pyisemail import is_email
import multiprocessing as Mp
import pymongo
import socket
import json
import re

class User(object):
	

	@classmethod
	def check_username(cls, username):

		check_expl = ""
		check_bool = None

		if not (2 < len(username) < 22):
			check_bool = False
			check_expl = "Username is too long/short"


		elif mongo_client["DuelDB"]["Users"].find({"username":username}):
			check_bool = False
			check_expl = "Username is too long/short"
			

		else:
			check_bool = True
	


		return ("USERNAME", check_bool, check_expl)

		
	@classmethod
	def check_email(cls, email):
		check_expl = ""
		check_bool = is_email(email, check_dns=True)

		if mongo_client["DuelDB"]["Users"].find({"email":email}):

			check_expl = "the email has been taken by someone else"
			check_bool = False

		return ("EMAIL", check_bool, check_expl)

	@classmethod
	def check_password(cls, password):
		"""

		1. min length is 8 and max length is 24
		2. at least include a digit number,
		3. at least a upcase and a lowcase letter

		"""

		check_expl = ""
		check_bool = None

		if   not (8 < len(password) < 24):
			check_bool = False 
			check_expl = "Password is too long/short!"


		elif not any((c.isdigit() for c in password)):
			check_bool = False 
			check_expl = "Password should have at least one numeral"


		elif not any((c.islower() for c in password)):
			check_bool = False 
			check_expl = "Password should have at least one lowercase letter"


		elif not any((c.isupper() for c in password)):
			check_bool = False 
			check_expl = "Password should have at least one uppercase letter"


		else:

			check_bool = True
		


		return ("PASSWORD", check_bool, check_expl)


	@classmethod
	def check_user(cls, user):

		# check all things in user values

		check_types = ("USERNAME", "EMAIL", "PASSWORD")
		check_funcs = (cls.check_username,cls.check_email, cls.check_password)
		check_map   = dict(zip(check_types,check_funcs))
		

		return {typ + "_" + "CHECK" : check_val for typ, *check_val in map(lambda t:  check_map[t](user[t.lower()]), check_types)}
		

		










class Server:

	clients = []

	def __init__(self, db_client):

		self.host = socket.gethostname()

		self.port = 8080

		self.encode_format = 'utf-8'

		self.HEADER = 64
		
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.s.bind((self.host, self.port))

		self.mongo_client = db_client

		self.database = self.mongo_client["DuelDB"]
	

						
	def procces_commands(self, conn, data):
		
		data_to_dict = json.loads(data)

		command, values = data_to_dict.values()

		if command == "LOGIN":

			user_query = {"email": values["email"], "hashed_password": sha256(values["password"].encode()).hexdigest()}

			find_account = self.database["Users"].find(user_query)

			if find_account:
				# TODO: burayı ilerde düzenle
				return {"LOGIN_PROCCES": True, "ACCOUNT": find_account}

			else:

				return {"LOGIN_PROCCES": True, "ACCOUNT": None}

		elif command == "REGISTER":

			check_result = User.check_user(values)


			if all(map(lambda x: x[0], check_result.values())):

				user = {"username": values["username"], "email": values["email"], "hashed_password": sha256(values["password"].encode()).hexdigest()}

				self.database["Users"].insert_one(user)

				return {"REGISTER_PROCCES":True, "DETAIL":check_result}

			else:
				# Send ERRORS about procces
				return {"REGISTER_PROCCES":False, "DETAIL":check_result}

		elif command == "INVITE":

			pass
		

	def handle_client(self, conn, addr):

		self.clients.append((conn, addr))


		connection = True
		
		while connection:

			data = conn.recv(self.HEADER).decode(self.encode_format)

			procces_result = self.procces_commands(conn, data)

			conn.send(json.dumps(procces_result).encode(self.encode_format))

			
			
		
	def start(self):

		self.state = True

		self.s.listen()

		
		while self.state:

			conn, addr = self.s.accept()

			P = Mp.Process(target = self.handle_client, args = (conn, addr))

			P.start()

			P.join()






if __name__ == '__main__':

	mongo_client = pymongo.MongoClient("")

	server = Server(db_client=mongo_client)
	
	server.start()


