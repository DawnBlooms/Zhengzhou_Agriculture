from flask import Blueprint, jsonify, request
from sqlalchemy import desc

from app.extension import db
from app.models.news import News

news_blueprint = Blueprint('news', __name__)

@news_blueprint.route('/selectPage', methods=['GET'])
def select_page():
    page_num = int(request.args.get('pageNum', 1))
    page_size = int(request.args.get('pageSize', 10))
    title = request.args.get('title', '')

    query = News.query.order_by(desc(News.id))
    if title:
        query = query.filter(News.title.like(f'%{title}%'))

    total = query.count()
    admins = query.offset((page_num - 1) * page_size).limit(page_size).all()

    data = [news.to_json() for news in admins]
    return jsonify({'code': '200', 'msg': 'success', 'data': {'list': data, 'total': total}})

@news_blueprint.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    new_admin = News(title=data['title'], avatar=data['avatar'], content=data['content'])
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '新增成功', 'data': ''})

@news_blueprint.route('/update', methods=['PUT'])
def update():
    data = request.get_json()
    admin = News.query.get(data['id'])
    if not admin:
        return jsonify({'code': '404', 'msg': '用户不存在'})
    admin.title = data['title']
    admin.avatar = data.get('avatar')
    admin.content = data.get('content')
    db.session.commit()
    return jsonify({'code': '200', 'msg': '更新成功'})

# 删除单个
@news_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    admin = News.query.get(id)
    if not admin:
        return jsonify({'code': '404', 'msg': '用户不存在'})
    db.session.delete(admin)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '删除成功'})

# 批量删除
@news_blueprint.route('/delete/batch', methods=['DELETE'])
def delete_batch():
    ids = request.get_json()
    News.query.filter(News.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'code': '200', 'msg': '批量删除成功'})


