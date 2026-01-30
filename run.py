from flask import Flask
from app.extension import db, cors
from app.config import Config
from app.api.user import user_blueprint
from app.api.admin import admin_blueprint
from app.api.web import web_blueprint
from app.api.files import files_blueprint
from app.api.notice import notice_blueprint
from app.api.farmer import farmer_blueprint
from app.api.news import news_blueprint
from app.api.cropType import crop_type_bp
from app.api.plants import plants_blueprint
from app.api.orders import orders_blueprint
from app.api.cards import cards_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    cors.init_app(app)

    # 注册蓝图
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(farmer_blueprint, url_prefix='/farmer')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(web_blueprint, url_prefix='/web')
    app.register_blueprint(files_blueprint, url_prefix='/files')
    app.register_blueprint(notice_blueprint, url_prefix='/notice')
    app.register_blueprint(news_blueprint, url_prefix='/news')
    app.register_blueprint(crop_type_bp, url_prefix='/cropType')
    app.register_blueprint(plants_blueprint, url_prefix='/plants')
    app.register_blueprint(orders_blueprint, url_prefix='/orders')
    app.register_blueprint(cards_blueprint, url_prefix='/cards')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=9090)
