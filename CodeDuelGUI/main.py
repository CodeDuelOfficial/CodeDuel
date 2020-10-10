
"""
@author:  Efe Osman ASLANOĞLU (PyroSoft) ,  Emircan DEMİRCİ(Venoox)
@date: 8.10.2020
"""

from homescreenn import*
from loginregister import*
from connection import*

@LoginForm.command(name = "login")
def login(email,password):
    return conn.send({"email": email, "password": password})

@LoginForm.command(name = "register")
def register(username,email,password):
    return conn.send({"username": username, "email": email, "password": password})

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
