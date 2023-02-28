"""CVAT XML to YOLO"""
import os
import glob
from xml.etree.ElementTree import parse

label_num_drone, label_num_bird, label_num_airplane = 0, 0, 0
label_num_helicopter, label_num_balloon, label_num_military = 0, 0, 0 

PATH = "./2023.02/02.22.d99_AI_project/balloon"  # path 수정 필요
label_dict = {'drone': 0, 'bird': 1, 'airplane': 2, 'helicopter': 3, 'balloon': 4, 'military drone': 5}
def ex04_main():
    """xml 1 ~ 5 같이 여러 개 생기면 찾는 함수"""
    xml_paths = glob.glob(os.path.join(PATH, "*.xml"))
    # xml_paths = glob.glob(os.path.join(PATH, "*", "*.xml"))
    os.makedirs(f"{PATH}/data/labels", exist_ok=True)  

    for xml_path in xml_paths :
        tree = parse(xml_path)
        root = tree.getroot()
        img_metas = root.findall("image")
        # print(img_metas)
        for img_meta in img_metas :
            # xml에 기록된 image name 가져오기
            image_name = img_meta.attrib['name']        # bird/bird_0.png
            # front_name = image_name.split('_')[0].replace("balloun", "balloon")  # balloun -> balloon
            # back_num = str( int(image_name.split('_')[-1].split(".")[0]) + 827)  # 0 -> 827
            # image_name = f'{front_name}_{back_num}.png' # balloun_0.png -> balloon_827.png

            # 경로에 '/' 가 있다면
            if '/' in image_name:
                image_name = image_name.split('/')[-1]  # bird_0.png
            else: 
                pass
            image_name_temp = image_name.replace(".png", ".txt")

            # Box meta 정보 뽑아오기 | XML은 모든 값이 str이라서 뭐 계산할 거면 int, float으로 바꿔줘야 함
            box_metas = img_meta.findall("box")
            img_width = int(img_meta.attrib['width'])
            img_height = int(img_meta.attrib['height'])
            # print(img_width, img_height)

            for box_meta in box_metas :
                box_label = box_meta.attrib['label']
                
                box = [int(float(box_meta.attrib['xtl'])), int(float(box_meta.attrib['ytl'])), int(float(box_meta.attrib['xbr'])), int(float(box_meta.attrib['ybr']))]
                # print(box_label, box)

                # yolo 형식에 맞게 normalization을 해보자
                yolo_x = round(((box[0] + box[2]) / 2) / img_width, 6)
                yolo_y = round(((box[1] + box[3]) / 2) / img_height, 6)
                yolo_w = round((box[2] - box[0]) / img_width, 6)
                yolo_h = round((box[3] - box[1]) / img_height, 6)
                # print("yolo xywh >>>", yolo_x, yolo_y, yolo_w, yolo_h)
                
                # label
                label = label_dict[box_label]
                # print(label) # 4.....+ 그 외 숫자들

                # 앞서 모은 정보들로 txt파일로 저장해보자
                with open(f"{PATH}/data/labels/{image_name_temp}", 'a') as f :
                    f.write(f"{label} {yolo_x} {yolo_y} {yolo_w} {yolo_h}\n")

# if __name__ == '__main__':
    # ex04_main()