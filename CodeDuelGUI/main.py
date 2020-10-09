"""
@author:  Efe Osman ASLANOĞLU (PyroSoft) ,  Emircan DEMİRCİ(Venoox)
@date: 8.10.2020
"""
from homescreenn import*
from loginregister import*
from connection import*

class Main():
    def __init__(self):
        # Send Connecion request to the server
        self.connect()
        # Initialize GUI Forms
        self.loginregister = LoginForm()

        self.homescreen = HomeScreen()
        
    def start(self):
        self.loginregister.show()
        
        self.homescreen.show()
        
    def connect(self):
        pass
    
    @LoginForm.command(name = "login")
    def login(self,username,email,password):
        pass
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main = Main()
    main.start()
    
    sys.exit(app.exec_())
