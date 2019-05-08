import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from graph_simulacra.simulacra_ui import Ui_MainWindow
from graph_simulacra.graph_simulacra import input_matrix_from_file
from graph_simulacra.graph_simulacra import draw_graph
from graph_simulacra.graph_simulacra import draw_graph_native
import io
from PIL import Image



class MainWindow(QMainWindow, Ui_MainWindow):
    matrix_array = []
    web_image_path = ''
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setFixedSize(self.size());
        self.actionOpen.triggered.connect(self.add_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionRank.triggered.connect(self.gen_rank)
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.show()

    def add_file(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                '',"Text files (*.txt)")
            MainWindow.matrix_array = input_matrix_from_file(fname[0])
            draw_graph_native(MainWindow.matrix_array)
            MainWindow.web_image_path = '/tmp/testplot_native.png'
            self.webView.load(QUrl("file://"+MainWindow.web_image_path))
        except FileNotFoundError:
            print('Uknown File')


    def save_file(self):
        try:
            fname = QFileDialog.getSaveFileName(self, 'Save file',
                                                '')
            plot_image = Image.open(MainWindow.web_image_path)
            plot_image.save(fname[0])
        except ValueError:
            print('Uknown File')

    def gen_rank(self):
        try:
            draw_graph(MainWindow.matrix_array)
            MainWindow.web_image_path = '/tmp/testplot.png'
            self.webView.load(QUrl("file://"+MainWindow.web_image_path))
        except FileNotFoundError:
            print('Uknown File')

    def undo(self):
        MainWindow.web_image_path = '/tmp/testplot_native.png'
        self.webView.load(QUrl("file://"+MainWindow.web_image_path))

    def redo(self):
        MainWindow.web_image_path = '/tmp/testplot.png'
        self.webView.load(QUrl("file://"+MainWindow.web_image_path))
