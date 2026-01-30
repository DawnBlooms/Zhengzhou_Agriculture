from flask import Blueprint, jsonify, request
from sqlalchemy import desc

from app.models.cards import Cards
from app.extension import db

cards_blueprint = Blueprint('cards', __name__)

@cards_blueprint.route('/selectPage', methods=['GET'])
def select_page():
    page_num = int(request.args.get('pageNum', 1))
    page_size = int(request.args.get('pageSize', 10))
    title = request.args.get('title', '')
    user_id = request.args.get('user_id', '')

    query = Cards.query
    query = query.order_by(desc(Cards.id))
    if title:
        query = query.filter(Cards.title.like(f'%{title}%'))
    if user_id:
        query = query.filter(Cards.user_id == user_id)

    total = query.count()
    cards = query.offset((page_num - 1) * page_size).limit(page_size).all()

    data = [card.to_json() for card in cards]
    return jsonify({'code': '200', 'msg': 'success', 'data': {'list': data, 'total': total}})

@cards_blueprint.route('/add', methods=['POST'])
def add():
    data = request.get_json()

    new_card = Cards(
        title=data['title'],
        user_id=data['user_id'],
        content=data.get('content', ''),
        avatar=data.get('avatar', ''),

    )
    db.session.add(new_card)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '新增成功', 'data':''})

@cards_blueprint.route('/update', methods=['PUT'])
def update():
    data = request.get_json()
    card = Cards.query.get(data['id'])
    if not card:
        return jsonify({'code': '404', 'msg': '卡片不存在'})
    card.title = data['title']
    card.content = data.get('content', card.content)
    card.avatar = data.get('avatar', card.avatar)

    db.session.commit()
    return jsonify({'code': '200', 'msg': '更新成功', 'data': card.to_json()})

@cards_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    card = Cards.query.get(id)
    if not card:
        return jsonify({'code': '404', 'msg': '卡片不存在'})
    db.session.delete(card)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '删除成功'})

@cards_blueprint.route('/delete/batch', methods=['DELETE'])
def delete_batch():
    ids = request.get_json()
    Cards.query.filter(Cards.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '批量删除成功'})
