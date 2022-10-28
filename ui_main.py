import os, sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import utils

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('MainWindow.ui')
form_class = uic.loadUiType(form)[0]

form_main = resource_path('SecondWindow.ui')
form_mainwindow = uic.loadUiType(form_main)[0]

def init_project_dir():
    base_dir : dict = {
        "cfg"    : "Config",
        "train"  : "TrainData",
        "test"   : "TestData",
        "val"    : "ValidData",
        "results": "Results"}
    return base_dir
base_dir = init_project_dir()

class MainWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def push_open_project(self):
        dir_name = QFileDialog.getExistingDirectory(self)

    def push_create_project(self):
        dir_name = QFileDialog.getExistingDirectory(self)
        for name in base_dir:
            os.mkdir(os.path.join(dir_name, base_dir[name]))

    def push_start_train(self):
        self.btn_main_to_second()

    def btn_main_to_second(self):
        self.hide()
        self.second = SecondWindow()
        self.second.exec()
        self.show()

    def push_exit_program(self):
        self.close()


class SecondWindow(QDialog, QWidget, form_mainwindow):

    def __init__(self):
        super(SecondWindow, self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    def btn_second_to_main(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()