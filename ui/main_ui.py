import os
import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

import sentence_alignment.Chinese_Arabia as Chinese_Arabia
import sentence_alignment.Chinese_English as Chinese_English
import sentence_alignment.Chinese_French as Chinese_French
import sentence_alignment.Chinese_German as Chinese_German
import sentence_alignment.Chinese_Japan as Chinese_Japan
import sentence_alignment.Chinese_Korean as Chinese_Korean
import sentence_alignment.Chinese_Portugal as Chinese_Portugal
import sentence_alignment.Chinese_Russian as Chinese_Russian
import sentence_alignment.Chinese_Spain as Chinese_Spain
import sentence_alignment.Globals as Globals
import ui.error as error
import ui.fonts as f
from phrase_alignment.palm.toolkit.configure import PDConfig
from phrase_alignment.processfile import process_file
from phrase_alignment.word_alignment import phrase_extract
from ui.second_ui import Window
from ui.wait import WaitWindow

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
languages = {'中文': Globals.CHINESE, '日语': Globals.JAPAN, '英语': Globals.ENGLISH, '俄语': Globals.RUSSIAN,
             '法语': Globals.FRENCH, '德语': Globals.GERMAN, '韩语': Globals.KOREAN, '阿拉伯语': Globals.ARABIA,
             '葡萄牙语': Globals.PORTUGAL, '西班牙语': Globals.SPAIN}


