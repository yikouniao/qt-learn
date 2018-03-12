# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'v101.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
import cv2
import random

from time import time
from util import load_mot, iou, show_tracking_results
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject,pyqtSignal
'''import qrc_resource'''
from functools import partial

#主窗口
class Ui_MainWindow(QtWidgets.QMainWindow):
    '''GUI class for algorithms. '''
    # thread for multi object tracking algorithm.
    mot_thread = None
    #初始化
    def __init__(self):
        super(Ui_MainWindow, self).__init__()#继承自Widgets的构造方法
        self.mot_thread = MOT()
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
        self.label_jiaoda.setPixmap(QtGui.QPixmap("./res/icon.png"))#交大校徽
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
        # set the window size for video/image
        self.label_image.setFixedSize(640, 480)
        self.label_image.setAutoFillBackground(False)
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
        # start the multi object tracking thread, run the algorithm.
        self.actionbegin.triggered.connect(self.mot_thread.start)
        # get the current frame and display the image on the gui.
        self.mot_thread.mot_signal.connect(self.update_frame)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "运动轨迹分析"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "单摄像头头多目标跟踪"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "algorithm 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "algorithm 3"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.actionChoose_txt.setText(_translate("MainWindow", "选择文本"))
        self.actionChoose_video.setText(_translate("MainWindow", "选择视频"))
        self.actionbegin.setText(_translate("MainWindow", "运行"))

    #开文本文件槽函数
    def Open_File(self):
        '''set the multi-object tracking detection directory. '''
        self.mot_thread.mot_det_dir, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          "选取文本文件",
                                                          "C:/",
                                                          "All Files (*);;Text Files (*.txt)")

    #开视频文件槽函数
    def Open_Video(self):
        '''set the multi-object tracking video directory.'''
        self.mot_thread.mot_video_dir, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                    "选取视频文件",
                                                                    "C:/",
                                                                    "All Files (*);;Video Files (*.rmvb,*.avi)")

    def update_frame(self, rgb_frame):
        self.label_image.clear()
        self.label_image.setPixmap(QtGui.QPixmap.fromImage(rgb_frame))


class MOT(QtCore.QThread):
    '''A class for multi object tracking thread. '''
    # video path and detection text path.
    mot_det_dir = None
    mot_video_dir = None
    vc = None
    tracks_active = []

    mot_signal = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(MOT, self).__init__(parent)

    def run(self):
        self.vc = cv2.VideoCapture(self.mot_video_dir)

        sigma_l = 0.4
        sigma_h = 0.5
        sigma_iou = 0.2
        t_min = 2

        # load bounding boxes.
        detections = load_mot(self.mot_det_dir)

        tracks_finished = []

        # set the color of the object randomly.
        color_for_boundingbox = [(13 * i % 255, (255 - 5 * i) % 255, (240 + 10 * i) % 255) for i in range(0, 51)]

        # run algorithm.
        for frame_num, detections_frame in enumerate(detections, start=1):
            # apply low threshold to detections

            dets = [det for det in detections_frame if det['score'] >= sigma_l]

            updated_tracks = []

            for track in self.tracks_active:
                if len(dets) > 0:
                    # get det with highest iou
                    best_match = max(dets, key=lambda x: iou(track['bboxes'][-1], x['bbox']))
                    if iou(track['bboxes'][-1], best_match['bbox']) >= sigma_iou:
                        track['bboxes'].append(best_match['bbox'])
                        track['max_score'] = max(track['max_score'], best_match['score'])

                        updated_tracks.append(track)

                        # remove from best matching detection from detections
                        del dets[dets.index(best_match)]

                # if track was not updated
                if len(updated_tracks) == 0 or track is not updated_tracks[-1]:
                    # finish track when the conditions are met
                    if track['max_score'] >= sigma_h and len(track['bboxes']) >= t_min:
                        tracks_finished.append(track)

            # create new tracks
            new_tracks = [{'bboxes': [det['bbox']], 'max_score': det['score'], 'start_frame': frame_num,
                           'color': color_for_boundingbox[(len(self.tracks_active) + random.randint(0, 51)) % 51]}
                          for i, det in enumerate(dets)]
            self.tracks_active = updated_tracks + new_tracks

            self.retval, current_frame = self.vc.read()
            labeled_frame = show_tracking_results(current_frame, self.tracks_active)
            rgb_frame = convert_cvimage_to_qimage(labeled_frame)
            self.mot_signal.emit(rgb_frame)
        self.vc.release()

def convert_cvimage_to_qimage(cvimage):
    '''Change the image format from mat to QImage.

    Args:
     cvimage: an image which is loaded by cv2.imread
    Return:
     q_image: an image can be shown on a qwidgets.
    '''
    bgr_image = cv2.resize(cvimage, (640, 480))
    rgb_frame = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    q_image = QtGui.QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0],
                            QtGui.QImage.Format_RGB888)
    return q_image