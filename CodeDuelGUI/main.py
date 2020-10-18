
"""
@author:  Efe Osman ASLANOĞLU (PyroSoft) ,  Emircan DEMİRCİ(Venoox)
@date: 8.10.2020
"""
import json
from homescreen import*
from loginform import*
from connection import*

@LoginForm.bind(name = "login")
def login(email,password):
    values = {"email": email, "password": password}
    return conn.send(bytes(json.dumps({"command": "login", "values":values}), 'utf-8'))

@LoginForm.bind(name = "register")
def register(username,email,password):
    values = {"username": username, "email": email, "password": password}
    return conn.send(bytes(json.dumps({"command": "register", "values": values}), 'utf-8'))

class Main():
    def __init__(self, conn):
        # Initialize variables
        self.conn = conn
        # Initialize GUI Forms
        self.loginform = LoginForm()
        self.homescreen = HomeScreen()
        
    def start(self):
        self.loginform.show()
        if self.loginform.get_state():
            self.loginform.close()
            self.homescreen.show()


        
    

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    conn = Connection().start() # Send Connecion request to the server
    next(conn) # start generator for yield assigment.
    
    main = Main(conn)
    main.start()
    sys.exit(app.exec_())
