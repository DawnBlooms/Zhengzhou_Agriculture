from flask import Blueprint, jsonify, request
from app.models.admin import Admin
from app.models.user import User
from app.extension import db

web_blueprint = Blueprint('web', __name__)

@web_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return jsonify({'code': '401', 'msg': '用户名或密码为空', 'data': ''})
    elif data.get('role') == 'ADMIN':
        admin = Admin.query.filter_by(username = data.get('username')).first()
        if not admin:
            return jsonify({'code': '401', 'msg': '账号不存在', 'data': ''})
        if admin.password != data.get('password'):
            return jsonify({'code': '401', 'msg': '密码错误', 'data': ''})

        return jsonify({'code': '200', 'msg': '登录成功', 'data': admin.to_json()})
    else:
        user = User.query.filter_by(username = data.get('username')).first()
        if not user:
            return jsonify({'code': '401', 'msg': '账号不存在', 'data': ''})
        if user.password != data.get('password'):
            return jsonify({'code': '401', 'msg': '密码错误', 'data': ''})

        return jsonify({'code': '200', 'msg': '登录成功', 'data': user.to_json()})

@web_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    # 1️⃣ 基本校验
    if not username or not password:
        return jsonify({'code': '401', 'msg': '用户名或密码为空', 'data': ''})

    # 2️⃣ 管理员注册
    if role == 'ADMIN':
        exist_admin = Admin.query.filter_by(username=username).first()
        if exist_admin:
            return jsonify({'code': '401', 'msg': '账号已存在', 'data': ''})

        admin = Admin(
            username=username,
            password=password,
            role=role
        )
        db.session.add(admin)
        db.session.commit()

        return jsonify({'code': '200', 'msg': '注册成功', 'data': admin.to_json()})

    # 3️⃣ 普通用户 / 农户注册
    else:
        exist_user = User.query.filter_by(username=username).first()
        if exist_user:
            return jsonify({'code': '401', 'msg': '账号已存在', 'data': ''})

        user = User(
            username=username,
            password=password,
            role=role   # USER / FARMER
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({'code': '200', 'msg': '注册成功', 'data': user.to_json()})
