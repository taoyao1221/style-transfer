#-*-coding:utf-8-*-
import pdb
import os
import requests
import json
import base64
# test code

path = os.path.dirname(os.path.realpath(__file__))   #获取当前目录
faces_path = path + '/input_images'                   #待识别人脸库目录

def load_faces(faces_path):
    base64_faces = []
    for root, dirs, files in os.walk(faces_path):
        for file in files:
            image_path = faces_path + "/" + file
            with open(image_path, 'rb') as file:
                in_image = file.read()
            base64_bytes = base64.b64encode(in_image)
            image_base64_string = 'data:image/jpeg;base64,' + base64_bytes.decode()  # 将字符串解码为Unicode编码的字符串
            base64_faces.append(image_base64_string)
    return files, base64_faces

files, base64_faces = load_faces(faces_path)
data = {}
data['style'] = ["wave"]
data['images'] = base64_faces
data = json.dumps(data)  # 转换为json格式
url = "http://192.168.0.122:1221/service/aihub/v1/style_transfer/1.0"
pdb.set_trace()
rv = requests.post(url, data=data, timeout=500)
#pdb.set_trace()
results = rv.json()   #获取server端返回的json对象数据
print results['styles']
print results['styled_images']
