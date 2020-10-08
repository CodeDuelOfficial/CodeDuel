#
#
###Updated By Venoox 24.09.2020
#
#
import PyQt5
from PyQt5 import QtWidgets , QtCore , QtGui
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
import sys

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow , self).__init__()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(TitleBar(self))
        #all objects layout
        self.objectsLayout = QHBoxLayout()
        self.objectsLayout.setContentsMargins(0,0,0,0)
        self.objectsLayout.addSpacing(0)
        #all menusLayout
        self.menusLayout = QVBoxLayout()
        self.menusLayout.setContentsMargins(0,0,0,0)
        self.menusLayout.addSpacing(-6)
        #all mainobjects layout
        self.mainobjectsLayout = QVBoxLayout()
        self.mainobjectsLayout.setContentsMargins(0,0,0,0)
        self.mainobjectsLayout.addSpacing(1)
        #main page all layouts layout
        self.allmain_page_layouts = QVBoxLayout()
        self.allmain_page_layouts.setContentsMargins(0,0,0,0)
        #main page layout
        self.main_page_layout = QHBoxLayout()
        self.main_page_layout.setContentsMargins(0,0,0,0)
        #main page vbox layout
        self.main_page_vbox = QVBoxLayout()
        self.main_page_layout.setContentsMargins(0,0,0,0)
        self.objectsLayout.addLayout(self.menusLayout)
        self.objectsLayout.addLayout(self.mainobjectsLayout)
        
        self.mainLayout.addLayout(self.objectsLayout)

        #all friends page layout
        self.allfriends_page_layouts = QVBoxLayout()
        self.allfriends_page_layouts.setContentsMargins(0,0,5,0)
        self.allfriends_page_layouts.addSpacing(0)
        #main friends layout
        self.myFriendsLayout = QVBoxLayout()
        self.myFriendsLayout.setContentsMargins(0,0,0,0)
        #friends menu layout 
        self.friendsmenu_layout = QHBoxLayout()
        self.friendsmenu_layout.setContentsMargins(0,0,0,0)
        #pending request layout
        self.pending_rqst_Layout = QVBoxLayout()
        self.pending_rqst_Layout.setContentsMargins(0,0,0,0)
        #search layout
        self.searchLayout = QVBoxLayout()
        self.searchLayout.setContentsMargins(0,0,0,0)
        #profile page layout
        self.profile_page_layout = QVBoxLayout()
        self.profile_page_layout.setContentsMargins(0,0,0,0)
        #main menu main objects
        self.setStyleSheet("background-color:#262626;")
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.sizegrip = QtWidgets.QSizeGrip(self)
        self.sizegrip.setStyleSheet("background-color:black;")
        self.setWindowFlags(Qt.FramelessWindowHint |  QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumSize(1080,700)
        self.setLayout(self.mainLayout)
        #stacked widgets

        #######################################
        ##Left Menus
        #######################################
        self.menus_stacked_widget = QStackedWidget()
        self.menus_stacked_widget.setFixedWidth(100)
        self.menusLayout.addWidget(self.menus_stacked_widget)

        self.main_left_menu_widget = QWidget()
        self.menus_stacked_widget.addWidget(self.main_left_menu_widget)

        self.profile_menu = QWidget()
        self.menus_stacked_widget.addWidget(self.profile_menu)

        #######################################
        ##Main Objects 
        #######################################
        self.main_objects_stacked_widget = QStackedWidget()
        self.mainobjectsLayout.addWidget(self.main_objects_stacked_widget)

        self.mainscreen_objects_widget = QWidget()
        self.main_objects_stacked_widget.addWidget(self.mainscreen_objects_widget)

        self.mainscreen_objects_widget.setLayout(self.allmain_page_layouts)
        self.allmain_page_layouts.addLayout(self.main_page_layout)
        self.allmain_page_layouts.addLayout(self.main_page_vbox , Qt.AlignRight)

        self.friends_screen_widget = QWidget()
        self.main_objects_stacked_widget.addWidget(self.friends_screen_widget)

        self.friends_screen_widget.setLayout(self.allfriends_page_layouts)
        self.allfriends_page_layouts.addLayout(self.friendsmenu_layout , Qt.AlignTop)

        self.profile_menu_widget = QWidget()
        self.main_objects_stacked_widget.addWidget(self.profile_menu_widget)
        self.profile_menu_widget.setLayout(self.profile_page_layout)
        ################################################################################
        ##Friends Menu Widgets
        #################################################################################
        self.friends_Stacked_widget = QStackedWidget()
        self.allfriends_page_layouts.addWidget(self.friends_Stacked_widget)

        self.myFriendsWidget = QWidget()
        self.friends_Stacked_widget.addWidget(self.myFriendsWidget)
        self.myFriendsWidget.setLayout(self.myFriendsLayout)

        self.pending_rqst_widget = QWidget()
        self.friends_Stacked_widget.addWidget(self.pending_rqst_widget)
        self.pending_rqst_widget.setLayout(self.pending_rqst_Layout)

        self.search_friends_widget = QWidget()
        self.friends_Stacked_widget.addWidget(self.search_friends_widget)
        self.search_friends_widget.setLayout(self.searchLayout)


        #objects
        ######################################
        ##left menu
        ######################################
        self.ghostLabel = QLabel(self.main_left_menu_widget)
        self.ghostLabel.resize(100,16770)
        self.ghostLabel.setStyleSheet("background-color:#141414;")
        
        self.pp_path = None

        if self.pp_path == None:
            self.pp_path = "Icon/codeduelIcon.png"


        self.profile_photo = QPushButton(self.main_left_menu_widget)
        self.profile_photo.setIcon(QIcon(self.pp_path))
        self.profile_photo.setIconSize(QSize(64,64))
        self.profile_photo.setFixedSize(50,50)
        self.profile_photo.move(25,0)
        self.region = QRegion(self.profile_photo.rect() , QRegion.Ellipse)
        self.profile_photo.setMask(self.region)
        self.profile_photo.clicked.connect(self.profile_photo_clicked)

        #main left menu home button       
        self.home_button = QPushButton('' , self.main_left_menu_widget)
        self.home_button.setIcon(QIcon("Buttons/homeButton2.png"))
        self.home_button.setGeometry(-2,80,105,50)
        self.home_button.setStyleSheet("""QPushButton{
            background-color:#595959;
            border:none;
        }
        QPushButton:hover{
            border-bottom: 4px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(0,191,255),stop:1 rgba(0, 0, 0, 0));
        }""")
        self.home_button.clicked.connect(self.home_button_clicked)
        self.home_button.setIconSize(QSize(20,20))


        #main left menu friends button
        self.friends_btn = QPushButton('' , self.main_left_menu_widget)
        self.friends_btn.setIcon(QIcon("Buttons/yourFriends.png"))
        self.friends_btn.setGeometry(-2,130,105,50)
        self.friends_btn.setStyleSheet("""QPushButton{
            background-color:#595959;
            border:none;
            margin-top:2px;
        }
        QPushButton:hover{
            border-bottom: 4px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(0,191,255),stop:1 rgba(0, 0, 0, 0));
        }""")
        self.friends_btn.clicked.connect(self.friends_btn_clicked)
        self.friends_btn.setIconSize(QSize(20,20))

        #profile left menu
        self.go_to_mainmenu = QPushButton('' , self.profile_menu)
        self.go_to_mainmenu.setIcon(QIcon("Buttons/settingsGoBackbtn.png"))
        self.go_to_mainmenu.setGeometry(10,10,35,35)
        self.go_to_mainmenu.setStyleSheet("""QPushButton{
            background-color:#595959;
            border:none;
        }
        QPushButton:hover{
            border-bottom:4px solid rgb(0,191,255);
        }""")
        self.go_to_mainmenu.clicked.connect(self.go_to_mainmenu_clicked)

        ######################################
        ##Main objects
        ######################################
        self.welcome_label = QLabel("<h1>Welcome to the</h1>" , self.mainscreen_objects_widget)
        self.welcome_label.setAlignment(Qt.AlignRight)
        self.welcome_label.setFont(QFont('Arial' , 15))
        self.main_page_layout.addWidget(self.welcome_label)
        self.welcome_label.setStyleSheet("""QLabel{
            color:#F2F2EB;
        }""")

        self.codeDuel_label = QLabel("<h1><font color='red'>Code</font>Duel<h1>" , self.mainscreen_objects_widget)
        self.codeDuel_label.setStyleSheet("""QLabel{
            color:orange; 
            margin-left:10px;
        }""")
        self.codeDuel_label.setAlignment(Qt.AlignLeft)
        self.codeDuel_label.setFont(QFont('Arial' , 15))
        self.main_page_layout.addWidget(self.codeDuel_label)

        self.what_is = QLabel("<h2>What is <font color = 'red'>Code</font><font color = 'orange'>Duel</font>?</h2>" , self.mainscreen_objects_widget)
        self.what_is.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-left:10px;
        }""")
        self.what_is.setFixedHeight(60)
        self.what_is.setFont(QFont('Arial' , 15))
        self.what_is.setAlignment(Qt.AlignLeft)
        self.main_page_vbox.addWidget(self.what_is)
        self.about_codeDuel = QLabel("<strong>With CodeDuel, you can fight codes with your friends.The first person <br>who finds the problem will win the duel.<br>If you are new, you can learn the game from our site!<br><a href='http://code-duel.com/'><font color = red>Code</font><font color = orange>Duel</font></a></strong>" , self.mainscreen_objects_widget)
        self.about_codeDuel.setOpenExternalLinks(True)
        self.about_codeDuel.setFont(QFont('Arial' ,20))
        self.about_codeDuel.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-right:20px;
        }""")
        self.about_codeDuel.setAlignment(Qt.AlignHCenter)
        self.main_page_vbox.addWidget(self.about_codeDuel)
        
        ##################################
        ##profile menu
        ##################################
        self.match_number = 0
        self.previous_matches = QLabel("Previous Matches:" + str(self.match_number))
        self.previous_matches.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-top:10px;
            font-size:32px;
        }""")
        self.previous_matches.setAlignment(Qt.AlignHCenter)

        self.profile_name_label = QLabel("Username")
        self.profile_name_label.setAlignment(Qt.AlignHCenter)
        self.profile_name_label.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-top:10px;
            font-size:32px;
        }""")
        
        self.profile_photo_pixmap = QPixmap(self.pp_path)
        self.scaled_pixmap_photo = self.profile_photo_pixmap.scaled(300, 300)
        
        self.profile_page_photo = QLabel()
        self.profile_page_photo.setAlignment(Qt.AlignCenter) 
        self.profile_page_photo.setPixmap(self.scaled_pixmap_photo)
        self.profile_page_photo.setFixedHeight(300)
        self.profile_page_photo.setStyleSheet("""QLabel{
            margin:300px;
            border:none;
        }""")

        ###########################################################
        ##Friends Screen
        ###########################################################
        #search page
        self.search_label = QLabel("check the name or the 4 digit number!")
        self.search_label.setAlignment(Qt.AlignCenter)
        self.search_label.setFont(QFont('Arial' , 25))
        self.search_label.setStyleSheet("color:#F2F2EB")
        
        #pending requests page
        self.pendingrqst_label = QLabel("You dont have any requests.")
        self.pendingrqst_label.setAlignment(Qt.AlignCenter)
        self.pendingrqst_label.setFont(QFont('Arial' , 25))
        self.pendingrqst_label.setStyleSheet("color:#F2F2EB")
        #my friends page
        self.ı_hopeyou_havefriend = QLabel("I hope you have friends :(")
        self.ı_hopeyou_havefriend.setAlignment(Qt.AlignCenter)
        self.ı_hopeyou_havefriend.setFont(QFont('Arial' , 25))
        self.ı_hopeyou_havefriend.setStyleSheet("color:#F2F2EB")

        #friends menu
        self.my_friends_btn = QPushButton("My Friends")
        self.my_friends_btn.setFixedSize(90,30)
        self.my_friends_btn.setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            color:#141414;
        }
        QPushButton:hover{
            border-bottom: 4px solid #5C5C5C;
        }""")
        self.my_friends_btn.clicked.connect(self.my_friends_btn_clicked)

        self.pending_rqst_btn = QPushButton("Pending Requests")
        self.pending_rqst_btn.setFixedSize(90,30)
        self.pending_rqst_btn.setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            color:#141414;
        }
        QPushButton:hover{
            border-bottom: 4px solid #5C5C5C;
        }""")
        self.pending_rqst_btn.clicked.connect(self.pending_rqst_btn_cliked)

        self.search_friends = QLineEdit()
        self.search_friends.setPlaceholderText("Search your friends, you must write name#0000")
        self.search_friends.setFixedSize(400,30)
        self.search_friends.setFont(QFont('Arial' , 10))
        self.search_friends.setStyleSheet("""QLineEdit{
            border: 3px solid #5C5C5C;
            color:#F2F2EB;
            background-color:#5c5c5c
        }""")
        
        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedSize(90,30)
        self.search_btn.setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            color:#141414;
        }
        QPushButton:hover{
            border-bottom: 4px solid #5C7B5C;
        }""")
        self.search_btn.clicked.connect(self.search_btn_clicked)


        self.ghostLabel2 = QLabel()
        self.ghostLabel2.setStyleSheet("""background-color:#8C8C8C;""")
        self.ghostLabel2.setAlignment(Qt.AlignCenter)
        self.ghostLabel2.setFixedHeight(30)

        self.friendsmenu_layout.addWidget(self.my_friends_btn)
        self.friendsmenu_layout.addWidget(self.pending_rqst_btn)
        self.friendsmenu_layout.addWidget(self.ghostLabel2)
        self.friendsmenu_layout.addWidget(self.search_friends)
        self.friendsmenu_layout.addWidget(self.search_btn)

        self.myFriendsLayout.addWidget(self.ı_hopeyou_havefriend)

        self.pending_rqst_Layout.addWidget(self.pendingrqst_label)

        self.searchLayout.addWidget(self.search_label)

        self.profile_page_layout.addWidget(self.profile_page_photo)
        self.profile_page_layout.addWidget(self.profile_name_label)
        self.profile_page_layout.addWidget(self.previous_matches)

        #sizegrip
        self.mainLayout.addWidget(self.sizegrip,0,Qt.AlignBottom|Qt.AlignRight)

    #home button clicked
    def home_button_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(0)
    #friends button clicked
    def friends_btn_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(1)

    def my_friends_btn_clicked(self):
        self.friends_Stacked_widget.setCurrentIndex(0)

    def pending_rqst_btn_cliked(self):
        self.friends_Stacked_widget.setCurrentIndex(1)

    def search_btn_clicked(self):
        self.friends_Stacked_widget.setCurrentIndex(2)
    
    def profile_photo_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(2)
        self.menus_stacked_widget.setCurrentIndex(1)

    def go_to_mainmenu_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(0)
        self.menus_stacked_widget.setCurrentIndex(0)
    


