#-*-coding:utf-8-*-
from flask import Flask, request, jsonify
#from redis import Redis
import json
app = Flask(__name__)

#redis = Redis(host='redis', port=6379)
@app.route('/service/aihub/v1/style_transfer/1.0', methods=['GET','POST'])
def style_transfer():
    request_json = request.get_json(force=True)
    if request_json:
        result_json = aihub_invoke_style_transfer(request_json)
    return result_json

@app.route('/service/aihub/v1/video_style_transfer/1.0', methods=['GET','POST'])
def video_style_transfer():
    request_json = request.get_json(force=True)
    if request_json:
        result_json = aihub_invoke_video_style_transfer(request_json)
    return result_json

#**********************************************************************************************************************
#
#  如下是您算法的内部实现，请遵循命名规则替换成您自己的算法实现，命名规则：aihub_invoke_xxxxxxxx_xxxxxxx(request_json)
#  通过curl向 http://aihub.finalshares.com/service/aihub/v1/算法名(例如:coloring)/1.0 发送json请求即可得到返回结果
#
#**********************************************************************************************************************
import imp
import os
import base64
import urllib

def aihub_invoke_style_transfer(request_json):
    #
    path = os.path.dirname(os.path.realpath(__file__))   #获取当前目录
    style_transfer_module = imp.load_source("new_evaluate", "./new_evaluate.py")

    styles = []
    styled_images = []
    input_image_name = 'img_in.jpg'    #用于存放原始图片
    output_image_name = 'img_out.jpg'   #用于存放转换风格后的图片
    for style, image in zip(request_json['style'], request_json['images']):
        image_base64_string = image.rsplit(',')[1]   #去除前面的文件类型及编码信息
        image_bytes = base64.b64decode(image_base64_string)  #base64解码
        with open(input_image_name, 'wb') as file_stream:
            file_stream.write(image_bytes)   #将接收到的图片二进制数据写入文件
        style_moddel = style + '.ckpt'
        checkpoint_dir = path + '/ckpt/' + style_moddel
        input_image_dir = path + '/' + input_image_name
        output_image_dir = path + '/' + output_image_name
        style_transfer_module.main(checkpoint_dir, input_image_dir, output_image_dir)  #调用风格转换模块进行风格转换
        with open(output_image_name, 'rb') as file:
                styled_image = file.read()
        styled_image_base64_bytes = base64.b64encode(styled_image)       #base64编码
        styled_image_base64_string = 'data:image/jpeg;base64,' + styled_image_base64_bytes.decode()  # 将字符串解码为Unicode编码的字符串
        styles.append(style)
        styled_images.append(styled_image_base64_string)

    result_json = {}
    result_json['aihub'] = "AIhub fasting AI, you are welcome, 2017-07-28"
    result_json['styles'] = styles
    result_json['styled_images'] = styled_images
    return jsonify(result_json)


@app.route('/service/test', methods=['GET','POST'])
def hello():
    count = redis.incr('hits')
    return 'Hello AIhub, this is {} times visiting.\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1221, debug=True)
