from flask import Blueprint, jsonify, request

from app.extension import db
from app.models.admin import Admin

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/selectPage', methods=['GET'])
def select_page():
    page_num = int(request.args.get('pageNum', 1))
    page_size = int(request.args.get('pageSize', 10))
    username = request.args.get('username', '')

    query = Admin.query
    if username:
        query = query.filter(Admin.username.like(f'%{username}%'))

    total = query.count()
    admins = query.offset((page_num - 1) * page_size).limit(page_size).all()

    data = [admin.to_json() for admin in admins]
    return jsonify({'code': '200', 'msg': 'success', 'data': {'list': data, 'total': total}})

@admin_blueprint.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    new_admin = Admin(username=data['username'], name=data['name'], email=data['email'], avatar=data['avatar'], phone=data['phone'], role='ADMIN')
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '新增成功', 'data': ''})

@admin_blueprint.route('/update', methods=['PUT'])
def update():
    data = request.get_json()
    admin = Admin.query.get(data['id'])
    if not admin:
        return jsonify({'code': '404', 'msg': '用户不存在'})
    admin.username = data['username']
    admin.avatar = data.get('avatar')
    admin.email = data.get('email')
    admin.phone = data.get('phone')
    db.session.commit()
    return jsonify({'code': '200', 'msg': '更新成功'})

# 删除单个
@admin_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    admin = Admin.query.get(id)
    if not admin:
        return jsonify({'code': '404', 'msg': '用户不存在'})
    db.session.delete(admin)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '删除成功'})

# 批量删除
@admin_blueprint.route('/delete/batch', methods=['DELETE'])
def delete_batch():
    ids = request.get_json()
    Admin.query.filter(Admin.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '批量删除成功'})

