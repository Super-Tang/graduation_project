import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

import ui.fonts as f


class Open_file(object):
    def __init__(self):
        self.text = None
        self.initial = './'
        self.file_name = None
        self.finished = False

    def setup_ui(self, QMainWindow):
        QMainWindow.setObjectName('MainWindow')
        QMainWindow.setFixedSize(900, 1200)
        self.frame = QtWidgets.QFrame()
        self.frame.setGeometry(QtCore.QRect(0, 0, 900, 1200))
        self.frame.setStyleSheet('background-color:#E0E0E0')
        QMainWindow.setCentralWidget(self.frame)
        QMainWindow.setWindowTitle('Text-Aligner')
        self.textarea = QtWidgets.QPlainTextEdit(self.frame)
        self.textarea.setGeometry(QtCore.QRect(10, 20, 880, 1080))
        self.open_button = QtWidgets.QPushButton(self.frame)
        self.open_button.setText('从文件导入')
        self.ok_button = QtWidgets.QPushButton(self.frame)
        self.ok_button.setText('确定')
        self.open_button.setGeometry(QtCore.QRect(10, 1110, 440, 80))
        self.open_button.setFont(f.font2)
        self.ok_button.setFont(f.font2)
        self.ok_button.setGeometry(QtCore.QRect(460, 1110, 430, 80))
        self.open_button.setStyleSheet('''QPushButton{border-radius:5px;color:black;}
                QPushButton:hover{background:#87CEFF;}
                QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}''')
        self.ok_button.setStyleSheet('''QPushButton{border-radius:5px;color:black;}
                QPushButton:hover{background:#87CEFF;}
                QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}''')
        self.open_button.clicked.connect(self.open)
        self.ok_button.clicked.connect(self.set_content)

    def open_file(self, file_name, count=0):
        try:
            if count == 0:
                f = open(file_name, 'r', encoding='EUC-KR')
            elif count == 1:
                f = open(file_name, 'r', encoding='EUC-JP')
            elif count == 2:
                f = open(file_name, 'r', encoding='utf-8')
            elif count == 3:
                f = open(file_name, 'r', encoding='gbk')
            else:
                return None
            text = []
            for line in f:
                text.append(line.strip())
            f.close()
            return text
        except:
            count += 1
            return self.open_file(file_name, count)

    def open(self):
        file, _ = QFileDialog.getOpenFileName(self, 'select file', self.initial,
                                        "All Files (*);;Text Files (*.txt)")
        if len(file) > 0:
            self.file_name = file.split('/')[-1]
            self.initial = file[0: len(file) - len(self.file_name)]
            self.text = self.open_file(file)
            show_text = ""
            for s in self.text:
                show_text += (s + '\n')
            self.textarea.setPlainText(show_text)

    def set_content(self):
        if len(self.textarea.toPlainText()) > 0:
            text = self.textarea.toPlainText().split('\n')
            self.text = [s for s in text if len(s) > 0]
            # print(self.text)
            if self.file_name is None:
                self.file_name = ''
        self.finished = True


class File_Window(QMainWindow, Open_file):
    def __init__(self, parent=None):
        super(File_Window, self).__init__(parent)
        self.setup_ui(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = File_Window()
    win.show()
    sys.exit(app.exec_())
