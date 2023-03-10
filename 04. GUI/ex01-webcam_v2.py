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
from important_data import *
import qdarktheme
from qt_material import list_themes
from qt_material import apply_stylesheet


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


# 버튼 색상 및 폰트
extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font_family': 'Roboto',
}

# Ui 디자인 작업 중
class Ui_MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        '''Ui 디자인'''
        # apply_stylesheet(app, theme='dark_purple.xml') # 검은색 테마
        # qdarktheme.setup_theme("light")  # 밝은색 테마
        apply_stylesheet(app, theme='dark_purple.xml', extra=extra) # 검은색 테마 + 버튼 색상 + 폰트
        # apply_stylesheet(app, 'light_cyan.xml', invert_secondary=True, extra=extra) # 밝은색 테마 + 버튼 색상 + 폰트
        # stylesheet = qdarktheme.setup_theme(corner_shape="sharp") # 버튼 모양 각지게
        # qdarktheme.setup_theme("auto") # os테마와 동기화

        # dark_palette = qdarktheme.load_palette()
        # link_color = dark_palette.link().color()
        # link_rgb = link_color.getRgb()
        # app.setPalette(qdarktheme.load_palette())

        self.setupUi(self)
        ''' 버튼 아이콘 '''
        # save
        myWindow = QMainWindow()
        save_pixmap = QStyle.StandardPixmap.SP_DialogSaveButton
        save_icon = myWindow.style().standardIcon(save_pixmap)
        self.pushButton_save.setIcon(save_icon)

        # capture
        capture_pixmap = QStyle.StandardPixmap.SP_DialogApplyButton
        capture_icon = myWindow.style().standardIcon(capture_pixmap)
        self.pushButton_capture.setIcon(capture_icon)

        # exit
        exit_pixmap = QStyle.StandardPixmap.SP_MessageBoxCritical
        exit_icon = myWindow.style().standardIcon(exit_pixmap)
        self.pushButton_exit.setIcon(exit_icon)

        ''' 웹캠 동작(종료)시키는 클릭 이벤트 처리 연결'''
        self.pushButton_cctv_on.clicked.connect(self.live_webcam_click_on)  # 동작
        self.pushButton_cctv_off.clicked.connect(self.live_webcam_click_off) # 종료 

        # '''Live Webcam 공간 부분'''
        # self.box_webcam = QtWidgets.QGroupBox(self.centralwidget)
        # self.box_webcam.setGeometry(QtCore.QRect(320, 30, 771, 491))
        # font = QtGui.QFont()
        # font.setFamily("Yu Gothic UI Semibold")
        # font.setPointSize(10)
        # font.setBold(True)
        # font.setWeight(75)
        # self.box_webcam.setFont(font)
        # self.box_webcam.setObjectName("box_webcam")

        ''' 실제 카메라 화면 출력 부분'''
        self.frame = QCameraViewfinder(self.box_webcam)
        self.frame.setGeometry(QtCore.QRect(10, 30, 751, 451))
        # self.frame.setFrameShape(QtWidgets.StyledPanel)
        # self.frame.setFrameShadow(QtWidgets.Raised)
        self.frame.setObjectName("frame")


    '''on 버튼 눌렀을 시 웹캠 시작'''
    def live_webcam_click_on(self, i) :
        self.available_cameras = QCameraInfo.availableCameras()
        if not self.available_cameras :
            sys.exit() # 연결된 카메라 없으면 종료
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.frame)
        self.camera.start()
        QMessageBox.about(self, 'App Alert', '연결된 카메라를 킵니다.')
        # import yolov8_tracking.track as track
        self.frame.show()

    '''off 버튼 눌렀을 시 웹캠 종료'''
    def live_webcam_click_off(self) :
        QMessageBox.about(self, 'App Alert', '연결된 카메라를 끕니다.')
        self.frame.hide() # 정확히는 숨김 처리 --> 노트북에 웹캠 불은 들어오고 있는 거 확인됨 
        
    '''X버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


    # 2번 버튼
    ''' email버튼 클릭 시 이메일 창 활성화'''    
    def email_clicked(self):
        # self.hide() # 메인윈도우 숨김
        self.second = email_form()
        self.second.exec() # 두번째 창을 닫을 때 까지 기다림
        self.show() 

    # 3번 버튼
    '''Data Analysis 버튼 클릭 시 DB창으로 이동'''
    def bi_clicked(self):
        # self.hide() # 메인윈도우 숨김
        self.second = connect_powerbi() 
        # self.second.exec() # 두번째 창을 닫을 때 까지 기다림
        # self.show() 

## 2번 버튼 ####

'''CUSTOMER_TABLE 연결'''
def connect_table():
    from mysql.connector import connection
    conn = connection.MySQLConnection(
        user     = USER,
        password = PASSWORD,
        host     = HOST,
        database = DATABASE
        )
    return conn


'''Count Data'''
def countData(id= None, name= None, email= None, table_name= None, mode= None):
    conn = connect_table()
    cur = conn.cursor()    
    print("mode", mode)
    # COUNT 문
    if mode == " SELECT":
        SQL_COUNT = f'''SELECT COUNT(*) FROM `{table_name}`
        WHERE `id` = '{str(id)}' OR `name`='{str(name)}' OR `email`='{str(email)}';'''
    elif mode == " DELETE":
        SQL_COUNT = f'''SELECT COUNT(*) FROM `{table_name}`
        WHERE `id` = '{str(id)}' AND `name`='{str(name)}' AND `email`='{str(email)}';'''

    cur.execute(SQL_COUNT)
    count = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return count

''' Select Data'''
def SelectData(id= None, name= None, email= None, table_name= None):
    id_list, name_list, email_list = [], [], []

    conn = connect_table()
    cur = conn.cursor()
    SQL_SELECT = f'''SELECT * FROM `{table_name}`
    WHERE `id` = '{str(id)}' OR `name`='{str(name)}' OR `email`='{str(email)}';'''
    cur.execute(SQL_SELECT)
    result = cur.fetchall()
    for i in result:
        id_list.append(i[1])
        name_list.append(i[2])
        email_list.append(i[3])
    conn.commit()
    conn.close()

    return id_list, name_list, email_list

''' Insert Data'''
def InsertData(id= None, name= None, email= None, table_name= None):
    conn = connect_table()
    cur = conn.cursor()
    SQL_INSERT = f'''INSERT INTO `{table_name}`(id, name, email) 
