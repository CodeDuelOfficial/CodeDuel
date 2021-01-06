#
#
###Updated By Emircan Demirci 2.12.2020
#
#
import PyQt5
from PyQt5 import QtWidgets , QtCore , QtGui
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
import sys
import os

def mask_image(imgdata, imgtype='jpg', size=256):
    """Return a ``QPixmap`` from *imgdata* masked with a smooth circle.

    *imgdata* are the raw image bytes, *imgtype* denotes the image type.

    The returned image will have a size of *size* × *size* pixels.

    """
    # Load image and convert to 32-bit ARGB (adds an alpha channel):
    image = QImage.fromData(imgdata, imgtype)
    image.convertToFormat(QImage.Format_ARGB32)

    # Crop image to a square:
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
    )
    image = image.copy(rect)

    # Create the output image with the same dimensions and an alpha channel
    # and make it completely transparent:
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    # Create a texture brush and paint a circle with the original image onto
    # the output image:
    brush = QBrush(image)        # Create texture brush
    painter = QPainter(out_img)  # Paint the output image
    painter.setBrush(brush)      # Use the image texture brush
    painter.setPen(Qt.NoPen)     # Don't draw an outline
    painter.setRenderHint(QPainter.Antialiasing, True)  # Use AA
    painter.drawEllipse(0, 0, imgsize, imgsize)  # Actually draw the circle
    painter.end()                # We are done (segfault if you forget this)

    # Convert the image to a pixmap and rescale it.  Take pixel ratio into
    # account to get a sharp image on retina displays:
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    return pm

class User_Inputs(QPlainTextEdit):
    def __init__(self , patern = None):
        super().__init__(patern)
        self.setStyleSheet("""
        QPlainTextEdit{
            border: 3px solid dimgray;
            border-style:outset;
            border-width:2px;
            border-radius:10px;
            color:silver;
            margin-left:300px;
            margin-right:300px;
            font-size:20px;
        }
        """)


