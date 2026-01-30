from app.extension import db

class Notice(db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
    time = db.Column(db.String(255))
    user = db.Column(db.String(255))

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'time': self.time,
            'user': self.user,
        }