class Main_UI(object):
    def __init__(self):
        self.initial = './'
        desktop = QApplication.desktop()
        self.height = desktop.height()
        self.width = desktop.width()
        self.source_file = None
        self.target_file = None
        self.source_text = None
        self.target_text = None
        self.source_count = 0
        self.target_count = 0
        self.current_source = 0
        self.current_target = 0
        self.save_source_sentence = []
        self.save_target_sentence = []
        self.is_merged = False
        self.button_show = False
        self.max_table_row = 30
        self.initial_flag = True
        self.aligned_phrase = None
        self.phrase_alignment = None

    def setupUi(self, QMainWindow, arg):
        self.args = arg
        self.timer = QTimer()
        self.timer.timeout.connect(self.extract)
        QMainWindow.setObjectName('MainWindow')
        QMainWindow.setFixedSize(self.width, self.height)
        self.add_status()
        self.frame = QtWidgets.QFrame()
        self.frame.setStyleSheet('background-color:#E0E0E0')
        self.frame.setGeometry(QtCore.QRect(0, 120, self.width, self.height - 50))
        QMainWindow.setCentralWidget(self.frame)
        self.set_frame()
        self.add_button()
        self.retranslateUi(QMainWindow)
        QtCore.QMetaObject.connectSlotsByName(QMainWindow)
        self.main_window = QMainWindow

    def set_frame(self):
        self.table = QtWidgets.QTableWidget(self.frame)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        self.table.setWordWrap(True)
        self.table.setColumnCount(3)
        self.table.setRowCount(1)
        self.table.setGeometry(QtCore.QRect(0, 0, self.width, 100))
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setColumnWidth(0, 100)
        self.table.setRowHeight(0, 100)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setStyleSheet("selection-background-color:yellow")
        width = (self.width - 132) // 2
        self.table.setColumnWidth(1, width)
        self.table.setColumnWidth(2, width)
        self.table.setStyleSheet("QTableWidget:item{border:4px black;}")
        item00 = QtWidgets.QTableWidgetItem(' No.')
        item00.setFont(f.font)
        self.table.setItem(0, 0, item00)
        hlayout = QtWidgets.QHBoxLayout()
        label1 = QtWidgets.QLabel('语言：')
        label1.setFont(f.font1)
        self.table.setFont(f.font2)
        self.source_lang = QtWidgets.QComboBox()
        self.source_lang.addItem(' 选择语言')
        self.source_lang.addItem('   日语')
        self.source_lang.addItem('   英语')
        self.source_lang.addItem('   俄语')
        self.source_lang.addItem('   法语')
        self.source_lang.addItem('   德语')
        self.source_lang.addItem('   韩语')
        self.source_lang.addItem('  西班牙语')
        self.source_lang.addItem('  葡萄牙语')
        self.source_lang.addItem('  阿拉伯语')
        self.source_lang.setFont(f.font1)
        self.source_lang.setFixedHeight(50)
        self.source_lang.setFixedWidth(250)
        self.source_lang.setStyleSheet("QComboBox{font-family:Microsoft YaHei;border:0px;border-color:black;"
                                  "background: #E3E3E3;font:24px;color:black;height: 20px;}")
        self.textedit = QtWidgets.QTextEdit('请输入文件名')
        self.textedit.setFont(f.font1)
        self.textedit.setFixedHeight(50)
        self.textedit.setFixedWidth(width - 600)
        button = QtWidgets.QPushButton()
        button.setFixedHeight(60)
        button.setFixedWidth(60)
        button.setStyleSheet("QPushButton{border-image: url(../icon/file.png)}")
        button.clicked.connect(self.open_source)
        hlayout.addWidget(label1, 0, QtCore.Qt.AlignCenter)
        hlayout.addWidget(self.source_lang, 1, QtCore.Qt.AlignLeft)
        hlayout.addWidget(self.textedit, 2, QtCore.Qt.AlignCenter)
        hlayout.addWidget(button, 3, QtCore.Qt.AlignLeft)
        widget = QtWidgets.QWidget()
        widget.setLayout(hlayout)
        self.table.setCellWidget(0, 1, widget)

        hlayout1 = QtWidgets.QHBoxLayout()
        label2 = QtWidgets.QLabel('语言：')
        label2.setFont(f.font1)
        target_lang = QtWidgets.QLabel('中文')
        target_lang.setFont(f.font1)
        target_lang.setFixedWidth(150)
        target_lang.setFixedHeight(50)
        self.textedit1 = QtWidgets.QTextEdit('请输入文件名')
        self.textedit1.setFont(f.font1)
        self.textedit1.setFixedHeight(50)
        self.textedit1.setFixedWidth(width - 600)
        button1 = QtWidgets.QPushButton()
        button1.setFixedHeight(60)
        button1.setFixedWidth(60)
        button1.setStyleSheet("QPushButton{border-image: url(../icon/file.png)}")
        button1.clicked.connect(self.open_target)
        hlayout1.addWidget(label2, 0, QtCore.Qt.AlignCenter)
        hlayout1.addWidget(target_lang, 1, QtCore.Qt.AlignLeft)
        hlayout1.addWidget(self.textedit1, 2, QtCore.Qt.AlignCenter)
        hlayout1.addWidget(button1, 3, QtCore.Qt.AlignLeft)
        widget = QtWidgets.QWidget()
        widget.setLayout(hlayout1)
        self.table.setCellWidget(0, 2, widget)

    def add_status(self):
        save_act = QtWidgets.QAction(QtGui.QIcon('../icon/save.png'), 'Save', self)
        save_act.setShortcut('Ctrl+S')
        save_act.setStatusTip('保存')
        place_act1 = QtWidgets.QAction("保存", self)
        align_act = QtWidgets.QAction(QtGui.QIcon('../icon/align.png'), 'Align', self)
        align_act.setShortcut('Ctrl+A')
        align_act.setStatusTip('对齐')
        place_act2 = QtWidgets.QAction("对齐", self)
        insert_act = QtWidgets.QAction(QtGui.QIcon("../icon/insert.png"), 'Insert', self)
        insert_act.setShortcut('Ctrl+I')
        place_act3 = QtWidgets.QAction('插入', self)
        delete_act = QtWidgets.QAction(QtGui.QIcon('../icon/delete.png'), 'Delete', self)
        delete_act.setShortcut('Ctrl+D')
        place_act4 = QtWidgets.QAction('删除', self)
        up_act = QtWidgets.QAction(QtGui.QIcon("../icon/up.png"), 'Up', self)
        up_act.setShortcut('Ctrl+U')
        place_act5 = QtWidgets.QAction('上移', self)
        down_act = QtWidgets.QAction(QtGui.QIcon('../icon/down.png'), 'Down', self)
        down_act.setShortcut('Ctrl+J')
        place_act6 = QtWidgets.QAction('下移', self)
        extract_act = QtWidgets.QAction(QtGui.QIcon('../icon/extract.jpg'), 'Extract', self)
        extract_act.setShortcut('Ctrl+E')
        place_act7 = QtWidgets.QAction('提取术语', self)
        exit_act = QtWidgets.QAction(QtGui.QIcon('../icon/exit.jpg'), 'Exit', self)
        exit_act.setShortcut('Ctrl+E')
        place_act8 = QtWidgets.QAction('退出', self)
        save_act.triggered.connect(self.save)
        place_act1.triggered.connect(self.save)
        align_act.triggered.connect(self.merge)
        place_act2.triggered.connect(self.merge)
        insert_act.triggered.connect(self.insert)
        place_act3.triggered.connect(self.insert)
        delete_act.triggered.connect(self.delete)
        place_act4.triggered.connect(self.delete)
        up_act.triggered.connect(self.up)
        place_act5.triggered.connect(self.up)
        down_act.triggered.connect(self.down)
        place_act6.triggered.connect(self.down)
        extract_act.triggered.connect(self.extract)
        place_act7.triggered.connect(self.extract)
        exit_act.triggered.connect(self.exit)
        place_act8.triggered.connect(self.exit)
        self.toolbar = self.addToolBar('Save')
        self.toolbar.addAction(save_act)
        self.toolbar.addAction(place_act1)
        self.toolbar.addAction(align_act)
        self.toolbar.addAction(place_act2)
        self.toolbar.addAction(insert_act)
        self.toolbar.addAction(place_act3)
        self.toolbar.addAction(delete_act)
        self.toolbar.addAction(place_act4)
        self.toolbar.addAction(up_act)
        self.toolbar.addAction(place_act5)
        self.toolbar.addAction(down_act)
        self.toolbar.addAction(place_act6)
        self.toolbar.addAction(extract_act)
        self.toolbar.addAction(place_act7)
        self.toolbar.addAction(exit_act)
        self.toolbar.addAction(place_act8)

    def exit(self):
        sys.exit(app.exec_())

    def save(self):
        fileName2, ok = QFileDialog.getSaveFileName(self, "文件保存", self.initial, "All Files (*);;Text Files (*.txt)")
        if len(fileName2) > 0 and self.is_merged:
            for i in range(self.table.rowCount() - 1):
                index = int(self.table.item(i + 1, 0).text()) - 1
                self.save_source_sentence[index] = str(self.table.item(i + 1, 1).text())
                self.save_target_sentence[index] = str(self.table.item(i + 1, 2).text())
            f = open(fileName2, 'w', encoding='gbk')
            for i in range(len(self.save_source_sentence)):
                f.write(self.save_source_sentence[i].strip() + '\n')
                f.write(self.save_target_sentence[i].strip() + '\n')
            f.close()
        else:
            self.errors = error.ErrorWindow("请按照正确操作使用")
            self.errors.show()

    def open_source(self):
        self.open(1)

    def open_target(self):
        self.open(2)

    def fill_table(self, is_source, is_list=False):
        self.table.setGeometry(QtCore.QRect(0, 0, self.width, self.height-150))
        self.table.setStyleSheet("QWidget:hover{background-color:rgb(223,223,223);}")
        if self.initial_flag:
            self.current_source = self.current_target = 0
        if is_list:
            if len(self.save_source_sentence) > 0:
                self.source_count = self.target_count = len(self.save_source_sentence)
                count = self.source_count - self.current_source
                if count <= self.max_table_row:
                    if self.table.rowCount() != count:
                        self.table.setRowCount(count+1)
                    for i in range(count):
                        if i + self.current_source < self.source_count:
                            self.table.setItem(i+1, 0, QtWidgets.QTableWidgetItem(" " + str(i + 1 + self.current_source)))
                            self.table.setItem(i+1, 1, QtWidgets.QTableWidgetItem(self.save_source_sentence[i+self.current_source].strip()))
                            self.table.setItem(i+1, 2, QtWidgets.QTableWidgetItem(self.save_target_sentence[i+self.current_source].strip()))
                else:
                    if self.table.rowCount() <= self.max_table_row:
                        self.table.setRowCount(self.max_table_row+1)
                    for i in range(self.max_table_row):
                        if i + self.current_source < self.source_count:
                            self.table.setItem(i+1, 0, QtWidgets.QTableWidgetItem(" " + str(i + 1 + self.current_source)))
                            self.table.setItem(i+1, 1, QtWidgets.QTableWidgetItem(self.save_source_sentence[i+self.current_source].strip()))
                            self.table.setItem(i+1, 2, QtWidgets.QTableWidgetItem(self.save_target_sentence[i+self.current_target].strip()))
                    self.current_source += self.max_table_row
                    self.current_target += self.max_table_row
            else:
                self.errors = error.ErrorWindow("请按照正确操作使用")
                self.errors.show()
        else:
            if is_source:
                sentence = self.source_text
                count = self.source_count = len(sentence)
                if self.source_count < self.target_count:
                    count = self.target_count
                count -= self.current_source
            else:
                sentence = self.target_text
                count = self.target_count = len(sentence)
                if self.target_count < self.source_count:
                    count = self.source_count
                count -= self.current_target
            if count <= self.max_table_row:
                if self.table.rowCount() != count:
                    self.table.setRowCount(count+1)
                if is_source:
                    # print(self.current_source)
                    for i in range(count):
                        if i + self.current_source < self.source_count:
                            self.table.setItem(i+1, 0, QtWidgets.QTableWidgetItem(" " + str(i + 1 + self.current_source)))
                            # print(sentence[i+self.current_source])
                            self.table.setItem(i+1, 1, QtWidgets.QTableWidgetItem(sentence[i+self.current_source].strip()))
                        else:
                            self.table.setItem(i + 1, 1, QtWidgets.QTableWidgetItem(""))
                else:
                    for i in range(count):
                        if i + self.current_target < self.target_count:
                            self.table.setItem(i+1, 0, QtWidgets.QTableWidgetItem(" " + str(i + 1 + self.current_target)))
                            self.table.setItem(i+1, 2, QtWidgets.QTableWidgetItem(sentence[i+self.current_target].strip()))
                        else:
                            self.table.setItem(i + 1, 2, QtWidgets.QTableWidgetItem(""))
            else:
                if self.table.rowCount() <= self.max_table_row:
                    self.table.setRowCount(self.max_table_row+1)
                if is_source:
                    index = 0
                    for i in range(self.max_table_row):
                        if i + self.current_source < self.source_count:
                            index += 1
                            self.table.setItem(i+1, 0, QtWidgets.QTableWidgetItem(" " + str(1 + i + self.current_source)))
                            self.table.setItem(i+1, 1, QtWidgets.QTableWidgetItem(sentence[i+self.current_source].strip()))
                        else:
                            self.table.setItem(i + 1, 1, QtWidgets.QTableWidgetItem(""))
                    self.current_source += index
                else:
                    index = 0
                    for i in range(self.max_table_row):
                        if i + self.current_target < self.target_count:
                            index += 1
                            self.table.setItem(i + 1, 0, QtWidgets.QTableWidgetItem(" " + str(1 + i + self.current_target)))
                            self.table.setItem(i+1, 2, QtWidgets.QTableWidgetItem(sentence[i + self.current_target].strip()))
                        else:
                            self.table.setItem(i + 1, 2, QtWidgets.QTableWidgetItem(""))
                    self.current_target += index
        # print('current_source', self.current_source)
        # print('current_target', self.current_target)
        self.table.resizeRowsToContents()
        if not self.button_show :
            self.add_button()

    def add_button(self):
        if self.table.rowCount() > 1:
            self.merge_button1 = QtWidgets.QPushButton(self.frame)
            self.merge_button1.setText("文档对齐")
            self.merge_button1.setFont(f.font1)
            self.merge_button1.setGeometry(QtCore.QRect(self.width // 2 - 120, self.height - 150, 150, 80))
            self.merge_button1.clicked.connect(self.merge)
            self.merge_button1.setStyleSheet('''QPushButton{border-radius:5px;color:black;}
                QPushButton:hover{background:#87CEFF;}
                QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}''')
            self.merge_button1.setVisible(True)
            self.save_button1 = QtWidgets.QPushButton(self.frame)
            self.save_button1.setText('保存文件')
            self.save_button1.setFont(f.font1)
            self.save_button1.setGeometry(QtCore.QRect(self.width // 2 + 70, self.height - 150, 150, 80))
            self.save_button1.clicked.connect(self.save)
            self.save_button1.setVisible(True)
            self.save_button1.setStyleSheet('''QPushButton{border-radius:5px;color:black;}
                QPushButton:hover{background:#87CEFF;}
                QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}''')
            self.button_show = True
            left_button = QtWidgets.QPushButton(self.frame)
            left_button.setGeometry(QtCore.QRect(self.width // 2 - 210, self.height - 135, 50, 50))
            left_button.setVisible(True)
            left_button.setStyleSheet("QPushButton{border-image: url(../icon/left_arrow.png)}QPushButton:hover{background:#87CEFF;}")
            left_button.setToolTip("上一页")
            left_button.clicked.connect(self.prev_page)
            right_button = QtWidgets.QPushButton(self.frame)
            right_button.setGeometry(QtCore.QRect(self.width // 2 + 250, self.height - 135, 50, 50))
            right_button.setVisible(True)
            right_button.setStyleSheet("QPushButton{border-image: url(../icon/right_arrow.png)}QPushButton:hover{background:#87CEFF;}")
            right_button.setToolTip("下一页")
            right_button.clicked.connect(self.next_page)

    def prev_page(self):
        index = int(self.table.item(1, 0).text()) - 1
        if self.is_merged:
            if index == 0:
                self.current_source = self.current_target = 0
            else:
                self.current_source = self.current_target = index - self.max_table_row
            self.fill_table(False, True)
        else:
            if self.source_text is not None:
                if index == 0:
                    self.current_source = 0
                else:
                    self.current_source = index - self.max_table_row
                self.fill_table(True)
            if self.target_text is not None:
                if index == 0:
                    self.current_target = 0
                else:
                    self.current_target = index - self.max_table_row
                self.fill_table(False)
        self.save_current_text()

    def next_page(self):
        if self.is_merged:
            self.fill_table(False, True)
        else:
            if self.source_text is not None:
                self.fill_table(True)
            if self.target_text is not None:
                self.fill_table(False)
        self.save_current_text()

    def save_current_text(self):
        if self.is_merged:
            for i in range(self.table.rowCount() - 1):
                index = int(self.table.item(i + 1, 0).text()) - 1
                self.save_source_sentence[index] = str(self.table.item(i + 1, 1).text())
                self.save_target_sentence[index] = str(self.table.item(i + 1, 2).text())
        else:
            if self.source_text is not None:
                for i in range(self.table.rowCount() - 1):
                    index = int(self.table.item(i + 1, 0).text()) - 1
                    self.source_text[index] = str(self.table.item(i + 1, 1).text())
            if self.target_text is not None:
                for i in range(self.table.rowCount() - 1):
                    index = int(self.table.item(i + 1, 0).text()) - 1
                    self.target_text[index] = str(self.table.item(i + 1, 2).text())

    def open(self, no):
        if no == 1:
            path = self.textedit.toPlainText()
            if path == '请输入文件名' or not os.path.exists(path):
                file, _ = QFileDialog.getOpenFileName(self, 'select file', self.initial, "All Files (*);;Text Files (*.txt)")
                if len(file) > 0:
                    self.source_file = file
                    file_text = file.split('/')[-1]
                    self.initial = file[0: len(file)-len(file_text)]
                    self.textedit.setText(file_text)
                    self.source_text = self.open_file(self.source_file)
            else:
                self.source_file = path
                self.source_text = self.open_file(self.source_file)
            self.fill_table(True)
            self.initial_flag = False
        else:
            path = self.textedit1.toPlainText()
            if path == '请输入文件名' or not os.path.exists(path):
                file, _ = QFileDialog.getOpenFileName(self, 'select file', self.initial, "All Files (*);;Text Files (*.txt)")
                if len(file) > 0:
                    self.target_file = file
                    file_text = file.split('/')[-1]
                    self.initial = file[0: len(file)-len(file_text)]
                    self.textedit1.setText(file_text)
                    self.target_text = self.open_file(self.target_file, 0)
            else:
                self.target_file = path
                self.target_text = self.open_file(self.target_file, 0)
            self.fill_table(False)
            self.initial_flag = False

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

    def merge(self):
        source_language = -1
        text = self.source_lang.currentText().strip()
        if text in languages.keys():
            source_language = languages[text]
        if source_language >= 0:
            save_content = None
            if len(self.source_text) > 0 and len(self.target_text) > 0:
                source_text = '\n'.join(self.source_text)
                target_text = '\n'.join(self.target_text)
                if source_language == Globals.ENGLISH:
                    self.args.init_from_params = self.args.en_init_from_params
                    self.args.src_vocab_fpath = self.args.en_src_vocab_fpath
                    self.args.trg_vocab_fpath = self.args.en_trg_vocab_fpath
                    self.args.bpe_model_dir = self.args.en_bpe_model_dir
                    save_content = Chinese_English.pip_line(source_text, target_text, False)
                elif source_language == Globals.FRENCH:
                    self.args.init_from_params = self.args.fr_init_from_params
                    self.args.src_vocab_fpath = self.args.fr_src_vocab_fpath
                    self.args.trg_vocab_fpath = self.args.fr_trg_vocab_fpath
                    self.args.bpe_model_dir = self.args.fr_bpe_model_dir
                    save_content = Chinese_French.pip_line(source_text, target_text, False)
                elif source_language == Globals.GERMAN:
                    self.args.init_from_params = self.args.de_init_from_params
                    self.args.src_vocab_fpath = self.args.de_src_vocab_fpath
                    self.args.trg_vocab_fpath = self.args.de_trg_vocab_fpath
                    self.args.bpe_model_dir = self.args.de_bpe_model_dir
                    save_content = Chinese_German.pip_line(source_text, target_text, False)
                elif source_language == Globals.RUSSIAN:
                    self.args.init_from_params = self.args.ru_init_from_params
                    self.args.src_vocab_fpath = self.args.ru_src_vocab_fpath
                    self.args.trg_vocab_fpath = self.args.ru_trg_vocab_fpath
                    self.args.bpe_model_dir = self.args.ru_bpe_model_dir
                    save_content = Chinese_Russian.pip_line(source_text, target_text, False)
                elif source_language == Globals.JAPAN:
                    save_content = Chinese_Japan.pip_line(source_text, target_text, False)
                elif source_language == Globals.ARABIA:
                    save_content = Chinese_Arabia.pip_line(source_text, target_text, False)
                elif source_language == Globals.KOREAN:
                    save_content = Chinese_Korean.pip_line(source_text, target_text, False)
                elif source_language == Globals.SPAIN:
                    self.args.init_from_params = self.args.es_init_from_params
                    self.args.src_vocab_fpath = self.args.es_src_vocab_fpath
                    self.args.trg_vocab_fpath = self.args.es_trg_vocab_fpath
                    self.args.bpe_model_dir = self.args.es_bpe_model_dir
                    save_content = Chinese_Spain.pip_line(source_text, target_text, False)
                elif source_language == Globals.PORTUGAL:
                    save_content = Chinese_Portugal.pip_line(source_text, target_text, False)
            if save_content is not None:
                self.is_merged = True
                self.current_source = self.current_target = 0
                self.save_source_sentence = []
                self.save_target_sentence = []
                for para in save_content:
                    for i in range(len(para)//2):
                        self.save_source_sentence.append(para[2*i])
                        self.save_target_sentence.append(para[2*i+1])
            self.fill_table(False, True)
        elif self.source_text is None or self.target_text is None:
            self.errors = error.ErrorWindow("请选择文件")
            self.errors.show()
        elif source_language == -1:
            self.errors = error.ErrorWindow("请选择语言")
            self.errors.show()
        if self.phrase_alignment is None:
            self.phrase_alignment = phrase_extract(source_language, self.args)

    def insert(self):
        index = 0
        if len(self.table.selectedItems()) > 0:
            select_row = self.table.selectedItems()[0].row()
            if select_row > 0:
                index = int(self.table.item(select_row, 0).text()) - 1
        if self.is_merged:
            self.save_source_sentence.insert(index, '')
            self.save_target_sentence.insert(index, '')
            self.current_source = self.current_target = int(self.table.item(1, 0).text()) - 1
            self.fill_table(False, True)
        else:
            if self.source_text is not None and len(self.source_text) > 0:
                self.source_text.insert(index, '')
                self.current_source = int(self.table.item(1, 0).text()) - 1
                self.fill_table(True)
            if self.target_text is not None and len(self.target_text) > 0:
                self.target_text.insert(index, '')
                self.current_target = int(self.table.item(1, 0).text()) - 1
                self.fill_table(False)

    def delete(self):
        index = -1
        if len(self.table.selectedItems()) > 0:
            select_row = self.table.selectedItems()[0].row()
            if select_row > 0:
                index = int(self.table.item(select_row, 0).text()) - 1
        if index >= 0:
            if self.is_merged:
                self.save_source_sentence.remove(self.save_source_sentence[index])
                self.save_target_sentence.remove(self.save_target_sentence[index])
                self.current_source = self.current_target = int(self.table.item(1, 0).text()) - 1
                self.fill_table(False, True)
            else:
                if self.source_text is not None and len(self.source_text) > 0:
                    self.source_text.remove(self.source_text[index])
                    self.current_source = int(self.table.item(1, 0).text()) - 1
                    self.fill_table(True)
                if self.target_text is not None and len(self.target_text) > 0:
                    self.target_text.remove(self.target_text[index])
                    self.current_target = int(self.table.item(1, 0).text()) - 1
                    self.fill_table(False)
        else:
            self.errors = error.ErrorWindow("请选择需要删除的行")
            self.errors.show()

    def up(self):
        if len(self.table.selectedItems()) > 0:
            self.select_row = self.table.selectedItems()[0].row()
            if self.select_row > 0:
                index = int(self.table.item(self.select_row, 0).text())
            else:
                index = 1
            if index > 1:
                up_row = index - 1
                if self.is_merged:
                    index -= 1
                    up_row -= 1
                    select_source = self.save_source_sentence[index]
                    select_target = self.save_target_sentence[index]
                    up_source = self.save_source_sentence[up_row]
                    up_target = self.save_target_sentence[up_row]
                    self.save_source_sentence[index] = up_source
                    self.save_target_sentence[index] = up_target
                    self.save_source_sentence[up_row] = select_source
                    self.save_target_sentence[up_row] = select_target
                    self.prev_page()
                else:
                    if self.source_text is not None and len(self.source_text) > 0:
                        index1 = index - 1
                        up_row1 = up_row - 1
                        up_source = self.source_text[up_row1]
                        select_source = self.source_text[index1]
                        self.source_text[index1] = up_source
                        self.source_text[up_row1] = select_source
                        self.prev_page()
                    if self.target_text is not None and len(self.target_text) > 0:
                        index1 = index - 1
                        up_row1 = up_row - 1
                        select_target = self.target_text[index1]
                        up_target = self.target_text[up_row1]
                        self.target_text[index1] = up_target
                        self.target_text[up_row1] = select_target
                        self.prev_page()

    def down(self):
        if len(self.table.selectedItems()) > 0:
            self.select_row = self.table.selectedItems()[0].row()
            if self.is_merged:
                if self.select_row > 0:
                    index = int(self.table.item(self.select_row, 0).text())
                else:
                    index = self.source_count
                if index < self.source_count - 1:
                    down_row = index + 1
                    index -= 1
                    down_row -= 1
                    select_source = self.save_source_sentence[index]
                    select_target = self.save_target_sentence[index]
                    down_source = self.save_source_sentence[down_row]
                    down_target = self.save_target_sentence[down_row]
                    self.save_source_sentence[down_row] = select_source
                    self.save_target_sentence[down_row] = select_target
                    self.save_source_sentence[index] = down_source
                    self.save_target_sentence[index] = down_target
                    self.prev_page()
            else:
                if self.source_text is not None and len(self.source_text) > 0:
                    if self.select_row > 0:
                        index = int(self.table.item(self.select_row, 0).text())
                    else:
                        index = self.source_count
                    if index <= self.source_count - 1:
                        down_row1 = index
                        index1 = index - 1
                        select_source = self.source_text[index1]
                        down_source = self.source_text[down_row1]
                        self.source_text[index1] = down_source
                        self.source_text[down_row1] = select_source
                        self.prev_page()
                if self.target_text is not None and len(self.target_text) > 0:
                    if self.select_row > 0:
                        index = int(self.table.item(self.select_row, 0).text())
                    else:
                        index = self.target_count
                    if index <= self.target_count - 1:
                        down_row1 = index
                        index1 = index - 1
                        select_target = self.target_text[index1]
                        down_target = self.target_text[down_row1]
                        self.target_text[index1] = down_target
                        self.target_text[down_row1] = select_target
                        self.prev_page()

    def extract(self):
        self.timer.start(1000)
        if not self.is_merged:
            self.errors = error.ErrorWindow("请先进行句子对齐操作")
            self.errors.show()
        else:
            source_language = -1
            text = self.source_lang.currentText().strip()
            if text in languages.keys():
                source_language = languages[text]
            if self.aligned_phrase is None:
                if source_language >= 0:
                    self.save_current_text()
                    process_file(self.save_source_sentence, self.save_target_sentence, source_language, self.args)
                    self.main_window.statusBar().showMessage('Processing, please wait!')
                    if not self.phrase_alignment.started:
                        self.process_window = None
                        self.phrase_alignment.start()
                        self.aligned_phrase = self.phrase_alignment.values
                        self.process_window = WaitWindow()
                        self.process_window.show()
                    else:
                        if self.process_window is None:
                            self.process_window = WaitWindow()
                            self.process_window.show()
            if len(self.aligned_phrase) > 0:
                self.timer.stop()
                if self.process_window:
                    self.process_window.close()
                self.main_window.statusBar().showMessage('Process finished!')
                win = Window(text=self.aligned_phrase)
                win.showMaximized()

    def retranslateUi(self, QMainWindow):
        QMainWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint)


class ParentWindow(QMainWindow, Main_UI):
    def __init__(self, arg, parent=None):
        super(ParentWindow, self).__init__(parent)
        self.setupUi(self, arg)


def default(args):
    args.enable_ce = False
    args.weight_sharing = True
    args.postprocess_cmd = "da"
    args.preprocess_cmd = "n"
    args.relu_dropout = 0.1
    args.attention_dropout = 0.1
    args.prepostprocess_dropout = 0.1
    args.n_layer = 6
    args.n_head = 8
    args.d_value = 64
    args.d_key = 64
    args.d_inner_hid = 2048
    args.d_model = 512
    args.max_length = 256
    args.pad_idx = 3
    args.unk_idx = 2
    args.eos_idx = 1
    args.bos_idx = 0
    args.trg_vocab_size = 20000
    args.src_vocab_size = 20000
    args.n_best = 1
    args.max_out_len = 257
    args.beam_size = 5
    args.label_smooth_eps = 0.1
    args.warmup_steps = 8000
    args.eps = 1e-9
    args.beta2 = 0.997
    args.beta1 = 0.9
    args.learning_rate = 2.0
    args.batch_size = 1
    args.shuffle_batch = True
    args.shuffle = True
    args.sort_type = "pool"
    args.pool_size = 200000
    args.use_token_batch = True
    args.token_delimiter = " "
    args.special_token = ["<s>", "<e>", "<unk>"]
    args.use_cuda = False
    return args


if __name__ == "__main__":
    args = PDConfig(yaml_file="../phrase_alignment/transformer.yaml")
    args.build()
    args = default(args)
    app = QApplication(sys.argv)
    win = ParentWindow(args)
    win.showMaximized()
    sys.exit(app.exec_())
