import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from graph_simulacra.simulacra_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.add_file)
        self.actionSave.triggered.connect(self.save_file)
        self.show()

    def add_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                        '/home',"Image files (*.jpg *.gif)")
        print(fname)


    def save_file(self):
        print('save')


