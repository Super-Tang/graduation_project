import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, qApp
from PyQt5 import QtCore, QtWidgets, QtGui
from ui.colors import color_list
import ui.fonts as f


class Second_UI(object):
    def __init__(self):
        self.colors = color_list
        desktop = QApplication.desktop()
        self.height = desktop.height()
        self.width = desktop.width()
        self.max_table_column = 8
        self.max_table_row = 30
        self.text = [[('What is', 1), ('leadership?', 2)],
        [('什么是', 1), ('领导？', 2)],[('Leaders', 1), ('don’t force other people to', 2), (' go along with them.', 3)],
        [('领导者', 1), ('不强制别人',2), ('与自己协调一致', 3)]]


    def setup_ui(self, QMainWindow):
        QMainWindow.setObjectName('MainWindow')
        QMainWindow.setFixedSize(self.width, self.height)
        self.frame = QtWidgets.QFrame()
        self.frame.setGeometry(QtCore.QRect(0, 120, self.width, self.height - 50))
        QMainWindow.setCentralWidget(self.frame)
        self.second_window = QMainWindow
        self.table = QtWidgets.QTableWidget(self.frame)
        self.column_width = (self.width - 100) // self.max_table_column
        self.table.setColumnCount(self.max_table_column)
        self.table.setShowGrid(False)
        self.table.setFixedHeight(self.height - 50)
        # self.table.setColumnWidth(0, 50)
        self.table.setFixedWidth(self.width)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setFont(f.font1)
        for i in range(self.max_table_column - 1):
            self.table.setColumnWidth(i+1, self.column_width)
        self.add_content()

    def add_content(self):
        count = len(self.text)
        if count <= self.max_table_row:
            self.table.setRowCount(count)
            self.table.setColumnCount(self.max_table_column + 1)
            # self.table.setColumnWidth(0, 50)
            index = 0
            for sentence in self.text:
                # self.table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(index)))
                for i in range(len(sentence)):
                    item = QtWidgets.QTableWidgetItem(sentence[i][0])
                    item.setForeground(QtGui.QBrush(self.colors[sentence[i][1]]))
                    self.table.setItem(index, i, item)
                index += 1
        self.table.resizeRowsToContents()


class Window(QMainWindow, Second_UI):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setup_ui(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.showMaximized()
    sys.exit(app.exec_())


