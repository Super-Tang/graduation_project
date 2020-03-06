from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog


class Third_Window(object):
    def setupUi(self, Dialog, message):
        Dialog.setObjectName('Dialog')
        Dialog.resize(300, 200)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 260, 110))
        self.label.setStyleSheet("color:red")
        self.label.setText('Error！ \n' + message)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate('Dialog', "Error"))


class ErrorWindow(QDialog, Third_Window):
    def __init__(self, message, parent=None):
        super(ErrorWindow, self).__init__(parent)
        self.setupUi(self, message)

