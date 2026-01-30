from datetime import datetime
from flask import Blueprint, request, jsonify
from app.models.notice import Notice
from app.extension import db

notice_blueprint = Blueprint('notice', __name__)

# 新增公告
@notice_blueprint.route('/add', methods=['POST'])
def add_notice():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    time = datetime.now()
    user = data.get('user')

    if not title or not content:
        return jsonify({'code': '400', 'msg': '标题和内容不能为空'})

    notice = Notice(title=title, content=content, user=user, time=time)
    db.session.add(notice)
    db.session.commit()

    return jsonify({'code': '200', 'msg': '新增成功'})


@notice_blueprint.route('/update', methods=['PUT'])
def update_notice():
    data = request.json
    notice_id = data.get('id')
    title = data.get('title')
    content = data.get('content')

    notice = Notice.query.get(notice_id)
    if not notice:
        return jsonify({'code': '404', 'msg': '公告不存在'})

    notice.title = title
    notice.content = content
    notice.time = datetime.now()
    db.session.commit()

    return jsonify({'code': '200', 'msg': '更新成功'})


@notice_blueprint.route('/delete/<int:notice_id>', methods=['DELETE'])
def delete_notice(notice_id):
    notice = Notice.query.get(notice_id)
    if not notice:
        return jsonify({'code': '404', 'msg': '公告不存在'})

    db.session.delete(notice)
    db.session.commit()

    return jsonify({'code': '200', 'msg': '删除成功'})


@notice_blueprint.route('/delete/batch', methods=['DELETE'])
def delete_notices_batch():
    data = request.json
    ids = data if isinstance(data, list) else []

    if not ids:
        return jsonify({'code': '400', 'msg': '未提供删除的 ID 列表'})

    notices = Notice.query.filter(Notice.id.in_(ids)).all()
    for notice in notices:
        db.session.delete(notice)
    db.session.commit()

    return jsonify({'code': '200', 'msg': '批量删除成功'})

# 分页查询公告
@notice_blueprint.route('/selectPage', methods=['GET'])
def select_page():
    page_num = request.args.get('pageNum', default=1, type=int)
    page_size = request.args.get('pageSize', default=10, type=int)
    title = request.args.get('title', default='', type=str)

    query = Notice.query
    if title:
        query = query.filter(Notice.title.like(f"%{title}%"))

    pagination = query.paginate(page=page_num, per_page=page_size, error_out=False)
    notices = [notice.to_json() for notice in pagination.items]

    return jsonify({
        'code': '200',
        'msg': '查询成功',
        'data': {
            'list': notices,
            'total': pagination.total
        }
    })

@notice_blueprint.route('/selectAll', methods=['GET'])
def select_all():
    notices = Notice.query.all()
    notices = [notice.to_json() for notice in notices]
    return jsonify({'code':'200', 'msg':'查询成功', 'data':notices})