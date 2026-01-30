from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy.orm import aliased

from app.extension import db
from app.models.orders import Orders
from app.models.plants import Plants
from app.models.user import User
from app.models.cropType import CropType

orders_blueprint = Blueprint('orders', __name__)

@orders_blueprint.route('/selectPage', methods=['GET'])
def select_page():
    # 获取分页参数和筛选条件
    page_num = int(request.args.get('pageNum', 1))  # 页码
    page_size = int(request.args.get('pageSize', 10))  # 每页条数
    username = request.args.get('username', '')  # 下单用户的用户名
    farmer_name = request.args.get('farmer_name', '')  # 农户姓名
    crop_type = request.args.get('type', '')  # 作物类型

    # 为 user 表创建别名
    user_alias = aliased(User)
    farmer_alias = aliased(User)

    # 构建查询
    query = Orders.query.join(user_alias, Orders.user).join(Plants, Orders.plants).join(CropType, Plants.crop_type).join(farmer_alias, Plants.farmer)

    if username:
        query = query.filter(user_alias.username.like(f'%{username}%'))
    if farmer_name:
        query = query.filter(farmer_alias.username == farmer_name)
    if crop_type:
        query = query.filter(CropType.type.like(f'%{crop_type}%'))

    pagination = query.paginate(page=page_num, per_page=page_size, error_out=False)
    orders = pagination.items
    total = pagination.total

    # 返回结果
    data = [order.to_json() for order in orders]
    return jsonify({
        'code': '200',
        'msg': 'success',
        'data': {
            'list': data,
            'total': total
        }
    })

@orders_blueprint.route('/update', methods=['PUT'])
def update():
    data = request.get_json()
    admin = Orders.query.get(data['id'])
    if not admin:
        return jsonify({'code': '404', 'msg': '用户不存在'})

    admin.area = data['area']
    admin.status = data.get('status')
    admin.predict = data.get('predict')
    admin.plan_img = data.get('plan_img')
    admin.insurance = data.get('insurance')
    db.session.commit()
    return jsonify({'code': '200', 'msg': '更新成功'})

@orders_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    admin = Orders.query.get(id)
    if not admin:
        return jsonify({'code': '404', 'msg': '用户不存在'})
    db.session.delete(admin)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '删除成功'})

# 批量删除
@orders_blueprint.route('/delete/batch', methods=['DELETE'])
def delete_batch():
    ids = request.get_json()
    Orders.query.filter(Orders.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '批量删除成功'})

@orders_blueprint.route('/add', methods=['POST'])
def add_plant():
    data = request.json

    # 创建新的 Plants 实例
    plant = Orders(
        user_id=data.get('user_id'),
        plants_id=data.get('plants_id'),
        area=data.get('area'),
        insurance=data.get('insurance'),
    )

    # 添加到数据库并提交
    db.session.add(plant)
    db.session.commit()

    return jsonify({'code': '200', 'msg': '新增成功'})

@orders_blueprint.route('/selectUserId', methods=['GET'])
def select_user_id():
    # 获取分页参数和筛选条件
    page_num = int(request.args.get('pageNum', 1))  # 页码
    page_size = int(request.args.get('pageSize', 10))  # 每页条数
    user_id = int(request.args.get('user_id', 0))
    crop_type = request.args.get('type', '')  # 作物类型

    # 为 user 表创建别名
    user_alias = aliased(User)
    farmer_alias = aliased(User)

    # 构建查询
    query = Orders.query.join(user_alias, Orders.user).join(Plants, Orders.plants).join(CropType, Plants.crop_type).join(farmer_alias, Plants.farmer)

    query = query.order_by(Orders.id.desc())

    if user_id:
        query = query.filter(user_alias.id == user_id)
    if crop_type:
        query = query.filter(CropType.type.like(f'%{crop_type}%'))

    # 分页查询
    pagination = query.paginate(page=page_num, per_page=page_size, error_out=False)
    orders = pagination.items
    total = pagination.total

    # 返回结果
    data = [order.to_json() for order in orders]
    return jsonify({
        'code': '200',
        'msg': 'success',
        'data': {
            'list': data,
            'total': total
        }
    })

@orders_blueprint.route('/selectId', methods=['GET'])
def select_id():
    id = int(request.args.get('id', 0))

    user_alias = aliased(User)
    farmer_alias = aliased(User)

    # 构建查询
    query = Orders.query.join(user_alias, Orders.user).join(Plants, Orders.plants).join(CropType, Plants.crop_type).join(farmer_alias, Plants.farmer)

    if id:
        query = query.filter(Orders.id == id).first()

    return jsonify({
        'code': '200',
        'msg': 'success',
        'data': query.to_json()
    })