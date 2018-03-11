# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'v101.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject,pyqtSignal

'''import qrc_resource'''


#主窗口
class Ui_MainWindow(QtWidgets.QMainWindow):
    #初始化
    def __init__(self):
        super(Ui_MainWindow, self).__init__()#继承自Widgets的构造方法
        self.setupUi(self)
    #主窗口的各项配置
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")#窗口名字
        MainWindow.resize(1012, 746)#窗口初始大小
        icon = QtGui.QIcon()#交大校徽
        icon.addPixmap(QtGui.QPixmap(":/res/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)#这个是主窗口的图标,没有弄
        MainWindow.setAutoFillBackground(False)#字面意思
        MainWindow.setStyleSheet("")#主窗口样式表，还没学会怎么写css，下次
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)


        self.centralwidget = QtWidgets.QWidget(MainWindow)#主窗口的widgets
        self.centralwidget.setObjectName("centralwidget")#对象名字
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)#主窗口widgets的布局，垂直
        self.verticalLayout_2.setObjectName("verticalLayout_2")#布局的名字

        self.frame = QtWidgets.QFrame(self.centralwidget)#QFrame对象，下面都是些设置
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")#名字
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)#frame的布局，水平
        self.horizontalLayout.setObjectName("horizontalLayout")#名字


        self.label_jiaoda = QtWidgets.QLabel(self.frame)#label，用来显示交大校徽
        self.label_jiaoda.setEnabled(True)


        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)#拉伸
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_jiaoda.sizePolicy().hasHeightForWidth())


        self.label_jiaoda.setSizePolicy(sizePolicy)#label的sizepolicy，下面都事label的设置
        self.label_jiaoda.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.label_jiaoda.setAcceptDrops(False)
        self.label_jiaoda.setText("")
        self.label_jiaoda.setTextFormat(QtCore.Qt.AutoText)
        self.label_jiaoda.setPixmap(QtGui.QPixmap(":/res/icon.png"))#交大校徽
        self.label_jiaoda.setScaledContents(True)#下面都是设置
        self.label_jiaoda.setWordWrap(False)
        self.label_jiaoda.setIndent(-1)
        self.label_jiaoda.setOpenExternalLinks(False)
        self.label_jiaoda.setObjectName("label_jiaoda")#布局
        self.horizontalLayout.addWidget(self.label_jiaoda)
        self.verticalLayout_2.addWidget(self.frame)


        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)#tabwidget准备用来实现三个算法的切换，
                                                                 #还不清楚可不可以这么搞
        self.tabWidget.setObjectName("tabWidget")#一些配置
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_image = QtWidgets.QLabel(self.tab_1)#嗯，这个label准备用来显示第一个算法的图片
        self.label_image.setObjectName("label_image")


        self.verticalLayout.addWidget(self.label_image)

        self.label_jiaoda.raise_()#栈排序
        self.label_image.raise_()


        self.tabWidget.addTab(self.tab_1, "")#2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")


        self.tab_3 = QtWidgets.QWidget()#3
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_2.addWidget(self.tabWidget)#2布局下的Tabwidget
        MainWindow.setCentralWidget(self.centralwidget)#把之前那个centralwidget加到主窗口

        self.menubar = QtWidgets.QMenuBar(MainWindow)#菜单
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1012, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionChoose_txt = QtWidgets.QAction(MainWindow)#选择文本文件的action
        self.actionChoose_txt.setObjectName("actionChoose_txt")
        self.actionChoose_video = QtWidgets.QAction(MainWindow)#选择视频文件的action
        self.actionChoose_video.setObjectName("actionChoose_video")
        self.actionbegin = QtWidgets.QAction(MainWindow)#运行的action
        self.actionbegin.setObjectName("actionbegin")

        self.menu.addAction(self.actionChoose_txt)#加到菜单上面去
        self.menu.addAction(self.actionChoose_video)
        self.menu.addSeparator()
        self.menu.addAction(self.actionbegin)
        self.menubar.addAction(self.menu.menuAction())

        self.actionChoose_txt.triggered.connect(self.Open_File)#选择文本文件的信号槽连接
        self.actionChoose_video.triggered.connect(self.Open_Video)#选择视频文件的信号槽连接
        self.actionbegin.triggered.connect(self.Begin)




        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "运动轨迹分析"))
        self.label_image.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "algorithm 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "algorithm 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "algorithm 3"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.actionChoose_txt.setText(_translate("MainWindow", "选择文本"))
        self.actionChoose_video.setText(_translate("MainWindow", "选择视频"))
        self.actionbegin.setText(_translate("MainWindow", "运行"))
    #开文本文件槽函数
    def Open_File(self,TxtDirectory):
        TxtDirectory, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          "选取文本文件",
                                                          "C:/",
                                                          "All Files (*);;Text Files (*.txt)")
        print(TxtDirectory, filetype)
    #开视频文件槽函数
    def Open_Video(self):
        fileName2, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                    "选取视频文件",
                                                                    "C:/",
                                                                    "All Files (*);;Video Files (*.rmvb,*.avi)")
        print(fileName2, filetype)
    #运行，槽函数
    def Begin(self):
        return 1
