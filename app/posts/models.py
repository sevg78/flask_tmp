from . database import db
from . users.models import User
from datetime import datetime
import re

def slugfu(st):
    pat = r'[^\w+]'
    return re.sub(pat, '-', st)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    slug = db.Colun(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        if self.title:
            self.slug = slugfu(self.title)
