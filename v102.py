# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'v102.ui'
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

    # 初始化
    def __init__(self):
        super(Ui_MainWindow, self).__init__()  # 继承自Widgets的构造方法
        self.mot_thread = MOT()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #固定窗口大小
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        # 交大校徽
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./res/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # 这个是主窗口的图标
        MainWindow.setWindowIcon(QtGui.QIcon("./res/main.ico"))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

        #主页面，及布局
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        #切换页面的widget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_image_1 = QtWidgets.QLabel(self.tab_1)
        # set the window size for video/image
        self.label_image_1.setFixedSize(640, 480)
        self.label_image_1.setText("")
        self.label_image_1.setObjectName("label_image_1")
        self.verticalLayout.addWidget(self.label_image_1)
        #tab1 的frame
        self.frame_1_out = QtWidgets.QFrame(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_1_out.sizePolicy().hasHeightForWidth())
        self.frame_1_out.setSizePolicy(sizePolicy)
        self.frame_1_out.setMaximumSize(QtCore.QSize(1230, 230))
        self.frame_1_out.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1_out.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1_out.setObjectName("frame_1_out")


        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_1_out)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        #放button的frame
        self.frame_1_button = QtWidgets.QFrame(self.frame_1_out)
        self.frame_1_button.setMinimumSize(QtCore.QSize(30, 0))
        self.frame_1_button.setMaximumSize(QtCore.QSize(350, 16777215))
        self.frame_1_button.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1_button.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1_button.setObjectName("frame_1_button")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_1_button)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        #选择文本文件按钮
        self.Choose_txt = QtWidgets.QPushButton(self.frame_1_button)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Choose_txt.sizePolicy().hasHeightForWidth())
        self.Choose_txt.setSizePolicy(sizePolicy)
        self.Choose_txt.setMinimumSize(QtCore.QSize(0, 50))
        self.Choose_txt.setMaximumSize(QtCore.QSize(300, 16777215))
        self.Choose_txt.setObjectName("Choose_txt")
        self.verticalLayout_2.addWidget(self.Choose_txt)

        #选择视频文件按钮
        self.choose_video = QtWidgets.QPushButton(self.frame_1_button)
        self.choose_video.setMinimumSize(QtCore.QSize(0, 50))
        self.choose_video.setMaximumSize(QtCore.QSize(300, 16777215))
        self.choose_video.setObjectName("choose_video")
        self.verticalLayout_2.addWidget(self.choose_video)

        #任老师的开始按钮
        self.begin_1 = QtWidgets.QPushButton(self.frame_1_button)
        self.begin_1.setMinimumSize(QtCore.QSize(50, 50))
        self.begin_1.setMaximumSize(QtCore.QSize(300, 50))
        self.begin_1.setObjectName("begin_1")
        self.verticalLayout_2.addWidget(self.begin_1)
        self.horizontalLayout_2.addWidget(self.frame_1_button)

        #交大校徽
        self.label_jiaoda = QtWidgets.QLabel(self.frame_1_out)
        self.label_jiaoda.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_jiaoda.sizePolicy().hasHeightForWidth())
        self.label_jiaoda.setSizePolicy(sizePolicy)
        self.label_jiaoda.setMaximumSize(QtCore.QSize(800, 200))
        self.label_jiaoda.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.label_jiaoda.setAcceptDrops(False)
        self.label_jiaoda.setText("")
        self.label_jiaoda.setTextFormat(QtCore.Qt.AutoText)
        self.label_jiaoda.setPixmap(QtGui.QPixmap("./res/icon.png"))
        self.label_jiaoda.setScaledContents(True)
        self.label_jiaoda.setWordWrap(False)
        self.label_jiaoda.setIndent(-1)
        self.label_jiaoda.setOpenExternalLinks(False)
        self.label_jiaoda.setObjectName("label_jiaoda")


        self.horizontalLayout_2.addWidget(self.label_jiaoda)
        self.verticalLayout.addWidget(self.frame_1_out)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        #第二个页面的上面的frame
        self.frame_2_up = QtWidgets.QFrame(self.tab_2)
        self.frame_2_up.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2_up.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2_up.setObjectName("frame_2_up")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2_up)
        self.horizontalLayout.setObjectName("horizontalLayout")
        #第二个页面的第一幅图像
        self.label_2_1 = QtWidgets.QLabel(self.frame_2_up)
        # set the window size for video/image
        self.label_2_1.setFixedSize(640, 480)
        self.label_2_1.setMinimumSize(QtCore.QSize(600, 0))
        self.label_2_1.setMaximumSize(QtCore.QSize(600, 16777215))
        self.label_2_1.setText("")
        self.label_2_1.setObjectName("label_2_1")
        self.horizontalLayout.addWidget(self.label_2_1)

        #第二个页面的第二副图像
        self.label_2_2 = QtWidgets.QLabel(self.frame_2_up)
        # set the window size for video/image
        self.label_2_2.setFixedSize(640, 480)
        self.label_2_2.setMinimumSize(QtCore.QSize(600, 0))
        self.label_2_2.setMaximumSize(QtCore.QSize(600, 16777215))
        self.label_2_2.setText("")
        self.label_2_2.setObjectName("label_2_2")


        self.horizontalLayout.addWidget(self.label_2_2)
        self.verticalLayout_3.addWidget(self.frame_2_up)
        #第二个页面，下面的frame
        self.frame_2_down = QtWidgets.QFrame(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2_down.sizePolicy().hasHeightForWidth())
        self.frame_2_down.setSizePolicy(sizePolicy)
        self.frame_2_down.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2_down.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2_down.setObjectName("frame_2_down")


        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_2_down)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        #第二个页面下面frame的主fame
        self.frame_2_down_main = QtWidgets.QFrame(self.frame_2_down)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2_down_main.sizePolicy().hasHeightForWidth())
        self.frame_2_down_main.setSizePolicy(sizePolicy)
        self.frame_2_down_main.setMaximumSize(QtCore.QSize(1230, 230))
        self.frame_2_down_main.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2_down_main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2_down_main.setObjectName("frame_2_down_main")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2_down_main)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        #第二个页面的buttonframe
        self.frame_2_button = QtWidgets.QFrame(self.frame_2_down_main)
        self.frame_2_button.setMinimumSize(QtCore.QSize(30, 0))
        self.frame_2_button.setMaximumSize(QtCore.QSize(350, 16777215))
        self.frame_2_button.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2_button.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2_button.setObjectName("frame_2_button")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_2_button)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        #梁总的选择文件按钮
        self.choose_file = QtWidgets.QPushButton(self.frame_2_button)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_file.sizePolicy().hasHeightForWidth())
        self.choose_file.setSizePolicy(sizePolicy)
        self.choose_file.setMinimumSize(QtCore.QSize(0, 50))
        self.choose_file.setMaximumSize(QtCore.QSize(300, 16777215))
        self.choose_file.setObjectName("choose_file")
        self.verticalLayout_4.addWidget(self.choose_file)

        #梁总的开始按钮
        self.begin_2 = QtWidgets.QPushButton(self.frame_2_button)
        self.begin_2.setMinimumSize(QtCore.QSize(50, 50))
        self.begin_2.setMaximumSize(QtCore.QSize(300, 50))
        self.begin_2.setObjectName("begin_2")
        self.verticalLayout_4.addWidget(self.begin_2)
        self.horizontalLayout_3.addWidget(self.frame_2_button)
        #交大校徽
        self.label_jiaoda_2 = QtWidgets.QLabel(self.frame_2_down_main)
        self.label_jiaoda_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_jiaoda_2.sizePolicy().hasHeightForWidth())
        self.label_jiaoda_2.setSizePolicy(sizePolicy)
        self.label_jiaoda_2.setMaximumSize(QtCore.QSize(800, 200))
        self.label_jiaoda_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.label_jiaoda_2.setAcceptDrops(False)
        self.label_jiaoda_2.setText("")
        self.label_jiaoda_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_jiaoda_2.setPixmap(QtGui.QPixmap("./res/icon.png"))
        self.label_jiaoda_2.setScaledContents(True)
        self.label_jiaoda_2.setWordWrap(False)
        self.label_jiaoda_2.setIndent(-1)
        self.label_jiaoda_2.setOpenExternalLinks(False)
        self.label_jiaoda_2.setObjectName("label_jiaoda_2")
        self.horizontalLayout_3.addWidget(self.label_jiaoda_2)
        self.verticalLayout_6.addWidget(self.frame_2_down_main)
        self.verticalLayout_3.addWidget(self.frame_2_down)
        self.tabWidget.addTab(self.tab_2, "")

        #第三个界面，尚无
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout_5.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        #主菜单
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 26))
        self.menubar.setObjectName("menubar")
        #关于按钮
        self.menu_about = QtWidgets.QMenu(self.menubar)
        self.menu_about.setObjectName("menu_about")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu_about.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        #连接信号槽
        #关于
        self.menubar.triggered['QAction*'].connect(self.show_about)
        #选择文本文件
        self.Choose_txt.clicked.connect(self.Open_file_txt)
        #选择视频文件
        self.choose_video.clicked.connect(self.Open_file_video)
        #任老师的运行
        # start the multi object tracking thread, run the algorithm.
        self.begin_1.clicked.connect(self.mot_thread.start)
        # get the current frame and display the image on the gui.
        self.mot_thread.mot_signal.connect(self.update_frame)


        #梁总的选择文件
        self.choose_file.clicked.connect(self.Open_file2)
        #梁总的运行
        self.begin_2.clicked.connect(self.Begin_2)


        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "运动轨迹分析"))
        self.Choose_txt.setText(_translate("MainWindow", "选择文本文件"))
        self.choose_video.setText(_translate("MainWindow", "选择视频文件"))
        self.begin_1.setText(_translate("MainWindow", "运行"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "单摄像头多目标跟踪"))
        self.choose_file.setText(_translate("MainWindow", "选择文件"))
        self.begin_2.setText(_translate("MainWindow", "运行"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "algorithm 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "algorithm 3"))
        self.menu_about.setTitle(_translate("MainWindow", "关于"))
    #任老师的开txt文件槽函数
    def Open_file_txt(self):
        '''set the multi-object tracking detection directory. '''
        self.mot_thread.mot_det_dir, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                               "选取文本文件",
                                                                               "C:/",
                                                                               "All Files (*);;Text Files (*.txt)")

    # 开视频文件槽函数
    def Open_file_video(self):
        '''set the multi-object tracking video directory.'''
        self.mot_thread.mot_video_dir, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                                 "选取视频文件",
                                                                                 "C:/",
                                                                                 "All Files (*);;Video Files (*.rmvb,*.avi)")

    #梁总，你看着改这个是开文件
    def Open_file2(self):
        '''set the multi-object tracking detection directory. '''
        self.mot_thread.mot_det_dir, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                               "选取文本文件",
                                                                               "C:/",
                                                                               "All Files (*);;Text Files (*.txt)")

    #梁总，你的运行
    def Begin_2(self):
        return

    #用来显示关于的
    def show_about(self):
        QtWidgets.QMessageBox.information(self,
                                "关于",
                                "上海交通大学CVPR实验室")
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