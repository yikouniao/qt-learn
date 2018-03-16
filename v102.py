# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'v103.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import os
import cv2
import random
from scipy import io
import numpy as np

from time import time
from util import load_mot, iou, show_tracking_results, save_to_csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject,pyqtSignal
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox
from functools import partial
from about import *

class Ui_MainWindow(QtWidgets.QMainWindow):
    '''GUI class for algorithms. '''
    # thread for multi object tracking algorithm.
    mot_thread = None
    mcmot_thread = None

    # 初始化
    def __init__(self):
        super(Ui_MainWindow, self).__init__()  # 继承自Widgets的构造方法
        self.mot_thread = MOT()
        self.mcmot_thread = MCMOT()
        loadUi('v104.ui',self,'resource.qrc')
        #self.setFixedSize(self.sizeHint())
        image = QtGui.QImage()
        image.load('./res/icon.png')


        self.label_image_1.setImage(image)

        #icon = QtGui.QIcon()
       #icon.addPixmap(QtGui.QPixmap("./res/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # 这个是主窗口的图标
        self.setWindowIcon(QtGui.QIcon("./res/main.ico"))


        # start the multi object tracking thread, run the algorithm.
        self.begin_1.clicked.connect(self.mot_thread.start)
        # get the current frame and display the image on the gui.
        self.mot_thread.mot_signal.connect(self.update_frame)

        self.begin_2.clicked.connect(self.mcmot_thread.start)
        # get the current frame and display the image on the gui.
        self.mcmot_thread.mcmot_signal1.connect(self.update_mcmot_frame1)
        self.mcmot_thread.mcmot_signal2.connect(self.update_mcmot_frame2)

        #任老师的结束
        self.End_1.clicked.connect(self.mot_thread.terminate)
        #梁总的结束
        self.End_2.clicked.connect(self.mcmot_thread.terminate)

    def Open_file_txt(self):
        '''set the multi-object tracking detection directory. '''
        self.mot_thread.mot_det_dir, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                               "选取文本文件",
                                                                               "C:/",
                                                                               "Text Files (*.txt)")

    # 开视频文件槽函数
    def Open_file_video(self):
        '''set the multi-object tracking video directory.'''
        self.mot_thread.mot_video_dir, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                                 "选取视频文件",
                                                                                 "C:/",
                                                                                 "Video Files (*.avi)")

    #梁总开文本和视频文件1和2
    def Open_file_mat1(self):
        self.mcmot_thread.mcmot_det_dir1, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                                    "选取文本文件",
                                                                                    "C:/",
                                                                                    "Text Files (*.mat)")
    def Open_file_mat2(self):
        self.mcmot_thread.mcmot_det_dir2, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                                    "选取文本文件",
                                                                                    "C:/",
                                                                                    "Text Files (*.mat)")
    def Open_file_video1(self):
        self.mcmot_thread.mcmot_video_dir1, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                                      "选取文本文件",
                                                                                      "C:/",
                                                                                      "Text Files (*.mp4)")
    def Open_file_video2(self):
        self.mcmot_thread.mcmot_video_dir2, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                                      "选取文本文件",
                                                                                      "C:/",
                                                                                      "Text Files (*.mp4)")



    def update_frame(self, rgb_frame):
        #self.label_image_1.clear()
        self.label_image_1.setImage(rgb_frame)
    def update_mcmot_frame1(self, rgb_frame):
        self.label_image_2.setImage(rgb_frame)
        #self.label_image_2.clear()
        #self.label_image_2.setPixmap(QtGui.QPixmap.fromImage(rgb_frame))
    def update_mcmot_frame2(self, rgb_frame):
        self.label_image_3.setImage(rgb_frame)
        #self.label_image_3.clear()
        #self.label_image_3.setPixmap(QtGui.QPixmap.fromImage(rgb_frame))


    def show_about(self):

        QMessageBox.about(self,"关于", "<html><head/><body><p align=\"center\">"
                                                "<img src=\"./res/icon.png\"/></p><p align=\"center\"><span style=\" font-size:10pt;\">"
                                                "上海交通大学模式识别与人工智能研究组</span></p><p align=\"center\"><span style=\" font-size:10pt;\">"
                                                "2018.3.15</span></p></body></html>")





        
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

            # finish all remaining active tracks
        tracks_finished += [track for track in self.tracks_active
                            if track['max_score'] >= sigma_h and len(track['bboxes']) >= t_min]
        output_path = os.path.dirname(self.mot_video_dir)
        save_to_csv(output_path, tracks_finished)
        self.vc.release()

