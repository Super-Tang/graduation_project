import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.fonts import *


class About_UI(object):
    def __init__(self):
        self.win = None

    def setup_ui(self, QMainWindow):
        QMainWindow.setWindowTitle('About')
        QMainWindow.resize(1200, 900)
        label = QtWidgets.QLabel(QMainWindow)
       # label.setGeometry(QtCore.QRect(10,0, 400, 40))
        label.setText('使用说明')
        # label.setWordWrap(True)
        label.setFont(font4)
        label.adjustSize()
        print(label.width())
        # label.setFont(font4)
        label1 = QtWidgets.QLabel(QMainWindow)
        label1.setFont(font2)
        label1.setGeometry(QtCore.QRect(30, 50, 800, 500))
        label1.setText('''
        1. 修改cof.yaml文件中的配置参数
        ''')


class About_win(QMainWindow, About_UI):
    def __init__(self, parent=None):
        super(About_win, self).__init__(parent)
        self.setup_ui(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = About_win()
    win.show()
    sys.exit(app.exec_())
