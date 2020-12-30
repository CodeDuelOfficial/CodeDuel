#
#
###Updated By EmircanDemirci 02.10.2020
#
#
import PyQt5
from PyQt5 import QtWidgets , QtCore
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
import sys
import syntax_pars

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.textEdit = Editor(self)
        self.toolBar = QToolBar(self)
        self.actionZoomIn = QAction('Zoom In', self)
        self.actionZoomOut = QAction('Zoom Out', self)
        self.textEdit.setHtml('<font color=blue>Hello <b>world</b></font>')
        self.setCentralWidget(self.textEdit)
        self.addToolBar(self.toolBar)
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoomOut)
        self.actionZoomIn.triggered.connect(self.onZoomInClicked)
        self.actionZoomOut.triggered.connect(self.onZoomOutClicked)

    def onZoomInClicked(self):
        self.textEdit.zoom(+1)

    def onZoomOutClicked(self):
        self.textEdit.zoom(-1)

class Editor(QTextEdit):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)

        self.zoomin = 1
        self.zoomout = -1

    def zoom(self , angleDelta):
        if angleDelta.y()< 0:
            self.zoomOut(1)
        elif angleDelta.y() > 0:
            self.zoomIn(5)

    def wheelEvent(self, event):
        if (event.modifiers() & QtCore.Qt.ControlModifier):
            self.zoom(event.angleDelta())

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()