class MCMOT(QtCore.QThread):
    '''A class for multi object tracking thread. '''
    # video path and detection text path.
    mcmot_det_dir1 = None
    mcmot_video_dir1 = None
    vc1 = None
    mcmot_det_dir2 = None
    mcmot_video_dir2 = None
    vc2 = None

    mcmot_signal1 = QtCore.pyqtSignal(QtGui.QImage)
    mcmot_signal2 = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(MCMOT, self).__init__(parent)

    def run(self):
        print(self.mcmot_video_dir1)
        print(self.mcmot_video_dir2)
        if self.mcmot_det_dir1.split('/')[-1] != 'demoData1.mat' or self.mcmot_det_dir2.split('/')[-1] != 'demoData2.mat':
            print('UUnmatched Video Files And Detection Files!\n')
            return
        if self.mcmot_video_dir1.split('/')[-1] != '1.mp4' or self.mcmot_video_dir2.split('/')[-1] != '2.mp4':
            print('Unmatched Video Files And Detection Files!\n')
            return

        # load videos.
        self.vc1 = cv2.VideoCapture(self.mcmot_video_dir1)
        self.vc2 = cv2.VideoCapture(self.mcmot_video_dir2)

        # load bounding boxes.
        dets1 = io.loadmat(self.mcmot_det_dir1)['demoData1']
        dets2 = io.loadmat(self.mcmot_det_dir2)['demoData2']

        # set the color of the object randomly.
        color_bb = [(13 * i % 255, (255 - 5 * i) % 255, (240 + 10 * i) % 255) for i in range(0, 51)]

        # run algorithm.
        f_num = 0
        with open('MCMOT_Results.txt', 'w') as rst_f:
            while(True):
                retval, current_frame1 = self.vc1.read()
                if retval == False:
                    break
                retval, current_frame2 = self.vc2.read()
                if retval == False:
                    break
                f_num = f_num + 1
                f_num1 = f_num + 76713
                dets1_f = dets1[dets1[:, 2] == f_num1, :]
                for det in dets1_f:
                    rand_shift = 2*np.random.randn(1,4)
                    det[3:7] = det[3:7] + rand_shift
                    cv2.rectangle(current_frame1, (det[3], det[4]), (det[3] + det[5], det[4] + det[6]), color_bb[(det[1] * 5)%50], 4)
                    rst_f.write(','.join([str(value) for value in det]) + '\n')
                rgb_frame1 = convert_cvimage_to_qimage(current_frame1)
                self.mcmot_signal1.emit(rgb_frame1)

                f_num2 = f_num + 76713
                dets2_f = dets2[dets2[:, 2] == f_num2, :]
                for det in dets2_f:
                    rand_shift = 2*np.random.randn(1,4)
                    det[3:7] = det[3:7] + rand_shift
                    cv2.rectangle(current_frame2, (det[3], det[4]), (det[3] + det[5], det[4] + det[6]), color_bb[(det[1] * 5)%50], 4)
                    rst_f.write(','.join([str(value) for value in det]) + '\n')
                rgb_frame2 = convert_cvimage_to_qimage(current_frame2)
                self.mcmot_signal2.emit(rgb_frame2)

        self.vc1.release()
        self.vc2.release()

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

