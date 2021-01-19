#
###Updated by Emircan Demirci 08.10.2020
#
from PyQt5.QtWidgets import (QMessageBox,QApplication, QMainWindow, QToolTip, QPushButton,
                             QDesktopWidget, QMainWindow, QAction, qApp, QToolBar, QVBoxLayout,
                             QComboBox,QLabel,QLineEdit,QGridLayout,QMenuBar,QMenu,QStatusBar,
                             QTextEdit,QDialog,QFrame,QProgressBar , QStackedWidget , QWidget
                             )
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon,QFont,QPixmap,QPalette
from PyQt5.QtCore import QCoreApplication, Qt,QBasicTimer, QPoint
import sys

class LoginForm(QWidget):
    binds = {"login": None, "register": None}
    def __init__(self):
        super().__init__()

        self.mainwidget = QMainWindow(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.main_stackedWidget = QStackedWidget(self)
        self.main_stackedWidget.setGeometry(0,70,600,400)

        self.login_page = QWidget()
        self.main_stackedWidget.addWidget(self.login_page)

        self.register_page = QWidget()
        self.main_stackedWidget.addWidget(self.register_page)

        #main screen properties
        self.setFixedSize(600,400)
        self.setStyleSheet("background-color:rgb(35,35,35);")

        #functions
        self.center()
        self.login_screen()

        #main_code_label
        self.main_code_label = QLabel("Code" , self)
        self.main_code_label.setFont(QFont('Arial' , 30))
        self.main_code_label.setGeometry(205,0,150,60)
        self.main_code_label.setAlignment(Qt.AlignTop)
        self.main_code_label.setStyleSheet("color:red")

        #main_duel_label
        self.main_duel_label = QLabel("Duel" , self)
        self.main_duel_label.setFont(QFont('Firestarter' , 30))
        self.main_duel_label.setGeometry(300,0,150,60)
        self.main_duel_label.setAlignment(Qt.AlignTop)
        self.main_duel_label.setStyleSheet("color:orange")

        #######################################
        ##titlebar variables
        #######################################


        #closebox
        self.closebox = QPushButton("X" , self)
        self.closebox.setFlat(True)
        self.closebox.setGeometry(550,0,50,30)
        self.closebox.clicked.connect(self.closeboxEvent)
        self.closebox.setStyleSheet("background-color:red;color:white;")

        #minimizebox
        self.minimizebox = QPushButton("_" , self)
        self.minimizebox.setGeometry(500,0,50,30)
        self.minimizebox.setFlat(True)
        self.minimizebox.clicked.connect(self.minimizeboxEvent)
        self.minimizebox.setStyleSheet("background-color:gray;color:white;")

        self.oldPos = self.pos()
        
        # state: Logined?
        self.state = False
    # Get State: Logined?
    def get_state():
        return state
    #titlebar movement functions
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    #closebutton
    def closeboxEvent(self):
    	self.close()

    #minimizebutton
    def minimizeboxEvent(self):
    	self.showMinimized()

    
    #####################################
    ##server-side
    ####################################
    @classmethod
    def bind(cls,name):
        assert (name in cls.binds)

        def getFunc(func):
            cls.binds[name] = func
            return func
        return getFunc   

    #Login Database
    def loginDatabaseConn(self):
        if self.login_email_textbox.text() == "" or self.login_pass_textbox.text() == "":
            login_error_messagebox = QMessageBox()
            login_error_messagebox.setStyleSheet("background-color:dimgray;color:silver;")
            login_error_messagebox.setText("Please fill in all blanks")
            login_error_messagebox.setWindowTitle("Error")
            login_error_messagebox.setIcon(QMessageBox.Warning)
            login_error_messagebox.setWindowIcon(QIcon("Buttons/warning.png"))
            login_error_messagebox.exec_()
        else:
            email , passwd = self.login_email_textbox.text() , self.login_pass_textbox.text()
            command_result = self.binds["login"](email, passwd)
    
    #registerlabel
    def registerLabelClicked(self):
        #register_email_label
        self.register_email_label = QLabel("Email" , self.register_page)
        self.register_email_label.setGeometry(100,5,100,100)
        self.register_email_label.setFont(QFont('Arial',18))
        self.register_email_label.setStyleSheet('color:silver')
        self.register_email_label.setAlignment(Qt.AlignTop)

        #register_email_textbox
        self.register_email_text = QLineEdit(self.register_page)
        self.register_email_text.move(200,0)
        self.register_email_text.resize(300,30)
        self.register_email_text.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")

        #uslabel
        self.register_username_label = QLabel("Username",self.register_page)
        self.register_username_label.setFont(QFont('Arial' , 18))
        self.register_username_label.setGeometry(55,50,120,85)
        self.register_username_label.setStyleSheet("color:#BFBFBF;")

        #register_username_textbox
        self.register_username_textbox = QLineEdit(self.register_page)
        self.register_username_textbox.move(200,75)
        self.register_username_textbox.resize(300,30)
        self.register_username_textbox.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")

        #register_password_label
        self.register_password_label = QLabel("Password",self.register_page)
        self.register_password_label.setFont(QFont('Arial' , 18))
        self.register_password_label.setGeometry(55,125,120,85)
        self.register_password_label.setStyleSheet("color:#BFBFBF;")


        #login_pass_textbox
        self.register_pass_textbox = QLineEdit(self.register_page)
        self.register_pass_textbox.move(200,150)
        self.register_pass_textbox.resize(300,30)
        self.register_pass_textbox.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")
        self.register_pass_textbox.setEchoMode(QLineEdit.Password)

        #confirm text box label
        self.confirm_label = QLabel("Confirm" , self.register_page)
        self.confirm_label.setFont(QFont('Arial' , 18))
        self.confirm_label.setGeometry(70,200,120,70)
        self.confirm_label.setStyleSheet("color:#BFBFBF")

        #register password textbox
        self.register_confirm_pass_textbox = QLineEdit(self.register_page)
        self.register_confirm_pass_textbox.move(200,218)
        self.register_confirm_pass_textbox.resize(300,30)
        self.register_confirm_pass_textbox.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")
        self.register_confirm_pass_textbox.setEchoMode(QLineEdit.Password)

        #register button add variables to database
        self.registerbutton = QPushButton("Register" , self.register_page)
        self.registerbutton.setGeometry(250,265,100,30)
        self.registerbutton.setStyleSheet("background-color:silver;border-style:outset;border-width:2px;border-radius:15px;padding:6px;border-color:#264348;")
        self.registerbutton.clicked.connect(self.registerDB)

        #login linked button
        self.go_login_screen = QPushButton("L͟o͟g͟i͟n͟",self.register_page)
        self.go_login_screen.setGeometry(270,305,50,20)
        self.go_login_screen.setFlat(True)
        self.go_login_screen.clicked.connect(self.login_screen)
        self.go_login_screen.setFont(QFont('Arial' , 8))
        self.go_login_screen.setStyleSheet("background-color:gray;color:rgb(175,93,72)")


        self.main_stackedWidget.setCurrentIndex(1)#go to the register page
    
    def registerDB(self):
        if self.register_email_text.text() == "" or self.register_pass_textbox.text() == "" or self.confirm_textbox.text() == "" or self.register_username_textbox.text() == "":
            register_error_messagebox = QMessageBox()
            register_error_messagebox.setStyleSheet("background-color:dimgray;color:silver;")
            register_error_messagebox.setText("Please fill in all blanks")
            register_error_messagebox.setWindowTitle("Error")
            register_error_messagebox.setIcon(QMessageBox.Warning)
            register_error_messagebox.setWindowIcon(QIcon("Buttons/warning.png"))
            register_error_messagebox.exec_()
        elif self.login_pass_textbox1.text() != self.confirm_textbox.text():
            register_pass_error_messagebox = QMessageBox()
            register_pass_error_messagebox.setStyleSheet("background-color:dimgray;color:silver;")
            register_pass_error_messagebox.setText("Passwords do not match")
            register_pass_error_messagebox.setWindowTitle("Error")
            register_pass_error_messagebox.setIcon(QMessageBox.Warning)
            register_pass_error_messagebox.setWindowIcon(QIcon("Buttons/warning.png"))
            register_pass_error_messagebox.exec_()
        else:
            register_username_label, email, passwd = self.register_username_textbox.text() , self.register_email_text.text() , self.register_pass_textbox.text()
            command_result = self.binds["register"](register_username_label, email, passwd)
    def login_screen(self):
        #login email label
        self.login_email_label = QLabel("Email" , self.login_page)
        self.login_email_label.setFont(QFont('Arial' , 20))
        self.login_email_label.setGeometry(100,20,100,40)
        self.login_email_label.setStyleSheet("color:#BFBFBF;")

    
        # login email textbox
        self.login_email_textbox = QLineEdit(self.login_page)
        self.login_email_textbox.move(250,22)
        self.login_email_textbox.resize(300,30)
        self.login_email_textbox.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")

        #login_pass_textbox
        self.login_pass_textbox = QLineEdit(self.login_page)
        self.login_pass_textbox.move(250,130)
        self.login_pass_textbox.resize(300,30)
        self.login_pass_textbox.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")
        self.login_pass_textbox.setEchoMode(QLineEdit.Password)
        #login passwor label
        self.login_password_label = QLabel("Password",self.login_page)
        self.login_password_label.setFont(QFont('Arial' , 18))
        self.login_password_label.setGeometry(100,86,120,120)
        self.login_password_label.setStyleSheet("color:#BFBFBF;")

        #letsgo(login) button check informations
        self.letsgobutton = QPushButton("Lets Go" , self.login_page)
        self.letsgobutton.setGeometry(250,200,100,30)
        self.letsgobutton.setStyleSheet("background-color:silver;border-style:outset;border-width:2px;border-radius:15px;padding:6px;border-color:#264348;")
        self.letsgobutton.clicked.connect(self.loginDatabaseConn)


        #register linked label
        self.register_linked_label = QPushButton("R͟e͟g͟i͟s͟t͟e͟r͟",self.login_page)
        self.register_linked_label.setGeometry(270,255,50,20)
        self.register_linked_label.clicked.connect(self.registerLabelClicked)
        self.register_linked_label.setFlat(True)
        self.register_linked_label.setFont(QFont('Arial' , 8))
        self.register_linked_label.setStyleSheet("background-color:rgb(35,35,35);color:rgb(175,93,72)")

        self.main_stackedWidget.setCurrentIndex(0)#go to the login page
    
