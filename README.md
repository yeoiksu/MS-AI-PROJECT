# 위험 비행물 탐지 시스템(Hazardous Flying Object Detection System)
- This repo is to record Microsoft AI School Team 2 Project.


## I. Summary of Project and Team
- Microsoft AI School Team 2 Project
- Schedule : 
    - Processing : 2023.2.6 ~ 3.22
    - A result briefing session : 2023.3.22 | Presentation : http://naver.me/FJ63fjJz
- Member of Project   
    Team Leader : @yeoiksu | https://github.com/yeoiksu  
    Team Member : @TaeYounKwon | https://github.com/TaeYounKwon  
    Team Member : @ssyjgs1 | https://github.com/ssyjgs1  
    Team Member : @Byunggu-Son | https://github.com/Byunggu-Son  
    Team Member : @yuyeon | https://github.com/yuyeon-choi  
    Team Member : 이주은님 | (GitHub 주소)
- Project Environment and Technical Stacks
    - Stacks : Python, PyTorch, Anaconda Environment, etc...
    - Environments : Processing Model on Microsoft Azure Data Science Virtual Machine

## II. Introduction  
본 시스템은 실시간 카메라로 확인하여 위험 비행물(군사용 드론)을 탐지 및 추적합니다. 위험 비행물을 발견할 시, 위험물을 촬영한 장비 GPS 정보를 경보 메세지와 함께 이메일로 사용자에게 제공하며, 데이터 분석을 통해 위험 비행물에 관련한 유용한 데이터를 사용자에게 제공합니다.  

위험 비행물의 탐지 및 추적은 YOLOv8L 모델을 기반으로 생성된 모델이 사용되었으며, 데이터베이스는 MariaDB, 데이터 분석은 Microsoft Power BI를 통해 제공됩니다.

## III. System Architecture
![system architecture](images/system%20architecture.png)
![alarm for user](images/alarm%20for%20user.png)


<!-- [Azure. ADO.NET & CRUD](https://github.com/yeoiksu/Microsoft-AI-School/tree/main/2022.11/11.10_d27_azure) -->
<hr>

## IV. Repository Folder
### 1. [Project Plan](#i-project-plan)
### 2. [Object Detection Model](#ii-object-detection-model)
### 3. [Database](#iii-database)
### 4. [GUI (PyQt5)](#iv-gui-pyqt5)
### 5. [Project Code](#v-project-code)

<hr>
