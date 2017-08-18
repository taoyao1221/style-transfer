#-*-coding:utf-8-*-
import pdb
import os
import requests
import json
import base64
# test code

path = os.path.dirname(os.path.realpath(__file__))   #获取当前目录
images_path = path + '/mutil_input_images'
styled_images = path + '/output_images'
def load_image(images_path):
    base64_images = []
    for root, dirs, files in os.walk(images_path):
        for file in files:
            image_path = images_path + "/" + file
            with open(image_path, 'rb') as file:
                in_image = file.read()
            base64_bytes = base64.b64encode(in_image)
            image_base64_string = 'data:image/jpeg;base64,' + base64_bytes.decode()  # 将字符串解码为Unicode编码的字符串
            base64_images.append(image_base64_string)
    return files, base64_images

files, base64_images = load_image(images_path)
data = {}
data['styles'] = ["wave", "wreck", "scream", "udnie", "rain_princess"]
data['images'] = base64_images
data = json.dumps(data)  # 转换为json格式
url = "http://192.168.1.70:5011/service/aihub/v1/style_transfer/1.0"
rv = requests.post(url, data=data, timeout=500)
results = rv.json()   #获取server端返回的json对象数据
for file, style, styled_image in zip(files, results['styles'], results['styled_images']):
    styled_image_base64_string = styled_image.rsplit(',')[1]   #去除前面的文件类型及编码信息
    styled_image_bytes = base64.b64decode(styled_image_base64_string)  #base64解码
    img_out_path = styled_images + '/' + style + '_' + file
    with open(img_out_path, 'wb') as file_stream:
        file_stream.write(styled_image_bytes)   #将接收到的图片二进制数据写入文件
