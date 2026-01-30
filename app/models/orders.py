from app.extension import db


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, comment='ID')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='用户ID')
    plants_id = db.Column(db.Integer, db.ForeignKey('plants.id'), comment='种植编号')
    area = db.Column(db.Integer, comment='种植面积(亩)')
    plan_img = db.Column(db.String(300), default='', comment='进度图片')
    predict = db.Column(db.Date, comment='预计结束时间')
    status = db.Column(db.String(200), default='等待种植', comment='状态')
    insurance = db.Column(db.String(20), default='否', comment='购买保险')

    user = db.relationship('User', back_populates='orders')
    plants = db.relationship('Plants', back_populates='orders')

    def to_json(self):
        formatted_predict = self.predict.strftime('%Y-%m-%d') if self.predict else None
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plants_id": self.plants_id,
            "area": self.area,
            "predict": formatted_predict,
            "status": self.status,
            "plan_img": self.plan_img,
            "insurance": self.insurance,

            "username": self.user.username,
            "user_email": self.user.email,
            "user_phone": self.user.phone,
            "user_avatar": self.user.avatar,

            "farmer_name": self.plants.farmer.username,
            "farmer_email": self.plants.farmer.email,
            "farmer_phone": self.plants.farmer.phone,
            "farmer_avatar": self.plants.farmer.avatar,

            "crop_avatar": self.plants.crop_type.avatar,
            "type": self.plants.crop_type.type,
            "classes": self.plants.crop_type.classes,
        }


