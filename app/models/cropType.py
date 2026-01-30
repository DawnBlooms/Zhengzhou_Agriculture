from app.extension import db

class CropType(db.Model):
    __tablename__ = 'cropType'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avatar = db.Column(db.String(400), nullable=True)
    type = db.Column(db.String(50), nullable=False)
    classes = db.Column(db.String(50), nullable=False)

    plants = db.relationship("Plants", back_populates="crop_type")

    def to_json(self):
        return {
            'id': self.id,
            'avatar': self.avatar,
            'type': self.type,
            'classes': self.classes
        }