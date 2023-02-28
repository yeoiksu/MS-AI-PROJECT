import os
import sys
import cv2, threading, sys, numpy as np, torch, time, argparse, os, glob
from torch import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

'''ui폼 받아오기'''
# Main
form = resource_path('ex01.ui')
form_class = uic.loadUiType(form)[0]
# Email
form_2 = resource_path('ex02_email.ui')
form_email = uic.loadUiType(form_2)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        ''' 웹캠 동작(종료)시키는 클릭 이벤트 처리 연결'''
        self.pushButton_cctv_on.clicked.connect(self.live_webcam_click_on)  # 동작
        self.pushButton_cctv_off.clicked.connect(self.live_webcam_click_off) # 종료

    ''' email버튼 클릭 시 이메일 창 활성화'''    
    def email_clicked(self):
        # self.hide() # 메인윈도우 숨김
        self.second = email_form()
        self.second.exec() # 두번째 창을 닫을 때 까지 기다림
        self.show()  

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

        ''' 실제 카메라 화면 출력 부분'''
        self.frame = QCameraViewfinder(self.box_webcam)
        self.frame.setGeometry(QtCore.QRect(10, 30, 751, 451))
        # self.frame.setFrameShape(QtWidgets.StyledPanel)
        # self.frame.setFrameShadow(QtWidgets.Raised)
        self.frame.setObjectName("frame")

        
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


    '''X버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    
    '''상태표시줄'''
    myWindow.statusBar()
    myWindow.statusBar().showMessage("위험 비행물 감지 시스템 동작합니다.")
    app.exec_()