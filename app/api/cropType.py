from collections import defaultdict

from flask import Blueprint, request, jsonify
from app.extension import db
from app.models.cropType import CropType

crop_type_bp = Blueprint('crop_type', __name__)


@crop_type_bp.route('/add', methods=['POST'])
def add_crop_type():
    data = request.json
    new_crop = CropType(
        avatar=data.get('avatar'),
        type=data.get('type'),
        classes=data.get('classes')
    )
    db.session.add(new_crop)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '新增成功'})


@crop_type_bp.route('/update', methods=['PUT'])
def update_crop_type():
    data = request.json
    crop = CropType.query.get(data.get('id'))
    if not crop:
        return jsonify({'code': '404', 'msg': '数据不存在'})

    crop.avatar = data.get('avatar')
    crop.type = data.get('type')
    crop.classes = data.get('classes')
    db.session.commit()
    return jsonify({'code': '200', 'msg': '更新成功'})


@crop_type_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_crop_type(id):
    crop = CropType.query.get(id)
    if not crop:
        return jsonify({'code': '404', 'msg': '数据不存在'})

    db.session.delete(crop)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '删除成功'})


@crop_type_bp.route('/selectPage', methods=['GET'])
def select_page():
    page_num = int(request.args.get('pageNum', 1))
    page_size = int(request.args.get('pageSize', 10))
    type = request.args.get('type', '')

    query = CropType.query
    if type:
        query = query.filter(CropType.type.like(f'%{type}%'))

    total = query.count()
    users = query.offset((page_num - 1) * page_size).limit(page_size).all()

    data = [user.to_json() for user in users]
    return jsonify({'code': '200', 'msg': 'success', 'data': {'list': data, 'total': total}})

@crop_type_bp.route('/delete/batch', methods=['DELETE'])
def delete_batch():
    ids = request.get_json()
    CropType.query.filter(CropType.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '批量删除成功'})


@crop_type_bp.route('/classes', methods=['GET'])
def get_distinct_classes():
    # 查询出所有记录
    results = db.session.query(CropType).all()

    # 使用字典将数据按 classes 分组
    grouped_data = defaultdict(list)
    for result in results:
        grouped_data[result.classes].append(result.to_json())

    # 转换为 JSON 格式，只返回每个分组的第一个对象或其他所需处理
    distinct_data = []
    for cls, items in grouped_data.items():
        # 这里只取第一个对象，如果需要所有对象，可保留 `items`
        distinct_data.append(items[0])

    return jsonify({'code': '200', 'msg': 'success', 'data': distinct_data})