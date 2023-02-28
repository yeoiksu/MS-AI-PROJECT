# I. Project Plan
## - 1 주차 (23.02.21 ~ 23.02.24)
1. 02.21 (TUE). 데이터 추가 수집 및 군용드론 이미지 수집 (label당 10,000장 목표)
- 데이터 현황    
    <img src ='./images/0221.png' ></img>

2. 02.22 (WED). 추가한 데이터 bbox 작업 (label당 약 10,000장 목표)
- 데이터 현황
    <img src ='./images/0222.png' ></img>

3. 02.23 (THU). 데이터셋 구축 및 팀원 역할 분담 및 (Multi-processing, Tracking, DB, PyQt5 등등)
- 최종 데이터 현황
<img src ='./images/0223.png' ></img>

- 팀원 역할분담

        1. Total (여익수 팀장)
            - 전반적인 알고르즘 설계 및 역할 분담
        2. Multi Processing (권태윤 팀원)
            - Detect.py 수정 
            - 새로운 object 탐지할 때 Database와 연결
            - Object tracking (같은 물체 tracking)
        3. Database (최유연 & 이주은 팀원)
            - DB 및 table 설정 (column 설정)
            - 실제 Database에 넣어서 저장할 data 짜는 알고리즘
                    ^^^ object tracking 연장선 ^^^
            - 데이터를 어떻게 활용해서 분석할지 (Power BI)
        4. GUI (이승윤 & 손병구 팀원)
            - Qt designer + pyqt5
            - 큰 틀은 같이 짜고, 그 안에 기능들은 개별로 진행
4. 02.24 (FRI). Yolov5 모델 inference 확인 및 모델 평가
- trainset 대상으로 val.py 실행 결과 (mAP50-95 : 0.859)
    <img src ='./images/result1.png' ></img>
        
- validset 대상으로 val.py 실행 결과 (mAP50-95 : 0.817)
    <img src ='./images/result2.png'></img>

<hr>

## - 2 주차 (23.02.27 ~ 23.03.03)

