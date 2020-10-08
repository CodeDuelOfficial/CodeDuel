from homescreenn import*
from loginregister import*


class Main():
    def __init__(self):
        self.loginregister = LoginForm(app)
        self.loginregister.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())