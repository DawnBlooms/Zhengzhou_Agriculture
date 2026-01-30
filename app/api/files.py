import os
import time
from flask import Blueprint, request, jsonify, current_app

files_blueprint = Blueprint('files', __name__)

# 文件上传接口
@files_blueprint.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({'code': '400', 'msg': '未上传文件'})

    # 定义文件存储路径（static 目录下的 files 文件夹）
    static_path = os.path.join(current_app.root_path, 'static', 'files')
    if not os.path.exists(static_path):
        os.makedirs(static_path)

    # 文件命名格式：时间戳-原文件名
    timestamp = str(int(time.time() * 1000))
    filename = f"{timestamp}-{file.filename}"
    file_path = os.path.join(static_path, filename)

    try:
        file.save(file_path)
        print(f"{file.filename} -- 上传成功")
    except Exception as e:
        print(f"{file.filename} -- 文件上传失败: {str(e)}")
        return jsonify({'code': '500', 'msg': '文件上传失败'})

    # 返回文件访问地址
    ip = current_app.config.get('IP', 'localhost')
    port = current_app.config.get('PORT', '9090')
    http = f"http://{ip}:{port}/static/files/"
    return jsonify({'code': '200', 'msg': '上传成功', 'data': http + filename})