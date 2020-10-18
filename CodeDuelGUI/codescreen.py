#
#
###Updated By Venoox 02.10.2020
#
#
import PyQt5
from PyQt5 import QtWidgets , QtCore , QtGui
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
import sys
from homescreenn import MainWindow
import syntax_pars

class CodeWindow(QWidget):
    def __init__(self):
        super(CodeWindow , self).__init__()
        self.layout  = QVBoxLayout()
        self.layout.addWidget(CodeScreenBar(self))
        self.sizegrip = QtWidgets.QSizeGrip(self)
        self.sizegrip.setStyleSheet("background-color:black")

        #screen styles
        self.setStyleSheet("background-color:rgb(35,35,35)")
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addStretch(-1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(1080,700)

        ############################################
        ##Layouts
        ############################################
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setContentsMargins(5,0,5,0)


        self.problemsLayout = QVBoxLayout()
        self.problemsLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addLayout(self.problemsLayout , Qt.AlignTop)

        self.problem_btns_layout = QHBoxLayout()
        self.problem_btns_layout.setContentsMargins(0,0,0,0)
        self.problemsLayout.addLayout(self.problem_btns_layout , Qt.AlignTop)

        self.problem_layout = QVBoxLayout()
        self.problem_layout.setContentsMargins(0,0,0,0)

        self.output_layout = QVBoxLayout()
        self.output_layout.setContentsMargins(0,0,0,0)

        self.status_Layout = QVBoxLayout()
        self.status_Layout.setContentsMargins(0,0,0,0)

        self.status_profile_photos_Layout = QHBoxLayout()
        self.status_profile_photos_Layout.setContentsMargins(0,0,0,0)

        self.status_names_Layout = QHBoxLayout()
        self.status_names_Layout.setContentsMargins(0,0,0,0)

        self.codescreenLayout = QVBoxLayout()
        self.codescreenLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addLayout(self.codescreenLayout , Qt.AlignTop)


        #######################################################
        ##Stacked Widgets
        #######################################################
        self.problems_stacked_widgets = QStackedWidget()
        self.problemsLayout.addWidget(self.problems_stacked_widgets)
        
        self.problem_widget = QWidget()
        self.problems_stacked_widgets.addWidget(self.problem_widget)
        self.problem_widget.setLayout(self.problem_layout)

        self.output_widget = QWidget()
        self.problems_stacked_widgets.addWidget(self.output_widget)
        self.output_widget.setLayout(self.output_layout)
        
        self.status_widget = QWidget()
        self.problems_stacked_widgets.addWidget(self.status_widget)
        self.status_widget.setLayout(self.status_Layout)

        ###########################################
        ##Problem Screen
        ###########################################
        self.problem_btn = QPushButton("Problem")
        self.problem_btn.setFixedHeight(30)
        self.problem_btn.clicked.connect(self.problem_btn_clicked)
        self.problem_btn.setStyleSheet("""QPushButton{
            border:none;
            background-color:#595959;
        }
        QPushButton:hover{
            border-bottom:4px solid rgb(0,191,255);
        }""")

        self.output_btn = QPushButton("Output")
        self.output_btn.setFixedHeight(30)
        self.output_btn.clicked.connect(self.output_btn_clicked)
        self.output_btn.setStyleSheet("""QPushButton{
            border:none;
            background-color:#595959;
        }
        QPushButton:hover{
            border-bottom:4px solid rgb(0,191,255);
        }""")

        self.status_btn = QPushButton("Status")
        self.status_btn.setFixedHeight(30)
        self.status_btn.clicked.connect(self.status_btn_clicked)
        self.status_btn.setStyleSheet("""QPushButton{
            border:none;
            background-color:#595959;
        }
        QPushButton:hover{
            border-bottom:4px solid rgb(0,191,255);
        }""")

        self.problem_graphicsView = QLabel()
        self.problem_graphicsView.setFixedHeight(520)
        self.problem_graphicsView.setAlignment(Qt.AlignTop)
        self.problem_graphicsView.setStyleSheet("border:1px solid white;color:white;font-size:16px;padding-bottom:10px")

        self.output_graphicsView = QLabel()
        self.output_graphicsView.setFixedHeight(520)
        self.output_graphicsView.setAlignment(Qt.AlignTop)
        self.output_graphicsView.setStyleSheet("border:1px solid white;color:white;font-size:16px;padding-bottom:10px")

        self.MainWindowClass = MainWindow()
        
        self.our_profile_photo_path = self.MainWindowClass.pp_path

        self.our_profile_photo = QPixmap(self.our_profile_photo_path)


        self.our_vs_photo = QLabel()
        self.our_vs_photo.setFixedHeight(80)
        self.our_vs_photo.setPixmap(self.our_profile_photo)
        self.our_vs_photo.setAlignment(Qt.AlignRight)
        self.our_vs_photo.setStyleSheet("""QLabel{
            border-radius:5px;
        }""")

        self.our_username = QLabel("Our Username")

        self.versus_Label = QLabel("VS")
        self.versus_Label.setAlignment(Qt.AlignCenter)
        self.versus_Label.setStyleSheet("color:white;font-size:24px;")

        self.enemys_vs_photo = QLabel()
        self.enemys_vs_photo.setFixedHeight(80)
        self.enemys_vs_photo.setPixmap(self.our_profile_photo)
        self.enemys_vs_photo.setStyleSheet("""QLabel{
            border-radius:5px;
        }""")

        self.enemys_username = QLabel("Enemys Username")


        self.time = 0

        self.timeLabel = QLabel("Time:" + str(self.time))
        self.timeLabel.setFont(QFont("Arial" , 20))
        self.timeLabel.setStyleSheet("color:#E6FFED")
        self.timeLabel.setAlignment(Qt.AlignCenter)

        self.endDuel_btn = QPushButton("End Duel")
        self.endDuel_btn.setFixedHeight(30)
        self.endDuel_btn.setStyleSheet("""QPushButton{
            border:none;
            background-color:#595959;
        }
        QPushButton:hover{
            border-bottom:4px solid rgb(0,191,255);
        }""")     

        ####################################################
        ##CodeScreen
        ####################################################
        self.codeScreen1 = QPlainTextEdit()
        self.codeScreen1.setFixedHeight(500)
        self.codeScreen1.setStyleSheet("color:white;")
        self.highlighter = syntax_pars.PythonHighlighter(self.codeScreen1.document())
        self.codeScreen1.show()

        self.codePrewiew = QPlainTextEdit()
        self.codePrewiew.setFixedHeight(100)
        self.codePrewiew.setStyleSheet("color:white;")
        self.highlighter = syntax_pars.PythonHighlighter(self.codePrewiew.document())
        self.codePrewiew.show()

        #addWidgets
        self.problem_btns_layout.addWidget(self.problem_btn)
        self.problem_btns_layout.addWidget(self.output_btn)
        self.problem_btns_layout.addWidget(self.status_btn)
        
        self.problem_layout.addWidget(self.problem_graphicsView)
        self.problemsLayout.addWidget(self.timeLabel , Qt.AlignTop)
        self.problemsLayout.addWidget(self.endDuel_btn)

        self.codescreenLayout.addWidget(self.codeScreen1)
        self.codescreenLayout.addWidget(self.codePrewiew)

        self.output_layout.addWidget(self.output_graphicsView)

        self.status_Layout.addLayout(self.status_profile_photos_Layout)
        self.status_Layout.addLayout(self.status_names_Layout)


        self.status_profile_photos_Layout.addWidget(self.our_vs_photo)
        self.status_profile_photos_Layout.addWidget(self.versus_Label)
        self.status_profile_photos_Layout.addWidget(self.enemys_vs_photo)


        self.layout.addLayout(self.mainLayout , Qt.AlignTop)
        self.layout.addWidget(self.sizegrip,0,Qt.AlignBottom|Qt.AlignRight)
        self.setLayout(self.layout)

    ############################################
    ##Functions
    ############################################
    def problem_btn_clicked(self):
        self.problems_stacked_widgets.setCurrentIndex(0)

    def output_btn_clicked(self):
        self.problems_stacked_widgets.setCurrentIndex(1)
    
    def status_btn_clicked(self):
        self.problems_stacked_widgets.setCurrentIndex(2)


class CodeScreenBar(QWidget):
    def __init__(self, parent):
        super(CodeScreenBar, self).__init__()
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
        super(CodeScreenBar, self).resizeEvent(QResizeEvent)
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
    ex = CodeWindow()
    ex.show()
    sys.exit(app.exec_())