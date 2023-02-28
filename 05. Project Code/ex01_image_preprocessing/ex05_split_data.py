# 데이터 나누기
# train 80 val 20 test 0

import os
import glob
import shutil
from sklearn.model_selection import train_test_split
from ex04_cvat2yolo import ex04_main

RATE = 0.8
RANDOM_SEED = 777
BIRD_FLAG = False
PATH = "./2023.02/02.22.d99_AI_project"
label_dict = {'drone': 0, 'bird': 1, 'airplane': 2, 'helicopter': 3, 'balloon': 4, 'military drone': 5}

def ex05_main():
    new_label_path = f"{PATH}/data/labels"

    # 폴더 생성
    modes = ['train', 'valid']
    for mode in modes:
        label_folder = f"{new_label_path.replace('data/labels', f'dataset/{mode}/labels')}" 
        image_folder   = f"{new_label_path.replace('data/labels', f'dataset/{mode}/images')}"
        os.makedirs(label_folder, exist_ok= True)  # create train folder
        os.makedirs(image_folder, exist_ok= True)  # create val folder   

    key_lists = []
    for key, value in label_dict.items():
        os.makedirs(f"{PATH}/data/labels/{key}", exist_ok=True)
        key_lists.append(key)

    label_paths = glob.glob(os.path.join(new_label_path, "*.txt"))

    # 파일 이동
    for label_path in label_paths:
        txt_name = label_path.split('\\')[-1]  # bird_0.txt
        label_name = txt_name.split('_')[0]    # bird
        try:
            shutil.move(label_path, os.path.join(new_label_path, label_name, txt_name))
        except:
            pass

    for item in key_lists: 
        print("*"*100)
        print(f"{item} split start...")

        txt_paths = glob.glob(os.path.join(new_label_path, item, '*.txt'))
        try:
            # train / valid split
            train_data, valid_data = train_test_split(txt_paths, test_size= 0.2, random_state= RANDOM_SEED)

            ### train
            for train_path in train_data:  # C:/Users/user/Documents/04.project/data/labels\drone\drone_2202.txt
                # label path setting
                new_train_path = train_path.replace(os.path.join('data/labels', item), 'dataset/train/labels')
                
                # label move
                # shutil.move(train_path, new_train_path)  
                shutil.copy(train_path, new_train_path)  
                
                # image path setting
                image_name = os.path.basename(train_path).replace('.txt', '.png') # drone_2202.png
                prev_image_path = os.path.join(f"{PATH}/{item}/images", image_name)       # C:/Users/user/Documents/04.project/drone/images\drone_2202.png
                new_image_path = os.path.join(f"{PATH}/dataset/train/images", image_name) # C:/Users/user/Documents/04.project/dataset/train/images\drone_2204.png
                
                # image move
                # shutil.move(prev_image_path, new_image_path) 
                shutil.copy(prev_image_path, new_image_path) 

            ### valid
            for valid_path in valid_data:
                # label path setting
                new_valid_path = valid_path.replace(os.path.join('data/labels', item), 'dataset/valid/labels')

                # label move
                # shutil.move(valid_path, new_valid_path)
                shutil.copy(valid_path, new_valid_path)

                # image path setting
                image_name = os.path.basename(valid_path).replace('.txt', '.png') 
                prev_image_path = os.path.join(f"{PATH}/{item}/images", image_name)       
                new_image_path = os.path.join(f"{PATH}/dataset/valid/images", image_name) 

                # image move
                # shutil.move(prev_image_path, new_image_path)  
                shutil.copy(prev_image_path, new_image_path)
                print_flag = True

        except Exception as e:
            print(e)
            print_flag = False

        if print_flag:
            # info print
            print("Total No. of Labels: ", len(txt_paths))
            print("Total No. of Train : ", len(train_data))
            print("Total No. of Valid : ", len(valid_data))
        print(f"{item} split finished...")

    # 폴더 삭제
    shutil.rmtree(f"{PATH}/data", ignore_errors=True)

if __name__ == '__main__':
    ex04_main()
    ex05_main()