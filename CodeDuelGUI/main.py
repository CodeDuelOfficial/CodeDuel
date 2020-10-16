
"""
@author:  Efe Osman ASLANOĞLU (PyroSoft) ,  Emircan DEMİRCİ(Venoox)
@date: 8.10.2020
"""
import json
from homescreenn import*
from loginregister import*
from connection import*

@LoginForm.bind(name = "login")
def login(email,password):
    values = {"email": email, "password": password}
    return conn.send(json.dumps({"command": "login", "values":values}))

@LoginForm.bind(name = "register")
def register(username,email,password):
    values = {"username": username, "email": email, "password": password}
    return conn.send(json.dumps({"command": "register", "values": values}))

class Main():
    def __init__(self, conn):
        # Initialize variables
        self.conn = conn
        # Initialize GUI Forms
        self.loginregister = LoginForm()
        self.homescreen = HomeScreen()
        
    def start(self):
        self.loginregister.show()
        self.homescreen.show()
        
    

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    conn = Connection().start() # Send Connecion request to the server
    next(conn) # start generator for yield assigment.
    
    main = Main(conn)
    main.start()
    sys.exit(app.exec_())
