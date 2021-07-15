
import datetime
import cv2
from PyQt5.QtCore import *
import threading, os, time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QFileDialog, QApplication, QListWidget
from main import start_camera, stop, re_start, start_video1, start_video2, start_video3, start_video4, start_video5, start_video6, start_video7,find_one
from image import start_image, people_num1
from PyQt5.QtCore import QThread, pyqtSignal
import shutil
import sqlite3
global is_open, index
is_open = 1
index = 1

class WorkThread(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    signal = pyqtSignal(str)

    def __int__(self):
        # 初始化函数
        super(WorkThread, self).__init__()

    def run(self):
        time.sleep(10)
        for i in range(1, 298):
            # 通过自定义信号把待显示的字符串传递给槽函数
            self.signal.emit(str(i))
            time.sleep(0.4)

class Work2Thread(QThread):
    def __int__(self):
        # 初始化函数
        super(Work2Thread, self).__init__()

    def run(self):
        a = Ui_self()
        a.start_video()

class Work3Thread(QThread):
    def __int__(self):
        # 初始化函数
        super(Work3Thread, self).__init__()

    def run(self):
        a = Ui_self()
        a.start_camera()

class Work4Thread(QThread):
    def __int__(self):
        # 初始化函数
        super(Work4Thread, self).__init__()

    def run(self):
        a = Ui_self()
        a.start_image()


#----------------------------------

class Ui_self(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setting_flag = 1
        self.init_ui()

        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.timer3 = QtCore.QTimer()
        self.timer4 = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.work = WorkThread() # 展示图片
        self.work.signal.connect(self.show_image) # 设置子线程发出信号后激活的函数
        self.work2 = Work2Thread() # 视频检测
        self.work3 = Work3Thread() # 摄像头检测
        self.work4 = Work4Thread() # 图片检测
        self.listFile = QListWidget()

        self.videoName=[] #地址列表

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setObjectName("self")
        self.resize(1223, 640)
        self.label_p1 = QtWidgets.QLabel(self)
        self.label_p1.setGeometry(QtCore.QRect(-20, -10, 401, 651))
        self.label_p1.setText("")
        self.label_p1.setPixmap(QtGui.QPixmap("./icons/bg.png"))
        self.label_p1.setScaledContents(True)
        self.label_p1.setObjectName("label_p1")
        self.label_pp = QtWidgets.QLabel(self)
        self.label_pp.setGeometry(QtCore.QRect(80, 110, 201, 61))
        self.label_pp.setText("")
        self.label_pp.setPixmap(QtGui.QPixmap("./icons/下载.png"))
        self.label_pp.setScaledContents(True)
        self.label_pp.setObjectName("label_pp")
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setGeometry(QtCore.QRect(50, 180, 261, 41))
        self.label_name.setStyleSheet("color: rgb(255, 255, 255);\n"
                                      "font: 12pt \"黑体\";")
        self.label_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_name.setObjectName("label_name")

        self.label_team = QtWidgets.QLabel(self)
        self.label_team.setGeometry(QtCore.QRect(50, 205, 261, 41))
        self.label_team.setStyleSheet("color: rgb(255, 255, 255);\n"
                                      "font: 11pt \"黑体\";")
        self.label_team.setAlignment(QtCore.Qt.AlignCenter)
        self.label_team.setObjectName("label_team")

        self.btn_close = QtWidgets.QPushButton(self)
        self.btn_close.setGeometry(QtCore.QRect(305, 32, 35, 35))
        self.btn_close.setStyleSheet("QPushButton{\n"
                                     "    border:none;\n"
                                     "    border-radius:6px;\n"
                                     "    background-color: transparent;\n"
                                     "}\n"
                                     "QPushButton:hover{\n"
                                     "    background-color: rgb(52, 59, 72);\n"
                                     "}\n"
                                     "QPushButton:pressed{\n"
                                     "    background-color: rgb(25, 40, 50);\n"
                                     "}")
        self.btn_close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./icons/cil-x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_close.setIcon(icon)
        self.btn_close.setFlat(True)
        self.btn_close.setObjectName("btn_close")
        self.btn_min = QtWidgets.QPushButton(self)
        self.btn_min.setGeometry(QtCore.QRect(272, 32, 35, 35))
        self.btn_min.setStyleSheet("QPushButton{\n"
                                   "    border:none;\n"
                                   "    border-radius:6px;\n"
                                   "    background-color: transparent;\n"
                                   "}\n"
                                   "QPushButton:hover{\n"
                                   "    background-color: rgb(52, 59, 72);\n"
                                   "}\n"
                                   "QPushButton:pressed{\n"
                                   "    background-color: rgb(25, 40, 50);\n"
                                   "}")
        self.btn_min.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./icons/cil-window-minimize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_min.setIcon(icon1)
        self.btn_min.setFlat(True)
        self.btn_min.setObjectName("btn_min")
        self.btn_show = QtWidgets.QPushButton(self)
        self.btn_show.setGeometry(QtCore.QRect(290, 550, 35, 35))
        self.btn_show.setStyleSheet("QPushButton{\n"
                                    "    border: 2px solid rgb(52, 59, 72);\n"
                                    "    border-radius: 5px;\n"
                                    "    background-color: rgb(52, 59, 72);\n"
                                    "}\n"
                                    "QPushButton:hover{\n"
                                    "    background-color: rgb(57, 65, 80);\n"
                                    "    border: 2px solid rgb(61, 70, 86);\n"
                                    "}\n"
                                    "QPushButton:pressed{\n"
                                    "    background-color: rgb(35, 40, 49);\n"
                                    "    border: 2px solid rgb(43, 50, 61);\n"
                                    "}")
        self.btn_show.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./icons/right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_show.setIcon(icon2)
        self.btn_show.setFlat(True)
        self.btn_show.setObjectName("btn_show")
        self.label_upload = QtWidgets.QLabel(self)
        self.label_upload.setGeometry(QtCore.QRect(48, 305, 290, 101))
        self.label_upload.setText("")
        self.label_upload.setPixmap(QtGui.QPixmap("./icons/label_gray.png"))
        self.label_upload.setScaledContents(True)
        self.label_upload.setObjectName("label_upload")
        self.btn_camera = QtWidgets.QPushButton(self)
        self.btn_camera.setGeometry(QtCore.QRect(55, 310, 81, 81))
        self.btn_camera.setStyleSheet("QPushButton{\n"
                                      "    border: 2px solid rgb(52, 59, 72);\n"
                                      "    border-radius: 5px;\n"
                                      "    background-color: rgb(52, 59, 72);\n"
                                      "}\n"
                                      "QPushButton:hover{\n"
                                      "    background-color: rgb(57, 65, 80);\n"
                                      "    border: 2px solid rgb(61, 70, 86);\n"
                                      "}\n"
                                      "QPushButton:pressed{\n"
                                      "    background-color: rgb(35, 40, 49);\n"
                                      "    border: 2px solid rgb(43, 50, 61);\n"
                                      "}")
        self.btn_camera.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./icons/camera.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_camera.setIcon(icon3)
        self.btn_camera.setIconSize(QtCore.QSize(50, 50))
        self.btn_camera.setObjectName("btn_camera")
        self.btn_image = QtWidgets.QPushButton(self)
        self.btn_image.setGeometry(QtCore.QRect(141, 310, 81, 81))
        self.btn_image.setStyleSheet("QPushButton{\n"
                                     "    border: 2px solid rgb(52, 59, 72);\n"
                                     "    border-radius: 5px;\n"
                                     "    background-color: rgb(52, 59, 72);\n"
                                     "}\n"
                                     "QPushButton:hover{\n"
                                     "    background-color: rgb(57, 65, 80);\n"
                                     "    border: 2px solid rgb(61, 70, 86);\n"
                                     "}\n"
                                     "QPushButton:pressed{\n"
                                     "    background-color: rgb(35, 40, 49);\n"
                                     "    border: 2px solid rgb(43, 50, 61);\n"
                                     "}")
        self.btn_image.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./icons/image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_image.setIcon(icon4)
        self.btn_image.setIconSize(QtCore.QSize(50, 50))
        self.btn_image.setObjectName("btn_image")
        self.btn_video = QtWidgets.QPushButton(self)
        self.btn_video.setGeometry(QtCore.QRect(226, 310, 81, 81))
        self.btn_video.setStyleSheet("QPushButton{\n"
                                     "    border: 2px solid rgb(52, 59, 72);\n"
                                     "    border-radius: 5px;\n"
                                     "    background-color: rgb(52, 59, 72);\n"
                                     "}\n"
                                     "QPushButton:hover{\n"
                                     "    background-color: rgb(57, 65, 80);\n"
                                     "    border: 2px solid rgb(61, 70, 86);\n"
                                     "}\n"
                                     "QPushButton:pressed{\n"
                                     "    background-color: rgb(35, 40, 49);\n"
                                     "    border: 2px solid rgb(43, 50, 61);\n"
                                     "}")
        self.btn_video.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("./icons/video.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_video.setIcon(icon5)
        self.btn_video.setIconSize(QtCore.QSize(50, 50))
        self.btn_video.setObjectName("btn_video")
        self.label_11 = QtWidgets.QLabel(self)
        self.label_11.setGeometry(QtCore.QRect(50, 420, 290, 101))
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap("./icons/label_gray.png"))
        self.label_11.setScaledContents(True)
        self.label_11.setObjectName("label_11")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(339, 14, 891, 611))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_p2 = QtWidgets.QLabel(self.frame)
        self.label_p2.setGeometry(QtCore.QRect(0, 0, 931, 561))
        self.label_p2.setText("")
        self.label_p2.setPixmap(QtGui.QPixmap("./icons/label_gray.png"))
        self.label_p2.setScaledContents(True)
        self.label_p2.setObjectName("label_p2")
        self.label_p3 = QtWidgets.QLabel(self.frame)
        self.label_p3.setGeometry(QtCore.QRect(0, 500, 878, 111))
        self.label_p3.setText("")
        self.label_p3.setPixmap(QtGui.QPixmap("./icons/label.png"))
        self.label_p3.setScaledContents(True)
        self.label_p3.setObjectName("label_p3")
        self.label_people = QtWidgets.QLabel(self.frame)
        self.label_people.setGeometry(QtCore.QRect(80, 530, 81, 41))
        self.label_people.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "font: 12pt \"黑体\";")
        self.label_people.setAlignment(QtCore.Qt.AlignCenter)
        self.label_people.setObjectName("label_people")
        self.label_user = QtWidgets.QLabel(self.frame)
        self.label_user.setGeometry(QtCore.QRect(40, 530, 41, 41))
        self.label_user.setText("")
        self.label_user.setPixmap(QtGui.QPixmap("./icons/user (1).png"))
        self.label_user.setScaledContents(True)
        self.label_user.setObjectName("label_user")
        self.label_cv = QtWidgets.QLabel(self.frame)
        self.label_cv.setGeometry(QtCore.QRect(36, 37, 791, 441))
        self.label_cv.setStyleSheet("border-radius:10px;\n"
                                    "border: 2px solid rgb(52, 59, 72);")
        self.label_cv.setText("")
        self.label_cv.setObjectName("label_cv")
        self.btn_stop = QtWidgets.QPushButton(self.frame)
        self.btn_stop.setGeometry(QtCore.QRect(646, 518, 61, 61))
        self.btn_stop.setStyleSheet("QPushButton{\n"
                                    "    border: 2px solid rgb(52, 59, 72);\n"
                                    "    border-radius: 5px;\n"
                                    "    background-color: rgb(52, 59, 72);\n"
                                    "}\n"
                                    "QPushButton:hover{\n"
                                    "    background-color: rgb(57, 65, 80);\n"
                                    "    border: 2px solid rgb(61, 70, 86);\n"
                                    "}\n"
                                    "QPushButton:pressed{\n"
                                    "    background-color: rgb(35, 40, 49);\n"
                                    "    border: 2px solid rgb(43, 50, 61);\n"
                                    "}")
        self.btn_stop.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("./icons/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_stop.setIcon(icon6)
        self.btn_stop.setIconSize(QtCore.QSize(41, 41))
        self.btn_stop.setObjectName("btn_stop")
        self.btn_play = QtWidgets.QPushButton(self.frame)
        self.btn_play.setGeometry(QtCore.QRect(711, 518, 61, 61))
        self.btn_play.setStyleSheet("QPushButton{\n"
                                    "    border: 2px solid rgb(52, 59, 72);\n"
                                    "    border-radius: 5px;\n"
                                    "    background-color: rgb(52, 59, 72);\n"
                                    "}\n"
                                    "QPushButton:hover{\n"
                                    "    background-color: rgb(57, 65, 80);\n"
                                    "    border: 2px solid rgb(61, 70, 86);\n"
                                    "}\n"
                                    "QPushButton:pressed{\n"
                                    "    background-color: rgb(35, 40, 49);\n"
                                    "    border: 2px solid rgb(43, 50, 61);\n"
                                    "}")
        self.btn_play.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("./icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_play.setIcon(icon7)
        self.btn_play.setIconSize(QtCore.QSize(41, 41))
        self.btn_play.setObjectName("btn_play")
        self.btn_pause = QtWidgets.QPushButton(self.frame)
        self.btn_pause.setGeometry(QtCore.QRect(777, 518, 61, 61))
        self.btn_pause.setStyleSheet("QPushButton{\n"
                                     "    border: 2px solid rgb(52, 59, 72);\n"
                                     "    border-radius: 5px;\n"
                                     "    background-color: rgb(52, 59, 72);\n"
                                     "}\n"
                                     "QPushButton:hover{\n"
                                     "    background-color: rgb(57, 65, 80);\n"
                                     "    border: 2px solid rgb(61, 70, 86);\n"
                                     "}\n"
                                     "QPushButton:pressed{\n"
                                     "    background-color: rgb(35, 40, 49);\n"
                                     "    border: 2px solid rgb(43, 50, 61);\n"
                                     "}")
        self.btn_pause.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("./icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_pause.setIcon(icon8)
        self.btn_pause.setIconSize(QtCore.QSize(41, 41))
        self.btn_pause.setObjectName("btn_pause")
        self.spinbox_num = QtWidgets.QSpinBox(self.frame)
        self.spinbox_num.setGeometry(QtCore.QRect(380, 540, 71, 21))
        self.spinbox_num.setStyleSheet("QSpinBox{\n"
                                       "    border: 2px solid rgb(52, 59, 72);\n"
                                       "    border-radius: 5px;\n"
                                       "    background-color: rgb(52, 59, 72);\n"
                                       "    color: rgb(255, 255, 255);\n"
                                       "font: 13pt \"黑体\";}\n"
                                       "QSpinBox:up-button{\n"
                                       "image: url(./icons/add.png);\n"
                                       "    background-color: rgb(44, 49, 60);\n"
                                       "    subcontrol-position:right;\n"
                                       "    width:20px;\n"
                                       "    height:20px;\n"
                                       "\n"
                                       "}\n"
                                       "QSpinBox:down-button{\n"
                                       "    \n"
                                       "    image: url(./icons/line.png);\n"
                                       "    background-color: rgb(44, 49, 60);\n"
                                       "    subcontrol-position:left;\n"
                                       "    width:20px;\n"
                                       "    height:20px;\n"
                                       "}\n"
                                       "QSPinBox:up-button:hover{\n"
                                       "    background-color: rgb(57, 65, 80);\n"
                                       "    border: 2px solid rgb(61, 70, 86);\n"
                                       "}\n"
                                       "QSpinBox:up-button:pressed{\n"
                                       "    background-color: rgb(35, 40, 49);\n"
                                       "    border: 2px solid rgb(43, 50, 61);\n"
                                       "}\n"
                                       "QSPinBox:down-button:hover{\n"
                                       "    background-color: rgb(57, 65, 80);\n"
                                       "    border: 2px solid rgb(61, 70, 86);\n"
                                       "}\n"
                                       "QSpinBox:down-button:pressed{\n"
                                       "    background-color: rgb(35, 40, 49);\n"
                                       "    border: 2px solid rgb(43, 50, 61);\n"
                                       "}")
        self.spinbox_num.setAlignment(QtCore.Qt.AlignCenter)
        self.spinbox_num.setObjectName("spinbox_num")

        self.label_single = QtWidgets.QLabel(self.frame)
        self.label_single.setGeometry(QtCore.QRect(301, 534, 81, 31))
        self.label_single.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "font: 12pt \"黑体\";")
        self.label_single.setObjectName("label_single")
        self.btn_num = QtWidgets.QPushButton(self.frame)
        self.btn_num.setGeometry(QtCore.QRect(460, 535, 51, 31))
        self.btn_num.setStyleSheet("QPushButton{\n"
                                   "    border: 2px solid rgb(52, 59, 72);\n"
                                   "    border-radius: 5px;\n"
                                   "    background-color: rgb(52, 59, 72);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "font: 12pt \"黑体\";\n"
                                   "}\n"
                                   "QPushButton:hover{\n"
                                   "    background-color: rgb(57, 65, 80);\n"
                                   "    border: 2px solid rgb(61, 70, 86);\n"
                                   "}\n"
                                   "QPushButton:pressed{\n"
                                   "    background-color: rgb(35, 40, 49);\n"
                                   "    border: 2px solid rgb(43, 50, 61);\n"
                                   "}")
        self.btn_num.setObjectName("btn_num")
        self.btn_hide = QtWidgets.QPushButton(self)
        self.btn_hide.setGeometry(QtCore.QRect(290, 550, 35, 35))
        self.btn_hide.setStyleSheet("QPushButton{\n"
                                    "    border: 2px solid rgb(52, 59, 72);\n"
                                    "    border-radius: 5px;\n"
                                    "    background-color: rgb(52, 59, 72);\n"
                                    "}\n"
                                    "QPushButton:hover{\n"
                                    "    background-color: rgb(57, 65, 80);\n"
                                    "    border: 2px solid rgb(61, 70, 86);\n"
                                    "}\n"
                                    "QPushButton:pressed{\n"
                                    "    background-color: rgb(35, 40, 49);\n"
                                    "    border: 2px solid rgb(43, 50, 61);\n"
                                    "}")
        self.btn_hide.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("./icons/return.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_hide.setIcon(icon9)
        self.btn_hide.setFlat(True)
        self.btn_hide.setObjectName("btn_hide")
        self.label_degree = QtWidgets.QLabel(self)
        self.label_degree.setGeometry(QtCore.QRect(80, 440, 50, 50))
        self.label_degree.setText("")
        self.label_degree.setPixmap(QtGui.QPixmap("./icons/filter.png"))
        self.label_degree.setScaledContents(True)
        self.label_degree.setObjectName("label_degree")
        self.spinbox = QtWidgets.QDoubleSpinBox(self)
        self.spinbox.setEnabled(True)
        self.spinbox.setGeometry(QtCore.QRect(150, 450, 141, 31))
        self.spinbox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.spinbox.setAutoFillBackground(False)
        self.spinbox.setStyleSheet("QDoubleSpinBox{\n"
                                   "    border: 2px solid rgb(52, 59, 72);\n"
                                   "    border-radius: 5px;\n"
                                   "    background-color: rgb(52, 59, 72);\n"
                                   "    color: rgb(255, 255, 255);\n"
                                   "font: 13pt \"黑体\";}\n"
                                   "QDoubleSpinBox:up-button{\n"
                                   "    image: url(./icons/add.png);\n"
                                   "    background-color: rgb(44, 49, 60);\n"
                                   "    subcontrol-position:right;\n"
                                   "    width:30px;\n"
                                   "    height:30px;\n"
                                   "\n"
                                   "}\n"
                                   "QDoubleSpinBox:down-button{\n"
                                   "    \n"
                                   "    image: url(./icons/line.png);\n"
                                   "    background-color: rgb(44, 49, 60);\n"
                                   "    subcontrol-position:left;\n"
                                   "    width:30px;\n"
                                   "    height:30px;\n"
                                   "}\n"
                                   "QDoubleSPinBox:up-button:hover{\n"
                                   "    background-color: rgb(57, 65, 80);\n"
                                   "    border: 2px solid rgb(61, 70, 86);\n"
                                   "}\n"
                                   "QDoubleSpinBox:up-button:pressed{\n"
                                   "    background-color: rgb(35, 40, 49);\n"
                                   "    border: 2px solid rgb(43, 50, 61);\n"
                                   "}\n"
                                   "QDoubleSPinBox:down-button:hover{\n"
                                   "    background-color: rgb(57, 65, 80);\n"
                                   "    border: 2px solid rgb(61, 70, 86);\n"
                                   "}\n"
                                   "QDoubleSpinBox:down-button:pressed{\n"
                                   "    background-color: rgb(35, 40, 49);\n"
                                   "    border: 2px solid rgb(43, 50, 61);\n"
                                   "}")
        self.spinbox.setAlignment(QtCore.Qt.AlignCenter)
        self.spinbox.setReadOnly(False)
        self.spinbox.setMaximum(1.0)
        self.spinbox.setSingleStep(0.01)
        self.spinbox.setProperty("value", 0.5)
        self.spinbox.setObjectName("spinbox")

        self.btn_setting = QtWidgets.QPushButton(self)
        self.btn_setting.setGeometry(QtCore.QRect(40, 550, 35, 35))
        self.btn_setting.setStyleSheet("QPushButton{\n"
                                       "    border: 2px solid rgb(52, 59, 72);\n"
                                       "    border-radius: 5px;\n"
                                       "    background-color: rgb(52, 59, 72);\n"
                                       "}\n"
                                       "QPushButton:hover{\n"
                                       "    background-color: rgb(57, 65, 80);\n"
                                       "    border: 2px solid rgb(61, 70, 86);\n"
                                       "}\n"
                                       "QPushButton:pressed{\n"
                                       "    background-color: rgb(35, 40, 49);\n"
                                       "    border: 2px solid rgb(43, 50, 61);\n"
                                       "}")
        self.btn_setting.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("./icons/setting.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_setting.setIconSize(QtCore.QSize(30, 30))
        self.btn_setting.setIcon(icon10)
        self.btn_setting.setFlat(True)
        self.btn_setting.setObjectName("btn_setting")
        self.frame_setting = QtWidgets.QFrame(self)
        self.frame_setting.setGeometry(QtCore.QRect(350, 150, 271, 341))
        self.frame_setting.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_setting.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_setting.setObjectName("frame_setting")

        self.label_2 = QtWidgets.QLabel(self.frame_setting)
        self.label_2.setGeometry(QtCore.QRect(-20, -10, 311, 361))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("./icons/bg.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        self.btn_GPUoff = QtWidgets.QPushButton(self.frame_setting)
        self.btn_GPUoff.setGeometry(QtCore.QRect(150, 76, 51, 31))
        self.btn_GPUoff.setStyleSheet("QPushButton{\n"
                                      "    border: 2px solid rgb(52, 59, 72);\n"
                                      "    border-radius: 5px;\n"
                                      "    background-color: rgb(52, 59, 72);\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "font: 12pt \"黑体\";\n"
                                      "}\n"
                                      "QPushButton:hover{\n"
                                      "    background-color: rgb(57, 65, 80);\n"
                                      "    border: 2px solid rgb(61, 70, 86);\n"
                                      "}\n"
                                      "QPushButton:pressed{\n"
                                      "    background-color: rgb(35, 40, 49);\n"
                                      "    border: 2px solid rgb(43, 50, 61);\n"
                                      "}")
        self.btn_GPUoff.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("./icons/switch-OFF (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_GPUoff.setIcon(icon10)
        self.btn_GPUoff.setIconSize(QtCore.QSize(61, 41))
        self.btn_GPUoff.setObjectName("btn_GPUoff")
        self.label_setting_1 = QtWidgets.QLabel(self.frame_setting)
        self.label_setting_1.setGeometry(QtCore.QRect(70, 80, 71, 21))
        self.label_setting_1.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "font: 12pt \"黑体\";")
        self.label_setting_1.setObjectName("label_setting_1")

        self.label_setting_2 = QtWidgets.QLabel(self.frame_setting)
        self.label_setting_2.setGeometry(QtCore.QRect(40, 229, 111, 31))
        self.label_setting_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "font: 12pt \"黑体\";")
        self.label_setting_2.setObjectName("label_setting_2")

        self.btn_setting_close = QtWidgets.QPushButton(self.frame_setting)
        self.btn_setting_close.setGeometry(QtCore.QRect(222, 14, 35, 35))
        self.btn_setting_close.setStyleSheet("QPushButton{\n"
                                             "    border:none;\n"
                                             "    border-radius:6px;\n"
                                             "    background-color: transparent;\n"
                                             "}\n"
                                             "QPushButton:hover{\n"
                                             "    background-color: rgb(52, 59, 72);\n"
                                             "}\n"
                                             "QPushButton:pressed{\n"
                                             "    background-color: rgb(25, 40, 50);\n"
                                             "}")
        self.btn_setting_close.setText("")
        self.btn_setting_close.setIcon(icon)
        self.btn_setting_close.setFlat(True)
        self.btn_setting_close.setObjectName("btn_setting_close")
        self.btn_history = QtWidgets.QPushButton(self.frame_setting)
        self.btn_history.setGeometry(QtCore.QRect(60, 130, 151, 31))
        self.btn_history.setStyleSheet("QPushButton{\n"
                                       "    border: 2px solid rgb(52, 59, 72);\n"
                                       "    border-radius: 5px;\n"
                                       "    background-color: rgb(52, 59, 72);\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "font: 12pt \"黑体\";\n"
                                       "}\n"
                                       "QPushButton:hover{\n"
                                       "    background-color: rgb(57, 65, 80);\n"
                                       "    border: 2px solid rgb(61, 70, 86);\n"
                                       "}\n"
                                       "QPushButton:pressed{\n"
                                       "    background-color: rgb(35, 40, 49);\n"
                                       "    border: 2px solid rgb(43, 50, 61);\n"
                                       "}")
        self.btn_history.setObjectName("btn_history")

        self.btn_history1 = QtWidgets.QPushButton(self.frame_setting)
        self.btn_history1.setGeometry(QtCore.QRect(60, 170, 151, 31))
        self.btn_history1.setStyleSheet("QPushButton{\n"
                                        "    border: 2px solid rgb(52, 59, 72);\n"
                                        "    border-radius: 5px;\n"
                                        "    background-color: rgb(52, 59, 72);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "font: 12pt \"黑体\";\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "    background-color: rgb(57, 65, 80);\n"
                                        "    border: 2px solid rgb(61, 70, 86);\n"
                                        "}\n"
                                        "QPushButton:pressed{\n"
                                        "    background-color: rgb(35, 40, 49);\n"
                                        "    border: 2px solid rgb(43, 50, 61);\n"
                                        "}")
        self.btn_history1.setObjectName("btn_history1")

        self.btn_GPUon = QtWidgets.QPushButton(self.frame_setting)
        self.btn_GPUon.setGeometry(QtCore.QRect(150, 76, 51, 31))
        self.btn_GPUon.setStyleSheet("QPushButton{\n"
                                     "    border: 2px solid rgb(52, 59, 72);\n"
                                     "    border-radius: 5px;\n"
                                     "    background-color: rgb(52, 59, 72);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "font: 12pt \"黑体\";\n"
                                     "}\n"
                                     "QPushButton:hover{\n"
                                     "    background-color: rgb(57, 65, 80);\n"
                                     "    border: 2px solid rgb(61, 70, 86);\n"
                                     "}\n"
                                     "QPushButton:pressed{\n"
                                     "    background-color: rgb(35, 40, 49);\n"
                                     "    border: 2px solid rgb(43, 50, 61);\n"
                                     "}")
        self.btn_GPUon.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("./icons/switch-ON (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_GPUon.setIcon(icon11)
        self.btn_GPUon.setIconSize(QtCore.QSize(61, 41))
        self.btn_GPUon.setObjectName("btn_GPUon")

        self.spinbox_num_2 = QtWidgets.QSpinBox(self.frame_setting)
        self.spinbox_num_2.setGeometry(QtCore.QRect(160, 230, 61, 31))
        self.spinbox_num_2.setStyleSheet("QSpinBox{\n"
                                         "    border: 2px solid rgb(52, 59, 72);\n"
                                         "    border-radius: 5px;\n"
                                         "    background-color: rgb(52, 59, 72);\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "font: 13pt \"黑体\";}\n"
                                         "QSpinBox:up-button{\n"
                                         "image: url(./icons/add.png);\n"
                                         "    background-color: rgb(44, 49, 60);\n"
                                         "    subcontrol-position:right;\n"
                                         "    width:20px;\n"
                                         "    height:20px;\n"
                                         "\n"
                                         "}\n"
                                         "QSpinBox:down-button{\n"
                                         "    \n"
                                         "    image: url(./icons/line.png);\n"
                                         "    background-color: rgb(44, 49, 60);\n"
                                         "    subcontrol-position:left;\n"
                                         "    width:20px;\n"
                                         "    height:20px;\n"
                                         "}\n"
                                         "QSPinBox:up-button:hover{\n"
                                         "    background-color: rgb(57, 65, 80);\n"
                                         "    border: 2px solid rgb(61, 70, 86);\n"
                                         "}\n"
                                         "QSpinBox:up-button:pressed{\n"
                                         "    background-color: rgb(35, 40, 49);\n"
                                         "    border: 2px solid rgb(43, 50, 61);\n"
                                         "}\n"
                                         "QSPinBox:down-button:hover{\n"
                                         "    background-color: rgb(57, 65, 80);\n"
                                         "    border: 2px solid rgb(61, 70, 86);\n"
                                         "}\n"
                                         "QSpinBox:down-button:pressed{\n"
                                         "    background-color: rgb(35, 40, 49);\n"
                                         "    border: 2px solid rgb(43, 50, 61);\n"
                                         "}")
        self.spinbox_num_2.setAlignment(QtCore.Qt.AlignCenter)
        self.spinbox_num_2.setMinimum(1)
        self.spinbox_num_2.setMaximum(7)
        self.spinbox_num_2.setObjectName("spinbox_num_2")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.label_cv.setScaledContents(True)

        self.btn_hide.hide()
        self.btn_show.show()
        self.label_cv.hide()
        self.label_p2.hide()
        self.label_p3.hide()
        self.label_user.hide()
        self.label_people.hide()
        self.btn_play.hide()
        self.btn_pause.hide()
        self.btn_stop.hide()
        self.label_single.hide()
        self.spinbox_num.hide()
        self.btn_num.hide()
        self.spinbox_num_2.hide()
        self.label_setting_2.hide()

        self.label_2.hide()
        self.btn_GPUoff.hide()
        self.btn_GPUon.hide()
        self.btn_setting_close.hide()
        self.btn_history.hide()
        self.btn_history1.hide()
        self.label_setting_1.hide()

        self.btn_show.show()
        self.btn_hide.hide()

        self.btn_GPUon.clicked.connect(self.GPUoff)
        self.btn_GPUoff.clicked.connect(self.GPUon)
        self.btn_setting.clicked.connect(self.show_setting)
        self.btn_setting_close.clicked.connect(self.hide_setting)
        self.btn_close.clicked.connect(self.exit)
        self.btn_min.clicked.connect(self.mini)
        self.btn_hide.clicked.connect(self.hide_frame)
        self.btn_show.clicked.connect(self.show_frame)
        self.btn_video.clicked.connect(self.getVideoInfo)
        self.btn_image.clicked.connect(self.getImageInfo)
        self.btn_camera.clicked.connect(self.getCamera)
        self.btn_history.clicked.connect(self.history)
        self.btn_history1.clicked.connect(self.historyClean)
        self.btn_num.clicked.connect(self.singleDetect)
        self.btn_pause.clicked.connect(self.pause)
        self.btn_play.clicked.connect(self.play)
        self.btn_stop.clicked.connect(self.stop)

        self.threshold = self.spinbox.value()  # 置信度
        self.detectnum = self.spinbox_num_2.value()  # 检测视频个数

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "self"))
        self.label_name.setText(_translate("Form", "基于百度飞桨的单/多镜头行人追踪"))
        self.label_team.setText(_translate("Form", "——随便什么都队"))
        self.label_single.setText(_translate("Form", "单独追踪"))
        self.btn_num.setText(_translate("Form", "选中"))
        self.label_setting_1.setText(_translate("Form", "开启GPU"))
        self.label_setting_2.setText(_translate("Form", "检测视频个数"))
        self.btn_history.setText(_translate("Form", "历史回放"))
        self.btn_history1.setText(_translate("Form", "清除历史记录"))

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = e.globalPos() - self.pos()
            e.accept()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.m_drag = False

    def mouseMoveEvent(self, e):
        try:
            if Qt.LeftButton and self.m_drag:
                self.move(e.globalPos() - self.m_DragPosition)
                e.accept()
        except:
            pass

    def exit(self):  # 退出
        def Thread():
            for i in reversed(range(0, 11)):
                self.setWindowOpacity(i / 10)
                time.sleep(0.02)
            os._exit(-1)

        Thread = threading.Thread(target=Thread)
        Thread.start()

    def mini(self):  # 最小化
        def Thread():
            for i in reversed(range(0, 11)):
                self.setWindowOpacity(i / 10)
                time.sleep(0.02)
            self.showMinimized()
            self.setWindowOpacity(1)

        Thread = threading.Thread(target=Thread)
        Thread.start()

    def hide_frame(self):
        self.anim = QPropertyAnimation(self.frame, b"geometry")
        self.anim.setDuration(200)
        self.anim.setStartValue(QRect(339, 14, 891, 611))
        self.anim.setEndValue(QRect(10, 14, 1, 611))
        self.anim.start()
        self.btn_hide.hide()
        self.btn_show.show()
        self.label_cv.hide()
        self.label_p2.hide()
        self.label_p3.hide()
        self.label_user.hide()
        self.label_people.hide()
        self.btn_play.hide()

        self.btn_pause.hide()
        self.btn_stop.hide()
        self.label_single.hide()
        self.spinbox_num.hide()
        self.btn_num.hide()

    def show_frame(self):
        self.anim = QPropertyAnimation(self.frame, b"geometry")
        self.anim.setDuration(200)
        self.anim.setStartValue(QRect(10, 14, 1, 611))
        self.anim.setEndValue(QRect(339, 14, 8091, 611))
        self.anim.start()
        self.btn_hide.show()
        self.btn_show.hide()
        self.label_cv.show()

        self.label_p2.show()
        self.label_p3.show()
        self.label_user.show()
        self.label_people.show()
        self.btn_play.show()
        self.btn_pause.show()
        self.btn_stop.show()
        self.label_single.show()
        self.spinbox_num.show()
        self.btn_num.show()

    def show_setting(self):
        # self.anim2 = QPropertyAnimation(self.frame, b"geometry")
        # self.anim2.setDuration(200)
        # self.anim2.setStartValue(QRect(40, 550, 35, 35))
        # self.anim2.setEndValue(QRect(50, 150, 271, 341))
        # self.anim2.start()
        self.label_2.show()
        if self.setting_flag == 1:
            self.btn_GPUon.show()
        else:
            self.btn_GPUoff.show()
        self.btn_setting_close.show()
        self.btn_history.show()
        self.label_setting_2.show()
        self.label_setting_1.show()
        self.spinbox_num_2.show()
        self.btn_history1.show()
        self.btn_show.setEnabled(False)
        self.btn_hide.setEnabled(False)
        self.btn_camera.setEnabled(False)
        self.btn_image.setEnabled(False)
        self.btn_video.setEnabled(False)
        self.btn_num.setEnabled(False)
        self.btn_play.setEnabled(False)
        self.btn_pause.setEnabled(False)
        self.btn_stop.setEnabled(False)
        self.spinbox.setEnabled(False)
        self.spinbox_num.setEnabled(False)
        self.btn_setting.setEnabled(False)

    def hide_setting(self):
        global index
        # self.anim1 = QPropertyAnimation(self.frame, b"geometry")
        # self.anim1.setDuration(200)
        # self.anim1.setStartValue(QRect(50, 150, 271, 341))
        # self.anim1.setEndValue(QRect(40, 550, 35, 35))
        # self.anim1.start()
        self.detectnum = self.spinbox_num_2.value()  # 检测视频个数
        index = self.detectnum
        self.label_2.hide()
        self.btn_GPUoff.hide()
        self.btn_GPUon.hide()
        self.btn_setting_close.hide()
        self.btn_history.hide()
        self.btn_history1.hide()
        self.spinbox_num_2.hide()
        self.label_setting_2.hide()
        self.label_setting_1.hide()
        self.btn_show.setEnabled(True)
        self.btn_hide.setEnabled(True)
        self.btn_camera.setEnabled(True)
        self.btn_image.setEnabled(True)
        self.btn_video.setEnabled(True)
        self.btn_num.setEnabled(True)
        self.btn_play.setEnabled(True)
        self.btn_pause.setEnabled(True)
        self.btn_stop.setEnabled(True)
        self.spinbox.setEnabled(True)
        self.spinbox_num.setEnabled(True)
        self.btn_setting.setEnabled(True)
        self.videoName = []
        global video_list
        video_list =[]

    def GPUon(self):   #开启GPU
        global is_open
        is_open = 1
        self.btn_GPUoff.hide()
        self.btn_GPUon.show()
        self.setting_flag = True
    #is_open == 1为GPU开启状态（默认开启），为0时为关闭状态

    def GPUoff(self):  #关闭GPU
        global is_open
        is_open = 0
        self.btn_GPUon.hide()
        self.btn_GPUoff.show()
        self.setting_flag = False

    def getImageInfo(self):
        global imgPath
        _translate = QtCore.QCoreApplication.translate
        self.show_frame()
        imgPath, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        if imgPath!='':
            self.work4.start()
            time.sleep(8)
            self.label_cv.setPixmap(QPixmap('./frame/00000.jpg'))
            self.label_people.setText(_translate("Form", "人数："+ people_num1()))

    def getVideoInfo(self):
        global video_list
        self.show_frame()
        if self.detectnum !=1 :
            self.detectnum -= 1
        else:
            self.btn_video.setEnabled(False)
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开视频", "", "*.mp4;;*.AVI;;*.rmvb;;All Files(*)")
        self.videoName.append(imgName)
        video_list = self.videoName
        #------------------------------------------------

    def getCamera(self):
        self.show_frame()
        self.work3.start()
        self.work.start()
        self.autoSubmitCloseOrder()

    def pause(self):
        pass

    def start_camera(self):
        re_start()
        os.system('python delet.py')
        start_camera()

    def start_video(self):
        global video_list, index
        if index == 1:
            start_video1(self.threshold, video_list[0])
        if index == 2:
            start_video2(self.threshold, video_list[0], video_list[1])
        if index == 3:
            start_video3(self.threshold, video_list[0], video_list[1], video_list[2])
        if index == 4:
            start_video4(self.threshold, video_list[0], video_list[1], video_list[2], video_list[3])
        if index == 5:
            start_video5(self.threshold, video_list[0], video_list[1], video_list[2], video_list[3], video_list[4])
        if index == 6:
            start_video6(self.threshold, video_list[0], video_list[1], video_list[2], video_list[3], video_list[4], video_list[5])
        if index == 7:
            start_video7(self.threshold, video_list[0], video_list[1], video_list[2], video_list[3], video_list[4], video_list[5],video_list[6])


    def start_image(self):
        global imgPath
        start_image(imgPath, self.threshold)



    def show_image(self,i):
        _translate = QtCore.QCoreApplication.translate
        global num
        self.label_cv.setPixmap(QPixmap('./frame/' + str(i).zfill(5) + '.jpg'))
        conn = sqlite3.connect("people_num.db")
        cur = conn.cursor()
        cursor = conn.execute("SELECT * from  num where rowid==%d "%int(i))
        for i in cursor:
            num = i[0]
        conn.commit()
        self.label_people.setText(_translate("Form", "人数："+str(num)))
        cur.close()
        conn.close()


    def autoSubmitCloseOrder(self):
        second = 0
        while True:
            QApplication.processEvents()
            time.sleep(0.1)
            second += 1
            if second % 10 == 0:
                print(datetime.datetime.now())

    def history(self):  # 历史记录
        self.show_frame()
        self.work.start()
        self.autoSubmitCloseOrder()

    def historyClean(self): # 删除历史记录
        shutil.rmtree('frame')
        os.mkdir('frame')
        conn = sqlite3.connect("people_num.db")
        cur = conn.cursor()
        sql = '''
            delete from "num";
        '''
        cur.execute(sql)
        conn.commit()

        cur.close()
        conn.close()

    def singleDetect(self):  # 单个行人追踪
        one_num = self.spinbox_num.value()  # num为所输入编号
        find_one(one_num)


    def pause(self):
        return

    def play(self):
        re_start()
        os.system('python delet.py')
        self.work2.start()
        self.work.start()
        self.autoSubmitCloseOrder()

    def stop(self):
        stop()
        self.work.terminate()

import sys

def is_true():
    global is_open
    if is_open == 1:
        return True
    else:
        return False

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = Ui_self()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
