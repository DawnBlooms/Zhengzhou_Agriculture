from datetime import datetime, timezone

from app.extension import db


class Cards(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(80))
    content = db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

    user = db.relationship('User', backref='cards')

    def to_json(self):
        formatted_time = self.time.strftime('%Y-%m-%d %H:%M') if self.time else None
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'user_avatar': self.user.avatar,
            'user_name': self.user.name,
            'email': self.user.email,
            'phone': self.user.phone,
            'role': self.user.role,
            'time': formatted_time,
            'title': self.title,
            'content': self.content,
            'avatar': self.avatar,
            'likes': self.likes,
            'dislikes': self.dislikes,
        }




