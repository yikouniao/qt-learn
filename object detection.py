# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hellow.py'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5.QtWidgets import QApplication,QMainWindow

from gui import *


if __name__ == '__main__':
    '''
    主函数
    '''

    app = QApplication(sys.argv)
    mainWindow = Ui_MainWindow()


    mainWindow.show()
    sys.exit(app.exec_())
