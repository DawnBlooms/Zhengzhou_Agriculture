from datetime import datetime

from flask import Blueprint, jsonify, request

from app.extension import db
from app.models.orders import Orders
from app.models.plants import Plants
from app.api.user import User
from app.api.cropType import CropType

plants_blueprint = Blueprint('plants', __name__)


@plants_blueprint.route('/selectPage', methods=['GET'])
def select_page():

    # 获取分页参数和筛选条件
    page_num = int(request.args.get('pageNum', 1))
    page_size = int(request.args.get('pageSize', 10))
    type = request.args.get('type', '')
    username = request.args.get('username', '')

    # 构建查询
    query = Plants.query.join(User, Plants.farmer).join(CropType, Plants.crop_type)
    query = query.order_by((Plants.likes + Plants.sales).desc())
    if type:
        query = query.filter(CropType.type.like(f'%{type}%'))
    if username:
        query = query.filter(User.username == username)

    # 分页查询
    total = query.count()
    plants = query.offset((page_num - 1) * page_size).limit(page_size).all()

    # 返回结果
    data = [plant.to_json() for plant in plants]
    return jsonify({
        'code': '200',
        'msg': 'success',
        'data': {
            'list': data,
            'total': total
        }
    })


@plants_blueprint.route('/add', methods=['POST'])
def add_plant():
    data = request.json
    # 获取 CropType 对象
    crop = db.session.query(CropType).filter(CropType.type == data.get('type')).first()

    if not crop:
        return jsonify({'code': '400', 'msg': '无效的作物类型'})

    crop_id = crop.id  # 或者 crop.type，根据你模型的定义

    # 创建新的 Plants 实例
    plant = Plants(
        crop_id=crop_id,
        farmer_id=data['farmer_id'],
        evaluate=data.get('evaluate'),
        deadline=datetime.strptime(data.get('deadline'), '%Y-%m-%d'),
        status=data.get('status'),
    )

    # 添加到数据库并提交
    db.session.add(plant)
    db.session.commit()

    return jsonify({'code': '200', 'msg': '新增成功'})


@plants_blueprint.route('/update', methods=['PUT'])
def update():
    data = request.get_json()
    admin = Plants.query.get(data['id'])
    if not admin:
        return jsonify({'code': '404', 'msg': '用户不存在'})
    crop = db.session.query(CropType).filter(CropType.type == data.get('type')).first()

    if not crop:
        return jsonify({'code': '400', 'msg': '无效的作物类型'})

    admin.evaluate = data['evaluate']
    admin.deadline = data.get('deadline')
    admin.crop_id = crop.id
    admin.status = data.get('status')

    orders = Orders.query.filter_by(plants_id = data['id']).all()

    for order in orders:
        order.status = data.get('status')

    db.session.commit()
    return jsonify({'code': '200', 'msg': '更新成功'})


@plants_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    admin = Plants.query.get(id)
    if not admin:
        return jsonify({'code': '404', 'msg': '用户不存在'})
    db.session.delete(admin)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '删除成功'})


@plants_blueprint.route('/delete/batch', methods=['DELETE'])
def delete_batch():
    ids = request.get_json()
    Plants.query.filter(Plants.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '批量删除成功'})


@plants_blueprint.route('/selectId', methods=['GET'])
def select_id():
    id = request.args.get('id')
    if not id:
        return jsonify({'code': '200', 'msg': '无效的作物'})

    # 执行查询
    query = Plants.query.join(User, Plants.farmer).join(CropType, Plants.crop_type)
    plants = query.filter(Plants.id == id).first()  # 获取单个作物

    if not plants:
        return jsonify({'code': '404', 'msg': '作物未找到'})

    # 将查询的 plants 转换为字典格式
    return jsonify({'code': '200', 'msg': 'success', 'data': plants.to_json()})


@plants_blueprint.route('/selectByClass', methods=['GET'])
def select_by_class():

    # 获取前端传递的参数
    page_num = int(request.args.get('pageNum', 1))
    page_size = int(request.args.get('pageSize', 10))
    classes = request.args.get('classes', None)
    type = request.args.get('type', None)

    # 查询数据库
    query = Plants.query.join(User, Plants.farmer).join(CropType, Plants.crop_type)
    query = query.order_by((Plants.likes + Plants.sales).desc())
    if classes:
        query = query.filter(CropType.classes == classes)

    if type:
        query = query.filter(CropType.type.like(f'%{type}%'))
    # 分页处理
    total_count = query.count()
    plants = query.offset((page_num - 1) * page_size).limit(page_size).all()

    # 格式化返回数据
    plant_data = [plant.to_json() for plant in plants]


    return jsonify({'code': '200', 'msg': 'success', 'data': { 'list': plant_data, 'total': total_count }})

