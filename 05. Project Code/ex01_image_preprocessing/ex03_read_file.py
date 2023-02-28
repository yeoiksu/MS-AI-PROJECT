import os
import glob
import cv2
import matplotlib.pyplot as plt

LABEL_NAME = 'helicopter'

# 최소 사이즈   
WIDTH_LIMIT, HEIGHT_LIMIT = 640, 640
RESIZE_LIMIT = 1280
small_img_list, small_size_paths = [], []

# 경로 변경 필요
root_path = f"C:/Users/user/Documents/03.dataset/230206_dataset/8_{LABEL_NAME}_old"
new_root = f"C:/Users/user/Documents/03.dataset/230206_dataset/8_{LABEL_NAME}"

# 폴더 생성
os.makedirs(new_root, exist_ok= True)
# os.makedirs(resize_img_root, exist_ok= True)

# 모든 이미지 (경로 변경 필요)
jpg_paths = glob.glob(os.path.join(root_path, '*.jpg'))
png_paths = glob.glob(os.path.join(root_path, '*.png'))
jpeg_paths = glob.glob(os.path.join(root_path, '*.jpeg'))
image_paths = jpg_paths + png_paths + jpeg_paths

# 마지막 작업 num (수정 필수 !!!!)
NUM = 14125

# 모든 이미지 경로
for index, image_path in enumerate(image_paths):
    index = index + NUM
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img_name = image_path.split('\\')[-1]
    RESIZE_FLAG = False
    try:
        # 가로가 세로보다 큰 경우 
        if (int(img.shape[1]) >= int(img.shape[0])):
            # 가로 이미지가 640 이하인 경우
            if (int(img.shape[1]) < WIDTH_LIMIT) :
                RESIZE_FLAG = True          
                aspect_ratio = float(WIDTH_LIMIT) / img.shape[1]
                dsize = (WIDTH_LIMIT, int(img.shape[0] * aspect_ratio))
                resized_img = cv2.resize(img, dsize, interpolation=cv2.INTER_AREA)
                cv2.imwrite( os.path.join(new_root, f'{LABEL_NAME}_{index}.png'), resized_img)

            # 가로 이미지가 960 이상인 경우
            elif (int(img.shape[1]) > RESIZE_LIMIT) :
                RESIZE_FLAG = True       
                aspect_ratio = float(RESIZE_LIMIT) / img.shape[1]
                dsize = (RESIZE_LIMIT, int(img.shape[0] * aspect_ratio))
                resized_img = cv2.resize(img, dsize, interpolation=cv2.INTER_AREA)
                cv2.imwrite( os.path.join(new_root, f'{LABEL_NAME}_{index}.png'), resized_img)
            else:
                cv2.imwrite( os.path.join(new_root, f'{LABEL_NAME}_{index}.png'), img)
            
        # 세로가 가로보다 큰 경우 
        elif (img.shape[0] > img.shape[1]):
            # 세로 이미지가 640 이하인 경우
            if (int(img.shape[0]) < HEIGHT_LIMIT) :
                RESIZE_FLAG = True
                aspect_ratio = float(HEIGHT_LIMIT) / img.shape[0]
                dsize = (int(img.shape[1] * aspect_ratio), HEIGHT_LIMIT)
                resized_img = cv2.resize(img, dsize, interpolation=cv2.INTER_AREA)
                cv2.imwrite( os.path.join(new_root, f'{LABEL_NAME}_{index}.png'), resized_img)
            
            # 세로 이미지가 960 이상인 경우
            elif (int(img.shape[0]) > RESIZE_LIMIT) :
                RESIZE_FLAG = True
                aspect_ratio = float(RESIZE_LIMIT) / img.shape[0]
                dsize = (int(img.shape[1] * aspect_ratio), RESIZE_LIMIT)
                resized_img = cv2.resize(img, dsize, interpolation=cv2.INTER_AREA)
                cv2.imwrite( os.path.join(new_root, f'{LABEL_NAME}_{index}.png'), resized_img)

            else:
                cv2.imwrite(os.path.join(new_root, f'{LABEL_NAME}_{index}.png'), img)
            
        print(f'{index}/{len(image_paths) + NUM}\t' , f'{RESIZE_FLAG}\t', img_name)

    except Exception as e:
        print(e, '\t', image_path)

# print('*'*100)
# print("No. of total images: ", len(image_paths))
# print("No. of small images: ", len(small_img_list))