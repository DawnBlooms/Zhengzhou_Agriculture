from app.extension import db

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    avatar = db.Column(db.String(800), unique=True, nullable=False)
    role = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(800), unique=True, nullable=False)

    def to_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'avatar': self.avatar,
            'role': self.role,
            'phone': self.phone,
            'email': self.email
        }