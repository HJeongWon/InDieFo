from datetime import datetime
from db import db
class User(db.Model):

    nickname = db.Column(db.String(80), unique=True)
    idx = db.Column(db.String(120), unique=True)
    pw = db.Column(db.String(20))
    created = db.Column(db.DateTime,default = datetime.now, )
    def __init__(self,id,pw,nickname):
        self.id = id
        self.pw = pw
        self.nickname = nickname;
