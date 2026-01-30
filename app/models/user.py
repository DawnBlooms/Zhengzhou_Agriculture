from app.extension import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    name = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    password = db.Column(db.String(80))
    avatar = db.Column(db.String(120))
    role = db.Column(db.String(120))

    orders = db.relationship('Orders', back_populates='user')
    plants = db.relationship("Plants", back_populates="farmer")

    def to_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'role': self.role,
            'name': self.name,
            'phone': self.phone,
        }