class HomeScreen(QWidget):
    binds = {"add_friend": None, "search_friend": None} # binding names can change.
    def __init__(self):
        super(HomeScreen , self).__init__()
        self.main = QVBoxLayout() #apps main layout
        self.main.addWidget(TitleBar(self))

        self.layout_map = {}
        self.button_map = {}

        self.initLayout()
        
        self.main.addLayout(self.layout_map["objects"])

        #main menu main objects
        self.setStyleSheet("background-color:#262626;")
        self.main.setContentsMargins(0,0,0,0)
        self.sizegrip = QtWidgets.QSizeGrip(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(800,600)
        self.setLayout(self.main)
        
        self.pp_path = "Buttons/unnamed.gif"


        self.initStackedWidgets()
        self.initMainLeftMenu()
        self.initHomePage()
        self.initFriendsPage()
        self.initProfilePage()
        self.initSettingsPage()
        self.initEditProfile()
        self.initChangePassword()
        self.addWidgetsToLayout()

        self.show()
    
    @classmethod
    def bind(cls,name):
        assert (name in cls.binds)

        def getFunc(func):
            cls.binds[name] = func
        return getFunc 
    
    #initialize Layouts
    def initLayout(self):
        #all objects layout
        self.layout_map["objects"] = QHBoxLayout()
        self.layout_map["objects"].setContentsMargins(0,0,0,0)
        self.layout_map["objects"].addSpacing(0)
        #all layout_map["menus"]
        self.layout_map["menus"] = QVBoxLayout()
        self.layout_map["menus"].setContentsMargins(0,0,0,0)
        self.layout_map["menus"].addSpacing(-6)
        #all mainobjects layout
        self.layout_map["main"] = QVBoxLayout()
        self.layout_map["main"].setContentsMargins(0,0,0,0)
        self.layout_map["main"].addSpacing(1)
        #main page all layouts layout
        self.layout_map["allmain_page"] = QVBoxLayout()
        self.layout_map["allmain_page"].setContentsMargins(0,0,0,0)
        #main page layout
        self.layout_map["main_page"] = QHBoxLayout()
        self.layout_map["main_page"].setContentsMargins(0,0,0,0)
        #main page vbox layout
        self.layout_map["mainPage_vbox"] = QVBoxLayout()
        self.layout_map["main_page"].setContentsMargins(0,0,0,0)
        self.layout_map["objects"].addLayout(self.layout_map["menus"])
        self.layout_map["objects"].addLayout(self.layout_map["main"])
        #all friends page layout
        self.layout_map["friends_page_objects"] = QVBoxLayout()
        self.layout_map["friends_page_objects"].setContentsMargins(0,0,5,0)
        self.layout_map["friends_page_objects"].addSpacing(0)
        #main friends layout
        self.layout_map["myFriends_Page"] = QVBoxLayout()
        self.layout_map["myFriends_Page"].setContentsMargins(0,0,0,0)
        #friends menu layout 
        self.layout_map["friendsMenu"] = QHBoxLayout()
        self.layout_map["friendsMenu"].setContentsMargins(0,0,0,0)
        #pending request layout
        self.layout_map["pending_requests"] = QVBoxLayout()
        self.layout_map["pending_requests"].setContentsMargins(0,0,0,0)
        #search layout
        self.layout_map["searchPage"] = QVBoxLayout()
        self.layout_map["searchPage"].setContentsMargins(0,0,0,0)
        #profile page layout
        self.layout_map["profilePage"] = QVBoxLayout()
        self.layout_map["profilePage"].setContentsMargins(0,0,0,0)
        #settings layout
        self.layout_map["settingsPage"] = QVBoxLayout()
        self.layout_map["settingsPage"].setContentsMargins(0,0,0,0)
        #settings profile scroll layout
        self.profile_settings_scroll = QScrollArea()
        self.profile_settings_scroll.setWidgetResizable(True)
        self.profile_settings_scroll.setStyleSheet("""QScrollArea
        {
            border:none;
            margin-right:5px;
        }""")
        self.profile_settings_scroll.verticalScrollBar().setStyleSheet(""" QScrollBar:vertical{
        border: 2px solid grey;
        background: #262626;
        border-radius: 4px;
        }
        QScrollBar QWidget{
            background-color:transparent;
        }
        QScrollBar::handle:vertical
        {
            background-color:#141414;         /* #605F5F; */
            min-height: 5px;
            border-radius: 4px;
            width:50px;
        }
        
        QScrollBar::add-line:vertical
        {
            margin: 0px 3px 0px 3px;
            width: 10px;
            height: 10px;
            subcontrol-position: right;
            subcontrol-origin: margin;
            background:none;
            color:none;
        }

        QScrollBar::sub-line:vertical
        {
            margin: 0px 3px 0px 3px;
            height: 10px;
            width: 10px;
            subcontrol-position: left;
            subcontrol-origin: margin;
            background:none;
            color:none;}""")
        #profile settings layout
        self.layout_map["profileSettings"] = QVBoxLayout()
        self.layout_map["profileSettings"].setContentsMargins(0,0,0,0)
        #settings menu layout
        self.layout_map["settingsMenu"] = QHBoxLayout()
        self.layout_map["settingsMenu"].setContentsMargins(0,0,0,0)
        #edit profile layout
        self.layout_map["editProfile"] = QVBoxLayout()
        self.layout_map["editProfile"].setContentsMargins(0,0,0,0)
        #edit profile buttons layout
        self.layout_map["saveClose_btn_editPage"] = QHBoxLayout()
        self.layout_map["saveClose_btn_editPage"].setContentsMargins(0,0,0,0)
        #change password layout
        self.layout_map["changePassword_page"] = QVBoxLayout()
        self.layout_map["changePassword_page"].setContentsMargins(0,0,0,0)
    #initialize HomeScreen
    def initHomePage(self):
        ######################################
        ##Main objects
        ######################################
        self.welcome_label = QLabel("<h1>Welcome to the</h1>" , self.mainscreen_objects_widget)
        self.welcome_label.setAlignment(Qt.AlignRight)
        self.welcome_label.setFont(QFont('Arial' , 15))
        self.layout_map["main_page"].addWidget(self.welcome_label)
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
        self.layout_map["main_page"].addWidget(self.codeDuel_label)

        self.what_is_app_title = QLabel("<h2>What is <font color = 'red'>Code</font><font color = 'orange'>Duel</font>?</h2>" , self.mainscreen_objects_widget)
        self.what_is_app_title.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-left:10px;
        }""")
        self.what_is_app_title.setFixedHeight(60)
        self.what_is_app_title.setFont(QFont('Arial' , 15))
        self.what_is_app_title.setAlignment(Qt.AlignLeft)
        self.layout_map["mainPage_vbox"].addWidget(self.what_is_app_title)
        self.about_codeDuel = QLabel("<strong>With CodeDuel, you can fight codes with your friends.The first person <br>who finds the problem will win the duel.<br>If you are new, you can learn the game from our site!<br><a href='http://code-duel.com/'><font color = red>Code</font><font color = orange>Duel</font></a></strong>" , self.mainscreen_objects_widget)
        self.about_codeDuel.setOpenExternalLinks(True)
        self.about_codeDuel.setFont(QFont('Arial' ,20))
        self.about_codeDuel.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-right:20px;
        }""")
        self.about_codeDuel.setAlignment(Qt.AlignHCenter)
        self.layout_map["mainPage_vbox"].addWidget(self.about_codeDuel)
    
    #initialize all stackedwidgets
    def initStackedWidgets(self):
        #stacked widgets

        #######################################
        ##Left Menus
        #######################################
        self.all_left_menus_stacked_wiget = QStackedWidget()
        self.all_left_menus_stacked_wiget.setFixedWidth(100)
        self.layout_map["menus"].addWidget(self.all_left_menus_stacked_wiget)

        self.main_left_menu_widget = QWidget()
        self.all_left_menus_stacked_wiget.addWidget(self.main_left_menu_widget)

        self.profile_page_left_menu_widget = QWidget()
        self.all_left_menus_stacked_wiget.addWidget(self.profile_page_left_menu_widget)

        #######################################
        ##Main Objects 
        #######################################
        self.main_objects_stacked_widget = QStackedWidget()
        self.layout_map["main"].addWidget(self.main_objects_stacked_widget)

        self.mainscreen_objects_widget = QWidget()
        self.main_objects_stacked_widget.addWidget(self.mainscreen_objects_widget)

        self.mainscreen_objects_widget.setLayout(self.layout_map["allmain_page"])
        self.layout_map["allmain_page"].addLayout(self.layout_map["main_page"])
        self.layout_map["allmain_page"].addLayout(self.layout_map["mainPage_vbox"] , Qt.AlignRight)

        self.friends_screen_widget = QWidget()
        self.main_objects_stacked_widget.addWidget(self.friends_screen_widget)
        self.friends_screen_widget.setLayout(self.layout_map["friends_page_objects"])
        self.layout_map["friends_page_objects"].addLayout(self.layout_map["friendsMenu"] , Qt.AlignTop)

        self.profile_page_widget = QWidget()
        self.main_objects_stacked_widget.addWidget(self.profile_page_widget)
        self.profile_page_widget.setLayout(self.layout_map["profilePage"])

        self.settings_page_widget = QWidget()
        self.main_objects_stacked_widget.addWidget(self.settings_page_widget)
        self.settings_page_widget.setLayout(self.layout_map["settingsPage"])
        
        self.layout_map["settingsPage"].addLayout(self.layout_map["settingsMenu"] , Qt.AlignTop)
        ################################################################################
        ##Friends Menu Widgets
        #################################################################################
        self.friends_Stacked_widget = QStackedWidget()
        self.layout_map["friends_page_objects"].addWidget(self.friends_Stacked_widget)

        self.myFriendsWidget = QWidget()
        self.myFriendsWidget.setLayout(self.layout_map["myFriends_Page"])

        self.pending_rqst_widget = QWidget()
        self.pending_rqst_widget.setLayout(self.layout_map["pending_requests"])

        self.search_lineedit_widget = QWidget()
        self.search_lineedit_widget.setLayout(self.layout_map["searchPage"])

        self.friends_Stacked_widget.addWidget(self.search_lineedit_widget)
        self.friends_Stacked_widget.addWidget(self.pending_rqst_widget)
        self.friends_Stacked_widget.addWidget(self.myFriendsWidget)
        #########################################################################
        ##settings widgets
        #########################################################################
        self.settings_stacked_widget = QStackedWidget()
        self.layout_map["settingsPage"].addWidget(self.settings_stacked_widget)

        self.profile_settings_page = QWidget()
        self.profile_settings_page.setLayout(self.layout_map["profileSettings"])
        self.profile_settings_scroll.setWidget(self.profile_settings_page)

        self.edit_profile_page = QWidget()
        self.edit_profile_page.setLayout(self.layout_map["editProfile"])

        self.change_password_page = QWidget()
        self.change_password_page.setLayout(self.layout_map["changePassword_page"])

        self.settings_stacked_widget.addWidget(self.profile_settings_scroll)
        self.settings_stacked_widget.addWidget(self.edit_profile_page)
        self.settings_stacked_widget.addWidget(self.change_password_page)
        
        
    def addWidgetsToLayout(self):
        ##########################################
        ##Layouts
        #########################################

        #friends top menu
        self.layout_map["friendsMenu"].addWidget(self.button_map["my_friends"])
        self.layout_map["friendsMenu"].addWidget(self.button_map["pending_request"])
        self.layout_map["friendsMenu"].addWidget(self.ghostLabel2)
        self.layout_map["friendsMenu"].addWidget(self.search_lineedit)
        self.layout_map["friendsMenu"].addWidget(self.button_map["search_btn"])

        #my friends page
        self.layout_map["myFriends_Page"].addWidget(self.myfriends_page_label)

        #pending requests page
        self.layout_map["pending_requests"].addWidget(self.pendingrqst_page_label)

        #search page
        self.layout_map["searchPage"].addWidget(self.search_page_label)

        #profile page
        self.layout_map["profilePage"].addWidget(self.profile_page_photo)
        self.layout_map["profilePage"].addWidget(self.profile_username)
        self.layout_map["profilePage"].addWidget(self.previous_matches)

        #settings page        
        self.layout_map["settingsMenu"].addWidget(self.button_map["profile_settings"] , Qt.AlignCenter)
        self.layout_map["settingsMenu"].addWidget(self.settings_ghost_label)

        #profile settings page
        self.layout_map["profileSettings"].addWidget(self.profile_settings_label)
        self.layout_map["profileSettings"].addWidget(self.profile_settings_photo)
        self.layout_map["profileSettings"].addWidget(self.settings_username)
        self.layout_map["profileSettings"].addWidget(self.user_email)
        self.layout_map["profileSettings"].addWidget(self.button_map["edit_profile"] , alignment = Qt.AlignTop)
        self.layout_map["profileSettings"].addWidget(self.change_password_label)
        self.layout_map["profileSettings"].addWidget(self.button_map["change_password"])
        
        #edit profile button clicked
        self.layout_map["editProfile"].addWidget(self.edit_profile_pp)
        self.layout_map["editProfile"].addWidget(self.button_map["change_avatar"])
        self.layout_map["editProfile"].addWidget(self.edit_username)
        self.layout_map["editProfile"].addWidget(self.edit_email)
        self.layout_map["editProfile"].addLayout(self.layout_map["saveClose_btn_editPage"]) 
        self.layout_map["saveClose_btn_editPage"].addWidget(self.button_map["save_changes"])
        self.layout_map["saveClose_btn_editPage"].addWidget(self.button_map["cancel_btn"])

        self.layout_map["changePassword_page"].addWidget(self.old_password)
        self.layout_map["changePassword_page"].addWidget(self.new_password)

        #sizegrip
        self.main.addWidget(self.sizegrip,0,Qt.AlignBottom|Qt.AlignRight)
    
    #initialize Friends Page
    def initFriendsPage(self):
        ###########################################################
        ##Friends Screen
        ###########################################################

        #search page
        self.search_page_label = QLabel("check the name or the 4 digit number!")
        self.search_page_label.setAlignment(Qt.AlignCenter)
        self.search_page_label.setFont(QFont('Arial' , 25))
        self.search_page_label.setStyleSheet("color:#F2F2EB")
        
        #pending requests page
        self.pendingrqst_page_label = QLabel("You dont have any requests.")
        self.pendingrqst_page_label.setAlignment(Qt.AlignCenter)
        self.pendingrqst_page_label.setFont(QFont('Arial' , 25))
        self.pendingrqst_page_label.setStyleSheet("color:#F2F2EB")
        #my friends page
        self.myfriends_page_label = QLabel("I hope you have friends :(")
        self.myfriends_page_label.setAlignment(Qt.AlignCenter)
        self.myfriends_page_label.setFont(QFont('Arial' , 25))
        self.myfriends_page_label.setStyleSheet("color:#F2F2EB")

        #friends menu
        self.button_map["my_friends"] = QPushButton("My Friends")
        self.button_map["my_friends"].setFixedSize(90,30)
        self.button_map["my_friends"].setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            color:#141414;
        }
        QPushButton:hover{
            border-bottom: 4px solid #5C5C5C;
        }""")
        self.button_map["my_friends"].clicked.connect(self.myfriends_btn_clicked)

        self.button_map["pending_request"] = QPushButton("Pending Requests")
        self.button_map["pending_request"].setFixedSize(90,30)
        self.button_map["pending_request"].setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            color:#141414;
        }
        QPushButton:hover{
            border-bottom: 4px solid #5C5C5C;
        }""")
        self.button_map["pending_request"].clicked.connect(self.pending_rqst_btn_clicked)

        self.search_lineedit = QLineEdit()
        self.search_lineedit.setPlaceholderText("Search your friends, you must write name#0000")
        self.search_lineedit.setFixedSize(400,30)
        self.search_lineedit.setFont(QFont('Arial' , 10))
        self.search_lineedit.setStyleSheet("""QLineEdit{
            border: 3px solid #5C5C5C;
            color:#F2F2EB;
            background-color:#5c5c5c
        }""")
        
        self.button_map["search_btn"] = QPushButton("Search")
        self.button_map["search_btn"].setFixedSize(90,30)
        self.button_map["search_btn"].setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            color:#141414;
        }
        QPushButton:hover{
            border-bottom: 4px solid #5C7B5C;
        }""")
        self.button_map["search_btn"].clicked.connect(self.search_btn_clicked)

        #ghost label (inactive label)
        self.ghostLabel2 = QLabel()
        self.ghostLabel2.setStyleSheet("""background-color:#8C8C8C;""")
        self.ghostLabel2.setAlignment(Qt.AlignCenter)
        self.ghostLabel2.setFixedHeight(30)
    
    #initialize Profile Page
    def initProfilePage(self):
        ##################################
        ##profile page
        ##################################
        self.match_number = 0
        self.previous_matches = QLabel("Previous Matches:" + str(self.match_number))
        self.previous_matches.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-top:10px;
            font-size:32px;
        }""")
        self.previous_matches.setAlignment(Qt.AlignHCenter)

        self.profile_username = QLabel("Username")
        self.profile_username.setAlignment(Qt.AlignHCenter)
        self.profile_username.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-top:10px;
            font-size:32px;
        }""")
        
        self.profile_photo_data= open(self.pp_path, 'rb').read()
        self.profile_photo_pixmap = mask_image(self.profile_photo_data)

        self.profile_page_photo = QLabel()
        self.profile_page_photo.setAlignment(Qt.AlignCenter) 
        self.profile_page_photo.setPixmap(self.profile_photo_pixmap)
        self.profile_page_photo.setFixedHeight(300)
        self.profile_page_photo.setStyleSheet("""QLabel{
            margin:300px;
            border:none;
        }""")
        
        #profile page left menu object
        self.button_map["goto_mainmenu"] = QPushButton('' , self.profile_page_left_menu_widget)
        self.button_map["goto_mainmenu"].setIcon(QIcon("Buttons/settingsGoBackbtn.png"))
        self.button_map["goto_mainmenu"].setGeometry(10,10,35,35)
        self.button_map["goto_mainmenu"].setStyleSheet("""QPushButton{
            background-color:#595959;
            border:none;
        }
        QPushButton:hover{
            border-bottom:4px solid rgb(0,191,255);
        }""")
        self.button_map["goto_mainmenu"].clicked.connect(self.goto_mainmenu_btn_clicked)
    
    
    
    #initialize Main Page Left Menu
    def initMainLeftMenu(self):
        ######################################
        ##left menu
        ######################################
        self.ghostLabel = QLabel(self.main_left_menu_widget)
        self.ghostLabel.resize(100,16770)
        self.ghostLabel.setStyleSheet("background-color:#141414;")

        self.button_map["profile_photo"] = QPushButton(self.main_left_menu_widget)
        self.button_map["profile_photo"].setIcon(QIcon(self.pp_path))
        self.button_map["profile_photo"].setIconSize(QSize(64,64))
        self.button_map["profile_photo"].setFixedSize(50,50)
        self.button_map["profile_photo"].move(25,0)
        self.region = QRegion(self.button_map["profile_photo"].rect() , QRegion.Ellipse)
        self.button_map["profile_photo"].setMask(self.region)
        self.button_map["profile_photo"].clicked.connect(self.profile_photo_clicked)

        #main left menu home button       
        self.button_map["home"] = QPushButton('' , self.main_left_menu_widget)
        self.button_map["home"].setIcon(QIcon("Buttons/homeButton2.png"))
        self.button_map["home"].setGeometry(-2,80,105,50)
        self.button_map["home"].setStyleSheet("""QPushButton{
            background-color:#595959;
            border:none;
        }
        QPushButton:hover{
            border-bottom: 4px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(0,191,255),stop:1 rgba(0, 0, 0, 0));
        }""")
        self.button_map["home"].clicked.connect(self.home_btn_clicked)
        self.button_map["home"].setIconSize(QSize(20,20))


        self.button_map["friends"] = QPushButton('' , self.main_left_menu_widget)
        self.button_map["friends"].setIcon(QIcon("Buttons/yourFriends.png"))
        self.button_map["friends"].setGeometry(-2,130,105,50)
        self.button_map["friends"].setStyleSheet("""QPushButton{
            background-color:#595959;
            border:none;
            margin-top:2px;
        }
        QPushButton:hover{
            border-bottom: 4px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(0,191,255),stop:1 rgba(0, 0, 0, 0));
        }""")
        self.button_map["friends"].clicked.connect(self.friends_btn_clicked)
        self.button_map["friends"].setIconSize(QSize(20,20))

        self.button_map["settings"] = QPushButton('' , self.main_left_menu_widget)
        self.button_map["settings"].setIcon(QIcon('Buttons/settingsBtn.png'))
        self.button_map["settings"].setGeometry(-2,180,105,50)
        self.button_map["settings"].setStyleSheet("""QPushButton{
            background-color:#595959;
            border:none;
            margin-top:2px;
        }
        QPushButton:hover{
            border-bottom: 4px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(0,191,255),stop:1 rgba(0, 0, 0, 0));
        }""")
        self.button_map["settings"].clicked.connect(self.settings_btn_clicked)
        self.button_map["settings"].setIconSize(QSize(20,20))

    def initSettingsPage(self):     
        #profile settings title
        self.profile_settings_label = QLabel("<h1><strong><font style='color:#bfbfbf'>Profile</font></strong></h1>")

        #ghostLabel
        self.settings_ghost_label = QLabel()
        self.settings_ghost_label.setStyleSheet("""QLabel{
            background-color:#8C8C8C;
            margin-right:5px;
        }""")
        self.settings_ghost_label.setAlignment(Qt.AlignCenter)
        self.settings_ghost_label.setFixedHeight(30)

        #profile settings button
        self.button_map["profile_settings"] = QPushButton("Profile")
        self.button_map["profile_settings"].setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
        }
        QPushButton:hover{
            border-bottom: 4px solid #5c5c5c;
        }""")
        self.button_map["profile_settings"].setFixedHeight(30)
        self.button_map["profile_settings"].setFixedWidth(90)
        self.button_map["profile_settings"].clicked.connect(self.profile_settings_btn_clicked)


        self.user_email = QLabel("Email")
        self.user_email.setAlignment(Qt.AlignHCenter)
        self.user_email.setStyleSheet("""QLabel{
            color:#F2F2EB;
            font-size:32px;
        }""")

        #username
        self.settings_username = QLabel("Username")
        self.settings_username.setAlignment(Qt.AlignHCenter)
        self.settings_username.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-top:10px;
            font-size:32px;
        }""")

        #profile photo
        self.profile_settings_photo = QLabel()
        self.profile_settings_photo.setAlignment(Qt.AlignCenter) 
        self.profile_settings_photo.setPixmap(self.profile_photo_pixmap)
        self.profile_settings_photo.setFixedHeight(300)
        self.profile_settings_photo.setStyleSheet("""QLabel{
            border:none;
        }""")

        #edit profile button 
        self.button_map["edit_profile"] = QPushButton("Edit Profile")
        self.button_map["edit_profile"].setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            margin-left:300px;
            margin-right:300px;
        }
        QPushButton:hover{
            border-bottom: 4px solid rgb(0,191,255);
        }""")
        self.button_map["edit_profile"].setFixedHeight(30)
        self.button_map["edit_profile"].clicked.connect(self.edit_profile_btn_clicked)

        #change password title
        self.change_password_label = QLabel("<h1><strong><font style='color:#bfbfbf'>Password</font></strong></h1>")
        self.change_password_label.setStyleSheet("margin-top:50px;")

        #change password
        self.button_map["change_password"]= QPushButton("Change Password")
        self.button_map["change_password"].setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            margin-right:500px;
            margin-left:50px
        }
        QPushButton:hover{
            border-bottom: 4px solid rgb(0,191,255);
        }""")
        self.button_map["change_password"].setFixedHeight(30)
        self.button_map["change_password"].clicked.connect(self.change_password_btn_clicked)

    def initEditProfile(self):
        self.edit_profile_pp = QLabel()
        self.edit_profile_pp.setAlignment(Qt.AlignCenter) 
        self.edit_profile_pp.setPixmap(self.profile_photo_pixmap)
        self.edit_profile_pp.setFixedHeight(300)
        self.edit_profile_pp.setStyleSheet("""QLabel{
            border:none;
        }""")

        self.button_map["change_avatar"] = QPushButton("Change Avatar")
        self.button_map["change_avatar"].setFixedHeight(35)
        self.button_map["change_avatar"].setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            margin-left:300px;
            margin-right:300px;
        }
        QPushButton:hover{
            border-bottom: 4px solid rgb(0,191,255);
        }""")
        self.button_map["change_avatar"].clicked.connect(self.change_avatar_btn_clicked)

        self.edit_username = User_Inputs()
        self.edit_username.setPlainText("Username")
        self.edit_username.setFixedHeight(40)

        self.edit_email = User_Inputs()
        self.edit_email.setPlainText("Email")
        self.edit_email.setFixedHeight(40)

        self.settings_stacked_widget.setCurrentIndex(1)

        self.button_map["save_changes"] = QPushButton("Save Changes")
        self.button_map["save_changes"].setFixedHeight(35)
        self.button_map["save_changes"].setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
        }
        QPushButton:hover{
            border-bottom: 4px solid rgb(0,191,255);
        }""")

        self.button_map["cancel_btn"] = QPushButton("Cancel")
        self.button_map["cancel_btn"].setFixedHeight(35)
        self.button_map["cancel_btn"].setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
        }
        QPushButton:hover{
            border-bottom: 4px solid rgb(0,191,255);
        }""")
        self.button_map["cancel_btn"].clicked.connect(self.cancel_btn_animation)

    def initChangePassword(self):
        self.old_password = User_Inputs()
        self.old_password.setPlainText("Old Password")
        self.old_password.setFixedHeight(40)

        self.new_password = User_Inputs()
        self.new_password.setPlainText("Old Password")
        self.new_password.setFixedHeight(40)

    def theme_market_btn_clicked(self):
        pass

    #edit profile button clicked
    def edit_profile_btn_clicked(self , scroll):
        QTimer.singleShot(400 , self.initEditProfile)

    #cancel btn clicked
    def cancel_btn_animation(self):
        QTimer.singleShot(400 , self.edit_cancelbtn_clicked)

    def edit_cancelbtn_clicked(self):
        self.settings_stacked_widget.setCurrentIndex(0)
    #change password
    def change_password_btn_clicked(self):
        self.settings_stacked_widget.setCurrentIndex(2)
    #home button clicked
    def home_btn_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(0)

    #friends button clicked
    def friends_btn_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(1)

    #friends page topmenu my friends button clicked
    def myfriends_btn_clicked(self):
        self.friends_Stacked_widget.setCurrentIndex(0)

    #friends page topmenu pending requests button clicked
    def pending_rqst_btn_clicked(self):
        self.friends_Stacked_widget.setCurrentIndex(1)

    #friends page topmenu search button clicked
    def search_btn_clicked(self):
        self.friends_Stacked_widget.setCurrentIndex(2)

    #main left menu profile photo clicked
    def profile_photo_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(2)
        self.all_left_menus_stacked_wiget.setCurrentIndex(1)

    #profile page go to main menu button (<-)
    def goto_mainmenu_btn_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(0)
        self.all_left_menus_stacked_wiget.setCurrentIndex(0)
    
    #settings btn clicked
    def settings_btn_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(3)
        self.settings_stacked_widget.setCurrentIndex(0)

    def profile_settings_btn_clicked(self):
        self.settings_stacked_widget.setCurrentIndex(0)

    #open file dialog
    def change_avatar_btn_clicked(self):
        self.filter = "Images (*.png *.xpm .jpg)"
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'),filter=self.filter)
        if self.filename[0] == '':
            print("ğ")
        else:
            #this variable will connect to database
            self.pp_path = self.filename[0]
            print(self.pp_path)


    
#titlebar
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = HomeScreen()
    ex.show()
    app.exec_()