VALUES ('{str(id)}', '{str(name)}', '{str(email)}');'''
    cur.execute(SQL_INSERT)
    conn.commit()
    conn.close()
    
''' Delete Data'''
def DeleteData(id= None, name= None, email= None, table_name= None):
    conn = connect_table()
    cur = conn.cursor()
    SQL_DELETE = f'''DELETE FROM `{table_name}` WHERE `id` = '{str(id)}' AND `name`='{str(name)}' AND `email`='{str(email)}';'''
    cur.execute(SQL_DELETE)
    conn.commit()
    if cur.rowcount >= 1:
        conn.close()
        return True
    else:
        conn.close()
        return False    

# WHERE  `id`='2' AND `name`='1' AND `email`='3' LIMIT 1;

####################################################################

'''2번 버튼, email 클래스 추가'''
class email_form(QDialog,QWidget,form_email):
    def __init__(self):
        super(email_form,self).__init__()
        self.initUi()
        self.show()
        print(self.info_comboBox.currentText(), '모드 입니다.')
        self.info_comboBox.currentIndexChanged.connect(self.printShtname)


    def initUi(self):
        self.setupUi(self)
        '''버튼 아이콘'''
        # enter
        capture_pixmap = QStyle.StandardPixmap.SP_DialogApplyButton
        capture_icon = myWindow.style().standardIcon(capture_pixmap)
        self.enter_pushButton.setIcon(capture_icon)

        # exit
        exit_pixmap = QStyle.StandardPixmap.SP_MessageBoxCritical
        exit_icon = myWindow.style().standardIcon(exit_pixmap)
        self.exit_pushButton.setIcon(exit_icon)
        

    '''info 입력/검색/삭제 부분 업데이트 중'''
####################################################################
    def reset(self):
        self.id_text.clear()
        self.name_text.clear()
        self.email_text.clear()  

    # def printShtname(self): # 콤보박스 상태 변경 시 터미널에 출력하는 기능 함수.
    #     print(self.info_comboBox.currentText(),'모드 입니다.')

    def add_info(self):
        set_flag = False

        fn_type = self.info_comboBox.currentText()  # 콤보 박스: 입력, 검색, 삭제
        id      = self.id_text.text()    # 아이디
        name    = self.name_text.text()  # 이름
        email   = self.email_text.text() # 이메일
        
        ## 1. 검색
        if fn_type == ' SELECT':
            if id or name or email:
                select_count = countData(id, name, email, TABLE_CUSTOMER, fn_type)
                if select_count > 0 :
                    set_flag = True
                    id_list, name_list, email_list = \
                        SelectData(
                            id    = id, 
                            name  = name,
                            email = email,
                            table_name= TABLE_CUSTOMER
                        )
                    QMessageBox.information(self, "Select 결과", f"{select_count}개의 데이터를 출력합니다.")
                else:
                    QMessageBox.critical(self, "입력 오류", "입력하신 정보의 데이터가 없습니다")
            else:
                QMessageBox.critical(self, "입력 오류", "정보를 입력해주세요!")
        
        ## 2. 입력
        elif fn_type == ' INSERT':
            if id and name and email:
                set_flag = True
                InsertData(
                    id    = id, 
                    name  = name,
                    email = email,
                    table_name= TABLE_CUSTOMER
                    )
            # close event 처럼 하나 필요 !!!
            else:
                QMessageBox.critical(self, "입력 오류", "모든 정보를 입력해주세요!")
                print("모든 정보를 입력해주세요!")

        ## 3. 삭제
        elif fn_type == ' DELETE':
            msg = '정말 삭제하시겠습니까?'
            buttonReply = QMessageBox.question(self, '삭제', msg, QMessageBox.Yes | QMessageBox.No)

            # 삭제 메세지에서 YES선택 시
            if buttonReply == QMessageBox.Yes:
                # 3개의 데이터 중 하나만이라도 존재하면
                if id and name and email:
                    delete_count = countData(id, name, email, TABLE_CUSTOMER, fn_type)
                    # delete할 행이 있다면
                    if delete_count > 0 :
                        set_flag = DeleteData(
                            id    = id, 
                            name  = name,
                            email = email,
                            table_name= TABLE_CUSTOMER)
                        QMessageBox.information(self, "Delete 결과", f"{delete_count}개의 데이터를 삭제합니다.")
                    # delete할 행이 없다면
                    else:
                        QMessageBox.critical(self, "입력 오류", "입력하신 정보의 데이터가 없습니다.\n데이터를 다시 확인 후 입력해주세요")
                else:
                    QMessageBox.critical(self, "입력 오류", "정보를 다시 입력해주세요!")     
            else: 
                buttonReply == QMessageBox.No
                QMessageBox.critical(self, "취소", "취소되었습니다!")
        ## info table에 입력할 데이터
        if set_flag:
            if fn_type == ' DELETE' or fn_type == ' INSERT':
                row = self.info_table.rowCount()
                self.info_table.insertRow(row)
                self.info_table.setItem(row, 0, QTableWidgetItem(fn_type))
                self.info_table.setItem(row, 1, QTableWidgetItem(id))
                self.info_table.setItem(row, 2, QTableWidgetItem(name))
                self.info_table.setItem(row, 3, QTableWidgetItem(email))
            elif fn_type == ' SELECT':
                for index, item in enumerate(id_list):
                    row = self.info_table.rowCount()
                    self.info_table.insertRow(row)
                    self.info_table.setItem(row, 0, QTableWidgetItem(fn_type))
                    self.info_table.setItem(row, 1, QTableWidgetItem(id_list[index]))
                    self.info_table.setItem(row, 2, QTableWidgetItem(name_list[index]))
                    self.info_table.setItem(row, 3, QTableWidgetItem(email_list[index]))

        self.reset()

######################################################################
    '''X버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore() 


'''3번 버튼 클릭 시 연결'''
def connect_powerbi():
    import webbrowser
    webbrowser.open(POWER_BI_LINK)


'''Data Analysis창 클래스 추가'''
class bi_form(QDialog,QWidget):
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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWindow = Ui_MainWindow()
    myWindow.show()
    
    '''상태표시줄'''
    myWindow.statusBar()
    myWindow.statusBar().showMessage("위험 비행물 감지 시스템 동작합니다.")
    app.exec_()