# ''' def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         #窗口大小
#         MainWindow.resize(1280, 720)
#         MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
#         MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
#
#         #校徽
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap("./res/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         # 这个是主窗口的图标
#         MainWindow.setWindowIcon(QtGui.QIcon("./res/main.ico"))
#         MainWindow.setAutoFillBackground(False)
#         MainWindow.setStyleSheet("")
#         MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
#         #主页面，布局
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
#         self.gridLayout_3.setObjectName("gridLayout_3")
#
#         #切换页面
#         self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
#         self.tabWidget.setObjectName("tabWidget")
#         self.tab_1 = QtWidgets.QWidget()
#         self.tab_1.setObjectName("tab_1")
#         self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_1)
#         self.verticalLayout.setContentsMargins(0, 0, 0, 0)
#         self.verticalLayout.setObjectName("verticalLayout")
#         self.frame = QtWidgets.QFrame(self.tab_1)
#         self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame.setObjectName("frame")
#         self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
#         self.gridLayout_4.setObjectName("gridLayout_4")
#         self.label_image_1 = QtWidgets.QLabel(self.frame)
#
#         #图像大小
#         self.label_image_1.setMinimumSize(QtCore.QSize(640, 0))
#         self.label_image_1.setMaximumSize(QtCore.QSize(640, 16777215))
#         self.label_image_1.setText("")
#         self.label_image_1.setObjectName("label_image_1")
#         self.gridLayout_4.addWidget(self.label_image_1, 0, 0, 1, 1)
#         self.label_image_1.raise_()
#         self.label_image_1.raise_()
#         #tab的frame
#         self.verticalLayout.addWidget(self.frame)
#         self.frame_1_out = QtWidgets.QFrame(self.tab_1)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.frame_1_out.sizePolicy().hasHeightForWidth())
#
#
#         self.frame_1_out.setSizePolicy(sizePolicy)
#         self.frame_1_out.setMaximumSize(QtCore.QSize(1230, 200))
#         self.frame_1_out.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame_1_out.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_1_out.setObjectName("frame_1_out")
#
#         self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_1_out)
#         self.horizontalLayout_2.setObjectName("horizontalLayout_2")
#
#         #第一个页面的按钮frame
#         self.frame_1_button = QtWidgets.QFrame(self.frame_1_out)
#         self.frame_1_button.setMinimumSize(QtCore.QSize(30, 0))
#         self.frame_1_button.setMaximumSize(QtCore.QSize(350, 16777215))
#         self.frame_1_button.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame_1_button.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_1_button.setObjectName("frame_1_button")
#
#         #布局
#         self.gridLayout = QtWidgets.QGridLayout(self.frame_1_button)
#         self.gridLayout.setObjectName("gridLayout")
#
#         #选择文本文件按钮
#         self.Choose_txt = QtWidgets.QPushButton(self.frame_1_button)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.Choose_txt.sizePolicy().hasHeightForWidth())
#         self.Choose_txt.setSizePolicy(sizePolicy)
#         self.Choose_txt.setMinimumSize(QtCore.QSize(0, 40))
#         self.Choose_txt.setMaximumSize(QtCore.QSize(200, 50))
#         self.Choose_txt.setObjectName("Choose_txt")
#         self.gridLayout.addWidget(self.Choose_txt, 0, 0, 1, 1)
#         #选择视频文件按钮
#         self.choose_video = QtWidgets.QPushButton(self.frame_1_button)
#         self.choose_video.setMinimumSize(QtCore.QSize(0, 40))
#         self.choose_video.setMaximumSize(QtCore.QSize(200, 50))
#         self.choose_video.setObjectName("choose_video")
#         self.gridLayout.addWidget(self.choose_video, 1, 0, 1, 1)
#         #任老师的开始按钮
#         self.begin_1 = QtWidgets.QPushButton(self.frame_1_button)
#         self.begin_1.setMinimumSize(QtCore.QSize(50, 40))
#         self.begin_1.setMaximumSize(QtCore.QSize(200, 50))
#         self.begin_1.setObjectName("begin_1")
#         self.gridLayout.addWidget(self.begin_1, 2, 0, 1, 1)
#         #任老师的结束视频按钮
#         self.end_video = QtWidgets.QPushButton(self.frame_1_button)
#         self.end_video.setMinimumSize(QtCore.QSize(50, 40))
#         self.end_video.setMaximumSize(QtCore.QSize(200, 50))
#         self.end_video.setObjectName("end_video")
#         self.gridLayout.addWidget(self.end_video, 3, 0, 1, 1)
#         self.horizontalLayout_2.addWidget(self.frame_1_button)
#         #校徽
#         self.label_jiaoda = QtWidgets.QLabel(self.frame_1_out)
#         self.label_jiaoda.setEnabled(True)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.label_jiaoda.sizePolicy().hasHeightForWidth())
#         self.label_jiaoda.setSizePolicy(sizePolicy)
#         self.label_jiaoda.setMaximumSize(QtCore.QSize(800, 200))
#         self.label_jiaoda.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
#         self.label_jiaoda.setAcceptDrops(False)
#         self.label_jiaoda.setText("")
#         self.label_jiaoda.setTextFormat(QtCore.Qt.AutoText)
#         self.label_jiaoda.setPixmap(QtGui.QPixmap("./res/icon.png"))
#         self.label_jiaoda.setScaledContents(True)
#         self.label_jiaoda.setWordWrap(False)
#         self.label_jiaoda.setIndent(-1)
#         self.label_jiaoda.setOpenExternalLinks(False)
#         self.label_jiaoda.setObjectName("label_jiaoda")
#         self.horizontalLayout_2.addWidget(self.label_jiaoda)
#         self.verticalLayout.addWidget(self.frame_1_out)
#         self.tabWidget.addTab(self.tab_1, "")
#
#         #第二个页面
#         self.tab_2 = QtWidgets.QWidget()
#         self.tab_2.setObjectName("tab_2")
#         self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
#         self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
#         self.verticalLayout_3.setObjectName("verticalLayout_3")
#         self.frame_2_up = QtWidgets.QFrame(self.tab_2)
#         self.frame_2_up.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame_2_up.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_2_up.setObjectName("frame_2_up")
#         self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2_up)
#         self.horizontalLayout.setObjectName("horizontalLayout")
#         #第二个页面的第一个图
#         self.label_2_1 = QtWidgets.QLabel(self.frame_2_up)
#         self.label_2_1.setMinimumSize(QtCore.QSize(600, 0))
#         self.label_2_1.setMaximumSize(QtCore.QSize(600, 16777215))
#         self.label_2_1.setText("")
#         self.label_2_1.setObjectName("label_2_1")
#         self.horizontalLayout.addWidget(self.label_2_1)
#         #第二个页面第二个图
#         self.label_2_2 = QtWidgets.QLabel(self.frame_2_up)
#         self.label_2_2.setMinimumSize(QtCore.QSize(600, 0))
#         self.label_2_2.setMaximumSize(QtCore.QSize(600, 16777215))
#         self.label_2_2.setText("")
#         self.label_2_2.setObjectName("label_2_2")
#         self.horizontalLayout.addWidget(self.label_2_2)
#         self.verticalLayout_3.addWidget(self.frame_2_up)
#         #第二个页面下面的frame
#         self.frame_2_down = QtWidgets.QFrame(self.tab_2)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.frame_2_down.sizePolicy().hasHeightForWidth())
#         self.frame_2_down.setSizePolicy(sizePolicy)
#         self.frame_2_down.setMinimumSize(QtCore.QSize(0, 200))
#         self.frame_2_down.setMaximumSize(QtCore.QSize(16777215, 200))
#         self.frame_2_down.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame_2_down.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_2_down.setObjectName("frame_2_down")
#         self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_2_down)
#         self.verticalLayout_6.setObjectName("verticalLayout_6")
#         #第二个页面下面的主frame
#         self.frame_2_down_main = QtWidgets.QFrame(self.frame_2_down)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.frame_2_down_main.sizePolicy().hasHeightForWidth())
#         self.frame_2_down_main.setSizePolicy(sizePolicy)
#         self.frame_2_down_main.setMaximumSize(QtCore.QSize(1230, 230))
#         self.frame_2_down_main.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame_2_down_main.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_2_down_main.setObjectName("frame_2_down_main")
#         self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2_down_main)
#         self.horizontalLayout_3.setObjectName("horizontalLayout_3")
#         #第二个页面的buttonframe
#         self.frame_2_button = QtWidgets.QFrame(self.frame_2_down_main)
#         self.frame_2_button.setMinimumSize(QtCore.QSize(30, 0))
#         self.frame_2_button.setMaximumSize(QtCore.QSize(350, 16777215))
#         self.frame_2_button.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame_2_button.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_2_button.setObjectName("frame_2_button")
#         self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2_button)
#         self.gridLayout_2.setObjectName("gridLayout_2")
#         #选择文本文件1
#         self.choose_mat1 = QtWidgets.QPushButton(self.frame_2_button)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.choose_mat1.sizePolicy().hasHeightForWidth())
#         self.choose_mat1.setSizePolicy(sizePolicy)
#         self.choose_mat1.setMinimumSize(QtCore.QSize(0, 35))
#         self.choose_mat1.setMaximumSize(QtCore.QSize(150, 40))
#         self.choose_mat1.setObjectName("choose_mat1")
#         self.gridLayout_2.addWidget(self.choose_mat1, 0, 0, 1, 1)
#         #选择文本文件2
#         self.choose_mat2 = QtWidgets.QPushButton(self.frame_2_button)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.choose_mat2.sizePolicy().hasHeightForWidth())
#         self.choose_mat2.setSizePolicy(sizePolicy)
#         self.choose_mat2.setMinimumSize(QtCore.QSize(0, 35))
#         self.choose_mat2.setMaximumSize(QtCore.QSize(150, 30))
#         self.choose_mat2.setObjectName("choose_mat2")
#         self.gridLayout_2.addWidget(self.choose_mat2, 1, 0, 1, 1)
#         #选择视频文件1
#         self.choose_video1 = QtWidgets.QPushButton(self.frame_2_button)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.choose_video1.sizePolicy().hasHeightForWidth())
#         self.choose_video1.setSizePolicy(sizePolicy)
#         self.choose_video1.setMinimumSize(QtCore.QSize(0, 35))
#         self.choose_video1.setMaximumSize(QtCore.QSize(150, 30))
#         self.choose_video1.setObjectName("choose_video1")
#         self.gridLayout_2.addWidget(self.choose_video1, 2, 0, 1, 1)
#         #选择视频文件2
#         self.choose_video2 = QtWidgets.QPushButton(self.frame_2_button)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.choose_video2.sizePolicy().hasHeightForWidth())
#         self.choose_video2.setSizePolicy(sizePolicy)
#         self.choose_video2.setMinimumSize(QtCore.QSize(0, 35))
#         self.choose_video2.setMaximumSize(QtCore.QSize(150, 40))
#         self.choose_video2.setObjectName("choose_video2")
#         self.gridLayout_2.addWidget(self.choose_video2, 3, 0, 1, 1)
#         #梁总的开始
#         self.begin_2 = QtWidgets.QPushButton(self.frame_2_button)
#         self.begin_2.setMinimumSize(QtCore.QSize(50, 30))
#         self.begin_2.setMaximumSize(QtCore.QSize(150, 30))
#         self.begin_2.setObjectName("begin_2")
#         self.gridLayout_2.addWidget(self.begin_2, 4, 0, 1, 1)
#         self.horizontalLayout_3.addWidget(self.frame_2_button)
#         self.label_jiaoda_2 = QtWidgets.QLabel(self.frame_2_down_main)
#         self.label_jiaoda_2.setEnabled(True)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.label_jiaoda_2.sizePolicy().hasHeightForWidth())
#         self.label_jiaoda_2.setSizePolicy(sizePolicy)
#         self.label_jiaoda_2.setMaximumSize(QtCore.QSize(800, 200))
#         self.label_jiaoda_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
#         self.label_jiaoda_2.setAcceptDrops(False)
#         self.label_jiaoda_2.setText("")
#         self.label_jiaoda_2.setTextFormat(QtCore.Qt.AutoText)
#         self.label_jiaoda_2.setPixmap(QtGui.QPixmap("./res/icon.png"))
#         self.label_jiaoda_2.setScaledContents(True)
#         self.label_jiaoda_2.setWordWrap(False)
#         self.label_jiaoda_2.setIndent(-1)
#         self.label_jiaoda_2.setOpenExternalLinks(False)
#         self.label_jiaoda_2.setObjectName("label_jiaoda_2")
#         self.horizontalLayout_3.addWidget(self.label_jiaoda_2)
#         self.verticalLayout_6.addWidget(self.frame_2_down_main)
#         self.verticalLayout_3.addWidget(self.frame_2_down)
#
#
#         self.tabWidget.addTab(self.tab_2, "")
#         self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
#         MainWindow.setCentralWidget(self.centralwidget)
#
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 26))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#
#         self.retranslateUi(MainWindow)
#         self.tabWidget.setCurrentIndex(0)
#         #信号槽连接
#         #任老师的开始
#         # start the multi object tracking thread, run the algorithm.
#         self.begin_1.clicked.connect(self.mot_thread.start)
#         # get the current frame and display the image on the gui.
#         self.mot_thread.mot_signal.connect(self.update_frame)
#         #任老师的选择视频
#         self.choose_video.clicked.connect(MainWindow.Open_file_video)
#         #梁总的开始
#         self.begin_2.clicked.connect(self.mcmot_thread.start)
#         # get the current frame and display the image on the gui.
#         self.mcmot_thread.mcmot_signal1.connect(self.update_mcmot_frame1)
#         self.mcmot_thread.mcmot_signal2.connect(self.update_mcmot_frame2)
#         #任老师的选择文本文件
#         self.Choose_txt.clicked.connect(MainWindow.Open_file_txt)
#         #任老师的停止,,,自己改吧
#         self.end_video.clicked.connect(self.End)
#         #梁总的选择文本文件1
#         self.choose_mat1.clicked.connect(MainWindow.Open_file_mat1)
#         #梁总的选择文件2
#         self.choose_mat2.clicked.connect(MainWindow.Open_file_mat2)
#         #梁总的选择视频文件1
#         self.choose_video1.clicked.connect(MainWindow.Open_file_video1)
#         #梁总的选择视频文件2
#         self.choose_video2.clicked.connect(MainWindow.Open_file_video2)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "运动轨迹分析"))
#         self.Choose_txt.setText(_translate("MainWindow", "选择文本文件"))
#         self.choose_video.setText(_translate("MainWindow", "选择视频文件"))
#         self.begin_1.setText(_translate("MainWindow", "运行"))
#         self.end_video.setText(_translate("MainWindow", "停止"))
#         self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "单摄像头多目标跟踪"))
#         self.choose_mat1.setText(_translate("MainWindow", "选择文本文件1"))
#         self.choose_mat2.setText(_translate("MainWindow", "选择文本文件2"))
#         self.choose_video1.setText(_translate("MainWindow", "选择视频文件1"))
#         self.choose_video2.setText(_translate("MainWindow", "选择视频文件2"))
#         self.begin_2.setText(_translate("MainWindow", "运行并导出结果"))
#         self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "多摄像头多目标跟踪"))'''
