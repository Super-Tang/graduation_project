from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog


class Fourth_Window(object):
    def setupUi(self, Dialog):
        Dialog.resize(300, 200)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 260, 110))
        self.label.setStyleSheet("color:blue")
        self.label.setText('Processing, please wait!')
        QtCore.QMetaObject.connectSlotsByName(Dialog)


class WaitWindow(QDialog, Fourth_Window):
    def __init__(self, parent=None):
        super(WaitWindow, self).__init__(parent)
        self.setupUi(self)