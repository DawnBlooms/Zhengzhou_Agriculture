from app.extension import db

class Plants(db.Model):
    __tablename__ = "plants"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey("cropType.id"), nullable=False)
    evaluate = db.Column(db.String(500))
    likes = db.Column(db.Integer, default=0)
    deadline = db.Column(db.Date)
    sales = db.Column(db.Integer, default=0)
    status = db.Column(db.String, default='等待种植')

    farmer = db.relationship("User", back_populates="plants")
    crop_type = db.relationship("CropType", back_populates="plants")
    orders = db.relationship('Orders', back_populates='plants')


    def to_json(self):
        formatted_deadline = self.deadline.strftime('%Y-%m-%d') if self.deadline else None
        return{
            "id": self.id,
            "farmer_id": self.farmer_id,
            "crop_id": self.crop_id,
            "evaluate": self.evaluate,
            "likes": self.likes,
            "deadline": formatted_deadline,
            "sales": self.sales,
            "status": self.status,
            "username": self.farmer.username,
            "email": self.farmer.email,
            "name": self.farmer.name,
            "phone": self.farmer.phone,
            "role": self.farmer.role,
            "farmer_avatar": self.farmer.avatar,
            "crop_avatar": self.crop_type.avatar,
            "type": self.crop_type.type,
            "classes": self.crop_type.classes,
        }

