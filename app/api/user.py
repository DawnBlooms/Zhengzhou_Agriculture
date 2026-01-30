from flask import Blueprint, jsonify, request
from app.models.user import User
from app.extension import db

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/selectPage', methods=['GET'])
def select_page():
    page_num = int(request.args.get('pageNum', 1))
    page_size = int(request.args.get('pageSize', 10))
    username = request.args.get('username', '')

    query = User.query.filter_by(role='USER')  # 根据 role 分拣数据
    if username:
        query = query.filter(User.username.like(f'%{username}%'))

    total = query.count()
    users = query.offset((page_num - 1) * page_size).limit(page_size).all()

    data = [user.to_json() for user in users]
    return jsonify({'code': '200', 'msg': 'success', 'data': {'list': data, 'total': total}})

@user_blueprint.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    # Role 默认指定为 'USER'
    new_user = User(
        username=data['username'],
        name=data['name'],
        email=data['email'],
        avatar=data['avatar'],
        phone=data['phone'],
        role='USER'  # 默认 'USER'，支持动态指定
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '新增成功', 'data': ''})

@user_blueprint.route('/update', methods=['PUT'])
def update():
    data = request.get_json()
    user = User.query.get(data['id'])
    if not user:
        return jsonify({'code': '404', 'msg': '用户不存在'})
    user.username = data['username']
    user.avatar = data.get('avatar')
    user.email = data.get('email')
    user.phone = data.get('phone')
    db.session.commit()
    return jsonify({'code': '200', 'msg': '更新成功'})

@user_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'code': '404', 'msg': '用户不存在'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '删除成功'})

@user_blueprint.route('/delete/batch', methods=['DELETE'])
def delete_batch():
    ids = request.get_json()
    User.query.filter(User.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '批量删除成功'})

@user_blueprint.route('/person', methods=['GET'])
def person():
    id = request.args.get('id')
    user = User.query.get(id)

    if not user:
        return jsonify({'code': '404', 'msg': '用户不存在'})

    return jsonify({'code':'200', 'msg': 'success', 'data':user.to_json()})
