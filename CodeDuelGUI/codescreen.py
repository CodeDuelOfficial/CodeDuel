#
#
###Updated By EmircanDemirci 02.10.2020
#
#
import PyQt5
from PyQt5 import QtWidgets , QtCore , QtGui
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
import sys
import syntax_pars
class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):

        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):

        self.codeEditor.lineNumberAreaPaintEvent(event)

class QCodeEdit(QtWidgets.QPlainTextEdit):
    def __init__(self,patern=None):
        super().__init__(patern)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)

    def keyPressEvent(self, event):
        QtWidgets.QPlainTextEdit.keyPressEvent(self, event)

    def focusInEvent(self, event):

        QtWidgets.QPlainTextEdit.focusInEvent(self, event)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = self.blockCount()
        while max_value >= 10:

            max_value /= 10
            digits += 1

        width = 3 + self.fontMetrics().width('9') * digits

        return width
    
    def updateLineNumberAreaWidth(self, _):

        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0,dy)
        else:
            self.lineNumberArea.update(rect.x(), rect.y(), self.lineNumberArea.width(), rect.height())
            self.lineNumberArea.setFixedWidth(self.lineNumberArea.width())


        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):

        super().resizeEvent(event)

        cr = self.contentsRect()

        self.lineNumberArea.setGeometry(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())

    def lineNumberAreaPaintEvent(self, event):

        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), QColor("transparent"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()

        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()

        while block.isValid() and (top <= event.rect().bottom()):

            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(QColor("#bfbfbf"))
                painter.drawText(-89, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()


            top = bottom

            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def zoom(self , angleDelta):
        if angleDelta.y()< 0:
            self.zoomOut(1)
        elif angleDelta.y() > 0:
            self.zoomIn(5)

    def wheelEvent(self, event):
        if (event.modifiers() & QtCore.Qt.ControlModifier):
            self.zoom(event.angleDelta())
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
        self.font_size = 18

        self.button_map = {}

        self.initLayout()
        self.initWidgets()
        self.initProblemScreen()
        self.initCodePage()

        self.actionZoomIn = QAction('Zoom In', self)
        self.actionZoomOut = QAction('Zoom Out', self)

        self.codeScreen1.addAction(self.actionZoomIn)
        self.codeScreen1.addAction(self.actionZoomOut)

        self.actionZoomIn.triggered.connect(self.action_ZoomIn)
        self.actionZoomOut.triggered.connect(self.action_ZoomOut)
        
        ###########################
        ##Adding Widgets To CodeScreen
        ###########################
        self.problem_btns_layout.addWidget(self.button_map["problem"])
        self.problem_btns_layout.addWidget(self.button_map["output"])
        self.problem_btns_layout.addWidget(self.button_map["status"])
        
        self.problem_layout.addWidget(self.problem_graphicsView)
        self.problemsLayout.addWidget(self.timeLabel , Qt.AlignTop)
        self.problemsLayout.addWidget(self.button_map["end_duel"])

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

    #initialize Layout
    def initLayout(self):
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

    #initialize widgets    
    def initWidgets(self):
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
    
    #initialize Problems Screen
    def initProblemScreen(self):
        ###########################################
        ##Problem Screen
        ###########################################
        self.button_map["problem"] = QPushButton("Problem")
        self.button_map["problem"].setFixedHeight(30)
        self.button_map["problem"].clicked.connect(self.problem_btn_clicked)
        self.button_map["problem"].setStyleSheet("""QPushButton{
            border:none;
            background-color:#595959;
        }
        QPushButton:hover{
            border-bottom:4px solid rgb(0,191,255);
        }""")

        self.button_map["output"] = QPushButton("Output")
        self.button_map["output"].setFixedHeight(30)
        self.button_map["output"].clicked.connect(self.output_btn_clicked)
        self.button_map["output"].setStyleSheet("""QPushButton{
            border:none;
            background-color:#595959;
        }
        QPushButton:hover{
            border-bottom:4px solid rgb(0,191,255);
        }""")

        self.button_map["status"] = QPushButton("Status")
        self.button_map["status"].setFixedHeight(30)
        self.button_map["status"].clicked.connect(self.status_btn_clicked)
        self.button_map["status"].setStyleSheet("""QPushButton{
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

        
        self.our_profile_photo_path = None

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

        self.button_map["end_duel"] = QPushButton("End Duel")
        self.button_map["end_duel"].setFixedHeight(30)
        self.button_map["end_duel"].setStyleSheet("""QPushButton{
            border:none;
            background-color:#595959;
        }
        QPushButton:hover{
            border-bottom:4px solid rgb(0,191,255);
        }""")

    #intialize Code Page
    def initCodePage(self):
        ####################################################
        ##CodeScreen
        ####################################################
        self.codeScreen1 = QCodeEdit()
        self.codeScreen1.setFixedHeight(500)
        self.codeScreen1.setStyleSheet("color:white;")
        self.highlight = syntax_pars.PythonHighlighter(self.codeScreen1.document())
        self.codeScreen1.show()

        self.codePrewiew = QCodeEdit()
        self.codePrewiew.setFixedHeight(100)
        self.codePrewiew.setStyleSheet("color:white;")
        self.highlighter = syntax_pars.PythonHighlighter(self.codePrewiew.document())
        self.codePrewiew.show()
    ############################################
    ##Functions
    ############################################
    def problem_btn_clicked(self):
        self.problems_stacked_widgets.setCurrentIndex(0)

    def output_btn_clicked(self):
        self.problems_stacked_widgets.setCurrentIndex(1)
    
    def status_btn_clicked(self):
        self.problems_stacked_widgets.setCurrentIndex(2)

    def action_ZoomOut(self):
        self.codeScreen1.zoom(-1)
    def action_ZoomIn(self):
        self.codeScreen1.zoom(+1)
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