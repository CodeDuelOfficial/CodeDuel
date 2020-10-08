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
    def __init__(self):
        super().__init__()

        self.mwidget = QMainWindow(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


        self.stacked_widget3 = QStackedWidget(self)
        self.stacked_widget3.setGeometry(0,70,600,400)

        self.login_page = QWidget()
        self.stacked_widget3.addWidget(self.login_page)

        self.register_page = QWidget()
        self.stacked_widget3.addWidget(self.register_page)

        #size
        self.setFixedSize(600,400)
        self.center()
        self.logButtonClicked()
        self.setStyleSheet("background-color:rgb(35,35,35);")


        #label1
        self.label1 = QLabel("Code" , self)
        self.label1.setFont(QFont('Firestarter' , 30))
        self.label1.setGeometry(205,0,150,60)
        self.label1.setAlignment(Qt.AlignTop)
        self.label1.setStyleSheet("color:red")

        #duelLabel
        self.duelLabel = QLabel("Duel" , self)
        self.duelLabel.setFont(QFont('Firestarter' , 30))
        self.duelLabel.setGeometry(300,0,150,60)
        self.duelLabel.setAlignment(Qt.AlignTop)
        self.duelLabel.setStyleSheet("color:orange")

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



    #center
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



        
    #letsgobuttondb
    def letsgoDB(self):
        if self.ustextbox.text() == "" or self.passtextbox.text() == "":
            letsgoerror = QMessageBox()
            letsgoerror.setStyleSheet("background-color:dimgray;color:silver;")
            letsgoerror.setText("Please fill in all blanks")
            letsgoerror.setWindowTitle("Error")
            letsgoerror.setIcon(QMessageBox.Warning)
            letsgoerror.setWindowIcon(QIcon("Buttons/warning.png"))
            letsgoerror.exec_()
        else:
            pass
    
    #registerlabel
    def registerLabelClicked(self):
        #emaillabel
        self.emaillabel = QLabel("Email" , self.register_page)
        self.emaillabel.setGeometry(100,5,100,100)
        self.emaillabel.setFont(QFont('Arial',18))
        self.emaillabel.setStyleSheet('color:silver')
        self.emaillabel.setAlignment(Qt.AlignTop)

        #emailtextbox
        self.emailtext = QLineEdit(self.register_page)
        self.emailtext.move(200,0)
        self.emailtext.resize(300,30)
        self.emailtext.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")

        #uslabel
        self.username = QLabel("Username",self.register_page)
        self.username.setFont(QFont('Arial' , 18))
        self.username.setGeometry(55,50,120,85)
        self.username.setStyleSheet("color:#BFBFBF;")

        #ustextbox
        self.ustextbox = QLineEdit(self.register_page)
        self.ustextbox.move(200,75)
        self.ustextbox.resize(300,30)
        self.ustextbox.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")

        #passlabel
        self.passlabel = QLabel("Password",self.register_page)
        self.passlabel.setFont(QFont('Arial' , 18))
        self.passlabel.setGeometry(55,125,120,85)
        self.passlabel.setStyleSheet("color:#BFBFBF;")


        #passtextbox
        self.passtextbox1 = QLineEdit(self.register_page)
        self.passtextbox1.move(200,150)
        self.passtextbox1.resize(300,30)
        self.passtextbox1.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")
        self.passtextbox1.setEchoMode(QLineEdit.Password)
        self.confirm_label = QLabel("Confirm" , self.register_page)
        self.confirm_label.setFont(QFont('Arial' , 18))
        self.confirm_label.setGeometry(70,200,120,70)
        self.confirm_label.setStyleSheet("color:#BFBFBF")

        #passtextbox
        self.confirm_textbox = QLineEdit(self.register_page)
        self.confirm_textbox.move(200,218)
        self.confirm_textbox.resize(300,30)
        self.confirm_textbox.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")
        self.confirm_textbox.setEchoMode(QLineEdit.Password)

        #registerbutton
        self.registerbutton = QPushButton("Register" , self.register_page)
        self.registerbutton.setGeometry(250,265,100,30)
        self.registerbutton.setStyleSheet("background-color:silver;border-style:outset;border-width:2px;border-radius:15px;padding:6px;border-color:#264348;")
        self.registerbutton.clicked.connect(self.registerDB)

        #logbutton
        self.logbutton = QPushButton("L͟o͟g͟i͟n͟",self.register_page)
        self.logbutton.setGeometry(270,305,50,20)
        self.logbutton.setFlat(True)
        self.logbutton.clicked.connect(self.logButtonClicked)
        self.logbutton.setFont(QFont('Arial' , 8))
        self.logbutton.setStyleSheet("background-color:gray;color:rgb(175,93,72)")

        self.stacked_widget3.setCurrentIndex(1)
    
    def registerDB(self):
        if self.emailtext.text() == "" or self.passtextbox1.text() == "" or self.confirm_textbox.text() == "" or self.ustextbox.text() == "":
            registererror = QMessageBox()
            registererror.setStyleSheet("background-color:dimgray;color:silver;")
            registererror.setText("Please fill in all blanks")
            registererror.setWindowTitle("Error")
            registererror.setIcon(QMessageBox.Warning)
            registererror.setWindowIcon(QIcon("Buttons/warning.png"))
            registererror.exec_()
        elif self.passtextbox1.text() != self.confirm_textbox.text():
            passworderror = QMessageBox()
            passworderror.setStyleSheet("background-color:dimgray;color:silver;")
            passworderror.setText("Passwords do not match")
            passworderror.setWindowTitle("Error")
            passworderror.setIcon(QMessageBox.Warning)
            passworderror.setWindowIcon(QIcon("Buttons/warning.png"))
            passworderror.exec_()
        else:
            pass
    def logButtonClicked(self):
                #usernamelabel
        self.label2 = QLabel("Email" , self.login_page)
        self.label2.setFont(QFont('Arial' , 20))
        self.label2.setGeometry(100,20,100,40)
        self.label2.setStyleSheet("color:#BFBFBF;")

        

        # usernametextbox
        self.ustextbox = QLineEdit(self.login_page)
        self.ustextbox.move(250,22)
        self.ustextbox.resize(300,30)
        self.ustextbox.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")

        #passtextbox
        self.passtextbox = QLineEdit(self.login_page)
        self.passtextbox.move(250,130)
        self.passtextbox.resize(300,30)
        self.passtextbox.setStyleSheet("border: 3px solid dimgray;border-style:outset;border-width:2px;border-radius:10px;color:silver")
        self.passtextbox.setEchoMode(QLineEdit.Password)
        #passlabel
        self.label3 = QLabel("Password",self.login_page)
        self.label3.setFont(QFont('Arial' , 18))
        self.label3.setGeometry(100,86,120,120)
        self.label3.setStyleSheet("color:#BFBFBF;")

        #letsgobutton
        self.letsgobutton = QPushButton("Lets Go" , self.login_page)
        self.letsgobutton.setGeometry(250,200,100,30)
        self.letsgobutton.setStyleSheet("background-color:silver;border-style:outset;border-width:2px;border-radius:15px;padding:6px;border-color:#264348;")
        self.letsgobutton.clicked.connect(self.letsgoDB)


        #registerlinklabel
        self.regButton = QPushButton("R͟e͟g͟i͟s͟t͟e͟r͟",self.login_page)
        self.regButton.setGeometry(270,255,50,20)
        self.regButton.clicked.connect(self.registerLabelClicked)
        self.regButton.setFlat(True)
        self.regButton.setFont(QFont('Arial' , 8))
        self.regButton.setStyleSheet("background-color:rgb(35,35,35);color:rgb(175,93,72)")
        self.stacked_widget3.setCurrentIndex(0)
