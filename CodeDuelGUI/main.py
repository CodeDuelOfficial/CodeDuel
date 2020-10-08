from homescreenn import*
from loginregister import*
from connection import*

class Main():
    def __init__(self):
        self.loginregister = LoginForm(app)
        self.loginregister.show()

    def connect(self):
        self.conn = Connection(socket.gethostname(), 8080 , 'utf-8')
        self.connloop = self.conn.start()
        self.connloop.send()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())