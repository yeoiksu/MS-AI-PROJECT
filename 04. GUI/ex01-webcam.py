import cv2, threading, sys, numpy as np, torch, time, argparse, os, glob
from torch import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os
import sys

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

'''ui폼 받아오기'''
# Main
### 추후 업데이트 예정
# Email
form_2 = resource_path('ex02_email.ui')
form_email = uic.loadUiType(form_2)[0]
# DataBase
form_3 = resource_path('ex03_db.ui')
form_db = uic.loadUiType(form_3)[0]
# bi
form_4 = resource_path('ex04_bi.ui')
form_bi = uic.loadUiType(form_4)[0]

class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Hazardous Flying Object Detection")
        MainWindow.resize(1120, 629)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.box_cctv = QtWidgets.QGroupBox(self.centralwidget)
        self.box_cctv.setGeometry(QtCore.QRect(20, 30, 271, 181))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.box_cctv.setFont(font)
        self.box_cctv.setObjectName("box_cctv")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.box_cctv)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 251, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_cctv = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_cctv.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_cctv.setObjectName("horizontalLayout_cctv")
        self.pushButton_cctv_on = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)

        '''웹캠 동작 클릭 이벤트'''
        self.pushButton_cctv_on.setFont(font)
        self.pushButton_cctv_on.setMouseTracking(False)
        self.pushButton_cctv_on.setAutoDefault(False)
        self.pushButton_cctv_on.setDefault(False)
        self.pushButton_cctv_on.setObjectName("pushButton_cctv_on")
        self.pushButton_cctv_on.clicked.connect(self.live_webcam_click_on) # 웹캠 동작시키는 클릭 이벤트 처리 연결

        self.horizontalLayout_cctv.addWidget(self.pushButton_cctv_on)
        self.pushButton_cctv_off = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)

        '''웹캠 종료 클릭 이벤트'''
        self.pushButton_cctv_off.setFont(font)
        self.pushButton_cctv_off.setObjectName("pushButton_cctv_off")
        self.pushButton_cctv_off.clicked.connect(self.live_webcam_click_off) # 웹캠 종료시키는 클릭 이벤트 처리 연결(디바이스 자체의 카메라가 꺼지진 않음 = 웹캠 불 들어옴)

        self.horizontalLayout_cctv.addWidget(self.pushButton_cctv_off)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.box_cctv)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 80, 121, 94))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_drone = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_drone.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_drone.setObjectName("verticalLayout_drone")
        self.checkBox_drone = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_drone.setFont(font)
        self.checkBox_drone.setObjectName("checkBox_drone")
        self.verticalLayout_drone.addWidget(self.checkBox_drone)
        self.checkBox_airplane = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_airplane.setFont(font)
        self.checkBox_airplane.setObjectName("checkBox_airplane")
        self.verticalLayout_drone.addWidget(self.checkBox_airplane)
        self.checkBox_helicopter = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_helicopter.setFont(font)
        self.checkBox_helicopter.setObjectName("checkBox_helicopter")
        self.verticalLayout_drone.addWidget(self.checkBox_helicopter)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.box_cctv)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(140, 80, 121, 94))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_military = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_military.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_military.setObjectName("verticalLayout_military")
        self.checkBox_military = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_military.setFont(font)
        self.checkBox_military.setObjectName("checkBox_military")
        self.verticalLayout_military.addWidget(self.checkBox_military)
        self.checkBox_bird = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_bird.setFont(font)
        self.checkBox_bird.setObjectName("checkBox_bird")
        self.verticalLayout_military.addWidget(self.checkBox_bird)
        self.checkBox_balloon = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_balloon.setFont(font)
        self.checkBox_balloon.setObjectName("checkBox_balloon")
        self.verticalLayout_military.addWidget(self.checkBox_balloon)
        
        '''Live Webcam 공간 부분'''
        self.box_webcam = QtWidgets.QGroupBox(self.centralwidget)
        self.box_webcam.setGeometry(QtCore.QRect(320, 30, 771, 491))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.box_webcam.setFont(font)
        self.box_webcam.setObjectName("box_webcam")

        '''실제 카메라 화면 출력 부분'''
        self.frame = QCameraViewfinder(self.box_webcam)
        self.frame.setGeometry(QtCore.QRect(10, 30, 751, 451))
        # self.frame.setFrameShape(QtWidgets.StyledPanel)
        # self.frame.setFrameShadow(QtWidgets.Raised)
        self.frame.setObjectName("frame")
        
        self.box_email = QtWidgets.QGroupBox(self.centralwidget)
        self.box_email.setGeometry(QtCore.QRect(20, 230, 271, 80))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.box_email.setFont(font)
        self.box_email.setObjectName("box_email")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.box_email)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 251, 51))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_email = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_email.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_email.setObjectName("horizontalLayout_email")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_email.addItem(spacerItem)
        self.pushButton_email = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)

        '''이메일 버튼 클릭'''
        self.pushButton_email.setFont(font)
        self.pushButton_email.setObjectName("pushButton_email")
        self.horizontalLayout_email.addWidget(self.pushButton_email)
        self.pushButton_email.clicked.connect(self.email_clicked) ### 이메일 버튼 클릭 이벤트 처리 연결


        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_email.addItem(spacerItem1)
        self.box_database = QtWidgets.QGroupBox(self.centralwidget)
        self.box_database.setGeometry(QtCore.QRect(20, 330, 271, 80))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.box_database.setFont(font)
        self.box_database.setObjectName("box_database")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.box_database)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 20, 251, 51))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_database = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_database.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_database.setObjectName("horizontalLayout_database")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_database.addItem(spacerItem2)
        self.pushButton_database = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)

        '''Database버튼 클릭'''
        self.pushButton_database.setFont(font)
        self.pushButton_database.setObjectName("pushButton_database")
        self.horizontalLayout_database.addWidget(self.pushButton_database)
        self.pushButton_database.clicked.connect(self.db_clicked)

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_database.addItem(spacerItem3)
        self.box_data = QtWidgets.QGroupBox(self.centralwidget)
        self.box_data.setGeometry(QtCore.QRect(20, 440, 271, 80))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.box_data.setFont(font)
        self.box_data.setObjectName("box_data")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.box_data)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(10, 20, 251, 51))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_data = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_data.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_data.setObjectName("horizontalLayout_data")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_data.addItem(spacerItem4)
        self.pushButton_data = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)

        '''Data Analysis(BI)버튼 클릭'''
        self.pushButton_data.setFont(font)
        self.pushButton_data.setObjectName("pushButton_data")
        self.horizontalLayout_data.addWidget(self.pushButton_data)
        self.pushButton_data.clicked.connect(self.bi_clicked)

        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_data.addItem(spacerItem5)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(320, 530, 771, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_capture = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_capture.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("04. GUI/pics/capture.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_capture.setIcon(icon)
        self.pushButton_capture.setObjectName("pushButton_capture")
        self.horizontalLayout.addWidget(self.pushButton_capture)
        self.pushButton_save = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_save.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("04. GUI/pics/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_save.setIcon(icon1)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout.addWidget(self.pushButton_save)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalSlider = QtWidgets.QSlider(self.horizontalLayoutWidget_2)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.label_thres_value = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        self.label_thres_value.setFont(font)
        self.label_thres_value.setObjectName("label_thres_value")
        self.horizontalLayout.addWidget(self.label_thres_value)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.pushButton_exit = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_exit.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("04. GUI/pics/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_exit.setIcon(icon2)
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.horizontalLayout.addWidget(self.pushButton_exit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setCheckable(False)
        self.actionExit.setIcon(icon2)
        self.actionExit.setObjectName("actionExit")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("04. GUI/pics/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon3)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setIcon(icon1)
        self.actionSave.setObjectName("actionSave")
        self.actionPrint = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("04. GUI/pics/print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrint.setIcon(icon4)
        self.actionPrint.setObjectName("actionPrint")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.horizontalSlider.valueChanged['int'].connect(self.label_thres_value.setNum) # type: ignore
        self.pushButton_exit.clicked.connect(MainWindow.close) # type: ignore
        self.menubar.triggered['QAction*'].connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton_cctv_on, self.pushButton_cctv_off)
        MainWindow.setTabOrder(self.pushButton_cctv_off, self.checkBox_drone)
        MainWindow.setTabOrder(self.checkBox_drone, self.checkBox_airplane)
        MainWindow.setTabOrder(self.checkBox_airplane, self.checkBox_helicopter)
        MainWindow.setTabOrder(self.checkBox_helicopter, self.checkBox_military)
        MainWindow.setTabOrder(self.checkBox_military, self.checkBox_bird)
        MainWindow.setTabOrder(self.checkBox_bird, self.checkBox_balloon)
        MainWindow.setTabOrder(self.checkBox_balloon, self.pushButton_email)
        MainWindow.setTabOrder(self.pushButton_email, self.pushButton_database)
        MainWindow.setTabOrder(self.pushButton_database, self.pushButton_data)
        MainWindow.setTabOrder(self.pushButton_data, self.pushButton_capture)
        MainWindow.setTabOrder(self.pushButton_capture, self.pushButton_save)
        MainWindow.setTabOrder(self.pushButton_save, self.horizontalSlider)
        MainWindow.setTabOrder(self.horizontalSlider, self.pushButton_exit)

    '''컴퓨터에 연결된 카메라가 있는지 없는지 판정하는 함수'''
    def camera_mode(self) : 
        self.available_cameras = QCameraInfo.availableCameras()
        if not self.available_cameras :
            sys.exit() # 연결된 카메라 없으면 종료

    '''컴퓨터에 연결된 카메라 중 index를 주어 i번 카메라 선택하는 함수'''
    def select_camera(self, i) :
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.frame) # 이 부분 빠지면 웹캠 화면 안 나오는 거 확인됨
        self.camera.start()

    '''off 버튼 눌렀을 시 웹캠 종료'''
    def live_webcam_click_off(self) :
        self.frame.hide() # 정확히는 숨김 처리 --> 노트북에 웹캠 불은 들어오고 있는 거 확인됨
        QMessageBox.about(self, 'App Alert', '연결된 카메라를 끕니다.')        
        

    '''on 버튼 눌렀을 시 웹캠 시작'''
    def live_webcam_click_on(self) :
        self.camera_mode() # 이 부분 빠지면 on 버튼 누르자마자 프로그램 종료됨
        QMessageBox.about(self, 'App Alert', '연결된 카메라를 킵니다.')
        self.select_camera(0) # 0번이 노트북에 연결된 웹캠이며, 이 부분 빠지면 마찬가지로 on 버튼 누르자마자 프로그램 종료됨
        self.frame.show()
    
    '''이메일 버튼 클릭 시 이메일 창으로 이동'''
    def email_clicked(self):
        # self.hide() # 메인윈도우 숨김
        self.second = email_form() 
        self.second.exec() # 두번째 창을 닫을 때 까지 기다림
        # self.show()  

    '''Database 버튼 클릭 시 DB창으로 이동'''
    def db_clicked(self):
        # self.hide() # 메인윈도우 숨김
        self.second = db_form() 
        self.second.exec() # 두번째 창을 닫을 때 까지 기다림
        # self.show()  

    '''Data Analysis 버튼 클릭 시 DB창으로 이동'''
    def bi_clicked(self):
        # self.hide() # 메인윈도우 숨김
        self.second = bi_form() 
        self.second.exec() # 두번째 창을 닫을 때 까지 기다림
        # self.show()  

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "위험 비행물 탐지 시스템"))
        self.box_cctv.setTitle(_translate("MainWindow", "01. CCTV Mode"))
        self.pushButton_cctv_on.setText(_translate("MainWindow", "on"))
        self.pushButton_cctv_off.setText(_translate("MainWindow", "off"))
        self.checkBox_drone.setText(_translate("MainWindow", "Drone"))
        self.checkBox_airplane.setText(_translate("MainWindow", "Airplane"))
        self.checkBox_helicopter.setText(_translate("MainWindow", "Helicopter"))
        self.checkBox_military.setText(_translate("MainWindow", "Military Drone"))
        self.checkBox_bird.setText(_translate("MainWindow", "Bird"))
        self.checkBox_balloon.setText(_translate("MainWindow", "Balloon"))
        self.box_webcam.setTitle(_translate("MainWindow", "Live Webcam"))
        self.box_email.setTitle(_translate("MainWindow", "02. Email System"))
        self.pushButton_email.setText(_translate("MainWindow", "Start"))
        self.box_database.setTitle(_translate("MainWindow", "03. Database"))
        self.pushButton_database.setText(_translate("MainWindow", "Start"))
        self.box_data.setTitle(_translate("MainWindow", "04. Data Analysis"))
        self.pushButton_data.setText(_translate("MainWindow", "Start"))
        self.pushButton_capture.setText(_translate("MainWindow", "Capture"))
        self.pushButton_save.setText(_translate("MainWindow", "Save"))
        self.label.setText(_translate("MainWindow", "Confidence Value"))
        self.label_thres_value.setText(_translate("MainWindow", "<html><head/><body><p>Value</p></body></html>"))
        self.pushButton_exit.setText(_translate("MainWindow", "Exit"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionPrint.setText(_translate("MainWindow", "Print"))
        self.actionPrint.setShortcut(_translate("MainWindow", "Ctrl+P")) 

'''email창 이동을 위한 클래스 추가'''
class email_form(QDialog,QWidget,form_email):
    def __init__(self):
        super(email_form,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    '''X버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore() 


'''Database창 이동을 위한 클래스 추가'''
class db_form(QDialog,QWidget,form_db):
    def __init__(self):
        super(db_form,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    '''X버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore() 


'''Data Analysis창 이동을 위한 클래스 추가'''
class bi_form(QDialog,QWidget,form_bi):
    def __init__(self):
        super(bi_form,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    '''X버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore() 

'''X버튼 누를 시 종료 재확인 메세지'''
def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
    ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if ans == QMessageBox.Yes:
        QCloseEvent.accept()
    else:
        QCloseEvent.ignore()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    '''상태표시줄'''
    MainWindow.statusBar()
    MainWindow.statusBar().showMessage("위험 비행물 탐지 시스템 동작합니다.")
    MainWindow.show()
    sys.exit(app.exec_())
