from app.extension import db

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
    avatar = db.Column(db.String(800))

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'avatar': self.avatar
        }