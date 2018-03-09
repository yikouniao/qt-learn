# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fffirst.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.setupUi(self)
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(687, 638)
        Dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.openGLWidget = QtWidgets.QOpenGLWidget(self.tab_1)
        self.openGLWidget.setObjectName("openGLWidget")
        self.verticalLayout.addWidget(self.openGLWidget)
        self.choose_1 = QtWidgets.QPushButton(self.tab_1)
        self.choose_1.setObjectName("choose_1")
        self.verticalLayout.addWidget(self.choose_1)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.exit = QtWidgets.QPushButton(Dialog)
        self.exit.setObjectName("exit")
        self.horizontalLayout.addWidget(self.exit)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.exit.clicked.connect(Dialog.reject)
        self.choose_1.clicked.connect(Dialog.file_open)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "运动轨迹分析"))
        self.choose_1.setText(_translate("Dialog", "选择文件"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Dialog", "algorithm 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "algorithm 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "algorithm 3"))
        self.exit.setText(_translate("Dialog", "退出"))
    def file_open(self):

        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "C:/",
                                                          "All Files (*);;Text Files (*.txt)")
        print(fileName1, filetype)

