import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from graph_simulacra.simulacra_ui import Ui_MainWindow
from graph_simulacra.graph_simulacra import input_matrix_from_file
from graph_simulacra.graph_simulacra import draw_graph


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.add_file)
        self.actionSave.triggered.connect(self.save_file)
        self.show()

    def add_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                        '/home',"Text files (*.txt)")
        matrix_array = input_matrix_from_file(fname[0])
        draw_graph(matrix_array)
        self.webView.load(QUrl("file:///tmp/testplot.png"))


    def save_file(self):
        print('save')


