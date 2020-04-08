import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QItemDelegate
from PyQt5 import QtCore, QtWidgets
from ui.colors import color_list1
import ui.fonts as f


class Second_UI(object):
    def __init__(self):
        self.initial = './'
        self.colors = color_list1
        desktop = QApplication.desktop()
        self.height = desktop.height()
        self.width = desktop.width()
        self.max_table_column = 10
        self.max_table_row = 15
        self.current_row = 0
        self.source_text = []
        self.target_text = []
        self.text = [[('Its', 0), ('qualities', 1), ('are difficult', 2), ('to', 3), ('define.', 4), ('But they are', 5), ('not so difficult', 6), ('to', -1), ('identity.', 5)], [('领导', 0), ('应具备', 2), ('什么样', -1), ('的素质', 1), (',这', 3), ('很难', 2), ('精确', -1), ('的解说', 4), (',', -1), ('但', 0), ('辨认直陈却也不', 5), ('难', 6)],
                     [('What', 0), ('is leadership?', 1)], [('什么是', 0), ('领导?', 1)],
                     [('Leaders', 0), ('don’t force', 1), ('other people', -1), ('to go along with', 2), ('them.', -1)],
                     [('领导者', 0), ('不强制', 1), ('别人与', -1), ('自己协调一致', 2), (',', -1), ('而是', -1), ('帮助他们', 1),
                      ('跟上', 2)],
                     [('They', 0), ('bring them along.', 1), ('Leaders', 0), ('get commitment', -1),
                      ('from others by', 2), ('giving', 3), ('it themselves,', 4), ('by building', 5),
                      ('an environment', 6), ('that encourages creativity, and by operating', 7), ('with honesty', 8),
                      ('and', -1), ('fairness.', 9)],
                     [('领导者', 0), ('让', -1), ('别人承担义务', 1), (',首先自己', 2), ('承担', 3), ('义务,', 4), ('造成', 5), ('一种', 6),
                      ('能鼓励创造', 7), ('的环境', 6), (',待人', 7), ('诚', 8), ('恳,', -1), ('处事公正。', 9)],
                     [('Its', 0), ('qualities', 1), ('are difficult', 2), ('to', 3), ('define.', 4),
                      ('But they are', 5), ('not so difficult', 6), ('to', -1), ('identity.', 5)],
                     [('领导', 0), ('应具备', 2), ('什么样', -1), ('的素质', 1), (',这', 3), ('很难', 2), ('精确', -1), ('的解说', 4),
                      (',', -1), ('但', 0), ('辨认直陈却也不', 5), ('难', 6)],
                     [('What', 0), ('is leadership?', 1)], [('什么是', 0), ('领导?', 1)],
                     [('Leaders', 0), ('don’t force', 1), ('other people', -1), ('to go along with', 2), ('them.', -1)],
                     [('领导者', 0), ('不强制', 1), ('别人与', -1), ('自己协调一致', 2), (',', -1), ('而是', -1), ('帮助他们', 1),
                      ('跟上', 2)],
                     [('They', 0), ('bring them along.', 1), ('Leaders', 0), ('get commitment', -1),
                      ('from others by', 2), ('giving', 3), ('it themselves,', 4), ('by building', 5),
                      ('an environment', 6), ('that encourages creativity, and by operating', 7), ('with honesty', 8),
                      ('and', -1), ('fairness.', 9)],
                     [('领导者', 0), ('让', -1), ('别人承担义务', 1), (',首先自己', 2), ('承担', 3), ('义务,', 4), ('造成', 5), ('一种', 6),
                      ('能鼓励创造', 7), ('的环境', 6), (',待人', 7), ('诚', 8), ('恳,', -1), ('处事公正。', 9)],
                     [('Its', 0), ('qualities', 1), ('are difficult', 2), ('to', 3), ('define.', 4),
                      ('But they are', 5), ('not so difficult', 6), ('to', -1), ('identity.', 5)],
                     [('领导', 0), ('应具备', 2), ('什么样', -1), ('的素质', 1), (',这', 3), ('很难', 2), ('精确', -1), ('的解说', 4),
                      (',', -1), ('但', 0), ('辨认直陈却也不', 5), ('难', 6)],
                     [('What', 0), ('is leadership?', 1)], [('什么是', 0), ('领导?', 1)],
                     [('Leaders', 0), ('don’t force', 1), ('other people', -1), ('to go along with', 2), ('them.', -1)],
                     [('领导者', 0), ('不强制', 1), ('别人与', -1), ('自己协调一致', 2), (',', -1), ('而是', -1), ('帮助他们', 1),
                      ('跟上', 2)],
                     [('They', 0), ('bring them along.', 1), ('Leaders', 0), ('get commitment', -1),
                      ('from others by', 2), ('giving', 3), ('it themselves,', 4), ('by building', 5),
                      ('an environment', 6), ('that encourages creativity, and by operating', 7), ('with honesty', 8),
                      ('and', -1), ('fairness.', 9)],
                     [('领导者', 0), ('让', -1), ('别人承担义务', 1), (',首先自己', 2), ('承担', 3), ('义务,', 4), ('造成', 5), ('一种', 6),
                      ('能鼓励创造', 7), ('的环境', 6), (',待人', 7), ('诚', 8), ('恳,', -1), ('处事公正。', 9)],
                     [('Its', 0), ('qualities', 1), ('are difficult', 2), ('to', 3), ('define.', 4),
                      ('But they are', 5), ('not so difficult', 6), ('to', -1), ('identity.', 5)],
                     [('领导', 0), ('应具备', 2), ('什么样', -1), ('的素质', 1), (',这', 3), ('很难', 2), ('精确', -1), ('的解说', 4),
                      (',', -1), ('但', 0), ('辨认直陈却也不', 5), ('难', 6)],
                     [('What', 0), ('is leadership?', 1)], [('什么是', 0), ('领导?', 1)],
                     [('Leaders', 0), ('don’t force', 1), ('other people', -1), ('to go along with', 2), ('them.', -1)],
                     [('领导者', 0), ('不强制', 1), ('别人与', -1), ('自己协调一致', 2), (',', -1), ('而是', -1), ('帮助他们', 1),
                      ('跟上', 2)],
                     [('They', 0), ('bring them along.', 1), ('Leaders', 0), ('get commitment', -1),
                      ('from others by', 2), ('giving', 3), ('it themselves,', 4), ('by building', 5),
                      ('an environment', 6), ('that encourages creativity, and by operating', 7), ('with honesty', 8),
                      ('and', -1), ('fairness.', 9)],
                     [('领导者', 0), ('让', -1), ('别人承担义务', 1), (',首先自己', 2), ('承担', 3), ('义务,', 4), ('造成', 5), ('一种', 6),
                      ('能鼓励创造', 7), ('的环境', 6), (',待人', 7), ('诚', 8), ('恳,', -1), ('处事公正。', 9)],
                     [('What', 0), ('is leadership?', 1)], [('什么是', 0), ('领导?', 1)],
                     [('Leaders', 0), ('don’t force', 1), ('other people', -1), ('to go along with', 2), ('them.', -1)],
                     [('领导者', 0), ('不强制', 1), ('别人与', -1), ('自己协调一致', 2), (',', -1), ('而是', -1), ('帮助他们', 1),
                      ('跟上', 2)],
                     [('They', 0), ('bring them along.', 1), ('Leaders', 0), ('get commitment', -1),
                      ('from others by', 2), ('giving', 3), ('it themselves,', 4), ('by building', 5),
                      ('an environment', 6), ('that encourages creativity, and by operating', 7), ('with honesty', 8),
                      ('and', -1), ('fairness.', 9)],
                     [('领导者', 0), ('让', -1), ('别人承担义务', 1), (',首先自己', 2), ('承担', 3), ('义务,', 4), ('造成', 5), ('一种', 6),
                      ('能鼓励创造', 7), ('的环境', 6), (',待人', 7), ('诚', 8), ('恳,', -1), ('处事公正。', 9)]
                     ]

    def setup_ui(self, QMainWindow, text):
        if text is not None:
            self.text = text
        index = 0
        for line in self.text:
            if index % 2 == 0:
                print(line)
                self.source_text.append(line)
            else:
                print(line)
                self.target_text.append(line)
            index += 1
        QMainWindow.setObjectName('MainWindow')
        QMainWindow.setFixedSize(self.width, self.height)
        self.frame = QtWidgets.QFrame()
        self.frame.setGeometry(QtCore.QRect(0, 120, self.width, self.height - 50))
        self.frame.setStyleSheet('background-color:#E0E0E0')
        QMainWindow.setCentralWidget(self.frame)
        self.second_window = QMainWindow
        self.table = QtWidgets.QTableWidget(self.frame)
        self.column_width = self.width - 100
        self.table.setColumnCount(2)
        self.table.setShowGrid(False)
        self.table.setFixedHeight(self.height - 100)
        self.table.setMinimumWidth(self.width)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setFont(f.font)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, self.column_width)
        # for i in range(self.max_table_column):
        #     self.table.setColumnWidth(i+1, self.column_width + 100)
        self.add_content()
        self.add_button()
        self.second_window.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

    def add_sentence(self, row_index, sent):
        if row_index >= self.table.rowCount():
            self.table.insertRow(row_index)
        hlayout = QtWidgets.QHBoxLayout()
        width = 0
        j = 0
        for i in range(len(sent)):
            label = QtWidgets.QLabel()
            label.setFont(f.font2)
            label.setText(sent[i][0].strip() + ' ')
            label.setStyleSheet('QLabel{color:'+self.colors[(sent[i][1]+1) % self.max_table_row]+';}')
            label.adjustSize()
            width += label.width()
            if width < self.column_width - 180:
                j += 1
                hlayout.addWidget(label)
            else:
                j = 1
                width = 0
                widget = QtWidgets.QWidget()
                widget.setLayout(hlayout)
                self.table.setCellWidget(row_index, 1, widget)
                row_index += 1
                if row_index >= self.table.rowCount():
                    self.table.insertRow(row_index)
                hlayout = QtWidgets.QHBoxLayout()
                hlayout.addWidget(label)
        while j < 20:
            label = QtWidgets.QLabel()
            label.setFont(f.font1)
            label.setText('             ')
            j += 1
            hlayout.addWidget(label, alignment=QtCore.Qt.AlignLeft)
        # vlayout.addWidget(widget1)
        widget = QtWidgets.QWidget()
        widget.setLayout(hlayout)
        self.table.setCellWidget(row_index, 1, widget)
        row_index += 1
        return row_index

    def add_content(self):
        count = len(self.source_text) - self.current_row
        if count <= self.max_table_row:
            if count != self.table.rowCount():
                self.table.setRowCount(count)
            row_index = 0
            for i in range(count):
                if row_index >= self.table.rowCount():
                    self.table.insertRow(row_index)
                self.table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(i+self.current_row+1)))
                row_index = self.add_sentence(row_index, self.source_text[i + self.current_row])
                if row_index >= self.table.rowCount():
                    self.table.insertRow(row_index)
                row_index = self.add_sentence(row_index, self.target_text[i + self.current_row])
                if row_index >= self.table.rowCount():
                    self.table.insertRow(row_index)
                row_index += 1
        else:
            self.table.setRowCount(self.max_table_row)
            # self.table.setColumnCount(self.max_table_column + 1)
            self.table.setColumnWidth(0, 50)
            row_index = 0
            for i in range(self.max_table_row):
                if row_index >= self.table.rowCount():
                    self.table.insertRow(row_index)
                self.table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(i + self.current_row + 1)))
                row_index = self.add_sentence(row_index, self.source_text[i + self.current_row])
                if row_index >= self.table.rowCount():
                    self.table.insertRow(row_index)
                row_index = self.add_sentence(row_index, self.target_text[i + self.current_row])
                if row_index >= self.table.rowCount():
                    self.table.insertRow(row_index)
                row_index += 1
            self.current_row += self.max_table_row
        self.table.resizeRowsToContents()

    def add_button(self):
        left_button = QtWidgets.QPushButton(self.frame)
        left_button.setGeometry(QtCore.QRect(self.width // 2 - 150, self.height - 75, 50, 50))
        left_button.setVisible(True)
        left_button.setStyleSheet(
            "QPushButton{border-image: url(icon/left_arrow.png)}QPushButton:hover{background:#87CEFF;}")
        left_button.setToolTip("上一页")
        left_button.clicked.connect(self.prev_page)
        right_button = QtWidgets.QPushButton(self.frame)
        right_button.setGeometry(QtCore.QRect(self.width // 2 + 245, self.height - 75, 50, 50))
        right_button.setVisible(True)
        right_button.setStyleSheet(
            "QPushButton{border-image: url(icon/right_arrow.png)}QPushButton:hover{background:#87CEFF;}")
        right_button.setToolTip("下一页")
        right_button.clicked.connect(self.next_page)
        save_button = QtWidgets.QPushButton(self.frame)
        save_button.setGeometry(QtCore.QRect(self.width // 2 - 75, self.height - 75, 150, 50))
        save_button.setVisible(True)
        save_button.setStyleSheet('''QPushButton{border-radius:5px;color:black;}
                QPushButton:hover{background:#87CEFF;}
                QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}''')
        save_button.setText('保 存')
        save_button.setFont(f.font1)
        save_button.clicked.connect(self.save)
        return_button = QtWidgets.QPushButton(self.frame)
        return_button.setGeometry(QtCore.QRect(self.width // 2 + 75, self.height - 75, 150, 50))
        return_button.setVisible(True)
        return_button.setStyleSheet('''QPushButton{border-radius:5px;color:black;}
                        QPushButton:hover{background:#87CEFF;}
                        QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}''')
        return_button.setText('返 回')
        return_button.setFont(f.font1)
        return_button.clicked.connect(self.exit)

    def exit(self):
        self.second_window.close()

    def prev_page(self):
        index = int(self.table.item(0, 0).text()) - 1
        if index > 0:
            self.table.setRowCount(1)
            self.current_row = index - self.max_table_row
            self.add_content()

    def next_page(self):
        index = int(self.table.item(0, 0).text()) - 1
        if index + self.max_table_row < len(self.text):
            self.table.setRowCount(1)
            self.add_content()

    def save(self):
        fileName2, ok2 = QFileDialog.getSaveFileName(self, "文件保存", self.initial, "All Files (*);;Text Files (*.txt)")
        if len(fileName2) > 0:
            f = open(fileName2, 'w', encoding='utf-8')
            count = len(self.source_text)
            for i in range(count):
                source = self.source_text[i]
                target = self.target_text[i]
                # print(source)
                f.write('No. ' + str(i) + ':\n')
                for s in source:
                    f.write(s[0] + ': ' + str(s[1]) + '\t')
                f.write('\n')
                for t in target:
                    f.write(t[0] + ': ' + str(t[1]) + '\t')
                f.write('\n\n')
            f.close()
            self.second_window.close()


class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


class Window(QMainWindow, Second_UI):
    def __init__(self, text, parent=None):
        super(Window, self).__init__(parent)
        self.setup_ui(self, text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window(text=None)
    win.showMaximized()
    sys.exit(app.exec_())


