# coding: utf-8
# Author: mark
# description: xxxx
# contact:

from flask import Flask, request, jsonify, send_file
import os
import hashlib

app = Flask(__name__)

# 保存最新客户端版本号和文件MD5值的映射表
latest_version = {
    "name": "yibutong",
    "version": "1.0.2",
    "md5": "",
}


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


@app.route('/check_version', methods=['GET'])
def check_version():
    # 返回包含最新版本号信息的JSON数据
    return jsonify(latest_version)


@app.route('/upload_client', methods=['POST'])
def upload_client():
    # 上传最新客户端程序文件，并更新版本号和MD5值的映射表
    file = request.files['file']
    filename = file.filename
    # 判断上传文件名是否为yibutong_[0-9].*.exe的格式
    if not filename.startswith('yibutong_') or not filename.endswith('.exe'):
        return "上传文件名的格式不对，应该是yibutong_版本号数字.exe"

    filepath = os.path.join(os.getcwd(), 'clients', filename)
    file.save(filepath)
    # 计算文件的MD5值
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            md5.update(data)
    # 更新版本号和MD5值的映射表
    latest_version['version'] = filename.split('.')[0].split('_')[1]
    latest_version['md5'] = md5.hexdigest()
    return "%s Upload success!" % filename


@app.route('/download_client', methods=['GET'])
def download_client():
    # 返回最新客户端程序文件
    filename = "yibutong_" + latest_version['version'] + '.exe'
    filepath = os.path.join(os.getcwd(), 'clients', filename)
    # 判断文件是否存在
    if not os.path.exists(filepath):
        return "文件不存在"
    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    app.run()
