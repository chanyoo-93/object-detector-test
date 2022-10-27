import os, sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('StartWindow.ui')
form_class = uic.loadUiType(form)[0]

form_main = resource_path('MainWindow.ui')
form_mainwindow = uic.loadUiType(form_main)[0]

def init_project_dir():
    basic_dir : dict = {
        "cfg"    : "Config",
        "train"  : "Train",
        "test"   : "Test",
        "val"    : "Valid",
        "results": "Results"}
    return basic_dir

class StartWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def push_open_project(self):
        dir_name = QFileDialog.getExistingDirectory(self)
        in_dir_list = os.listdir(dir_name)
        print(in_dir_list)
        self.btn_main_to_second()

    def push_create_project(self):
        dir_name = QFileDialog.getExistingDirectory(self)
        basic_dir = init_project_dir()
        for name in basic_dir:
            os.mkdir(os.path.join(dir_name, basic_dir[name]))
        self.btn_main_to_second()

    def btn_main_to_second(self):
        self.hide()
        self.second = MainWindow()
        self.second.exec()
        self.show()

    def push_exit_program(self):
        self.close()


class MainWindow(QDialog, QWidget, form_mainwindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    def btn_second_to_main(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = StartWindow()
    myWindow.show()
    app.exec_()