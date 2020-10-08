from homescreenn import*
from loginregister import*
from connection import*

class Main():
    def __init__(self):
        # Send Connecion request to the server
        self.connect()
        # Initialize GUI Forms
        self.loginregister = LoginForm()
        
    def start(self):
        self.loginregister.show()
        
    def connect(self):
        self.conn = Connection(socket.gethostname(), 8080 , 'utf-8')
        self.connloop = self.conn.start()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main = Main()
    main.start()
    
    sys.exit(app.exec_())
