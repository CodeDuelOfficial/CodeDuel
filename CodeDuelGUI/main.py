"""
@author:  Efe Osman ASLANOĞLU (PyroSoft) ,  Emircan DEMİRCİ(Venoox)
@date: 8.10.2020
"""
from homescreenn import*
from loginregister import*
from connection import*

@LoginForm.command(name = "login")
def login(username,email,password):
    pass

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
    main = Main(conn)
    main.start()
    
    sys.exit(app.exec_())