class TitleBar(QWidget):
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = QLabel("CodeDuel")
        self.window_maximized = False

        btn_size = 35

        self.btn_close = QPushButton("✕")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)
        self.btn_close.setFlat(True)
        self.btn_close.move(750,0)
        self.btn_close.setStyleSheet("background-color: red;color:white;")

        self.btn_min = QPushButton("－")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.move(600,0)
        self.btn_min.setFlat(True)
        self.btn_min.setStyleSheet("background-color: gray;color:white;")

        self.btn_max = QPushButton("☐")
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size, btn_size)
        self.btn_max.move(600,0)
        self.btn_max.setFlat(True)
        self.btn_max.setStyleSheet("background-color: gray;color:white;")

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)


        self.title.setStyleSheet("""
            background-color: #141414;
            color:white;
        """)
        self.setLayout(self.layout)

        self.start = QPoint(0,0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(TitleBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False




    def btn_close_clicked(self):
        self.parent.close()



    def btn_min_clicked(self):
        self.parent.showMinimized()

    def btn_max_clicked(self):
        self.parent.showMaximized()
        self.window_maximized = True
        if self.window_maximized == True:
            self.btn_max.disconnect()
            self.btn_max.setText("❐")
            self.btn_max.clicked.connect(self.restoreDownEvent)
    
    def restoreDownEvent(self):
        self.parent.showNormal()
        self.window_maximized = False

        if self.window_maximized == False:
            self.btn_max.disconnect()
            self.btn_max.setText("☐")
            self.btn_max.clicked.connect(self.btn_max_clicked)

