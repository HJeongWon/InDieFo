

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from db import db,User,Board
admin = Admin()

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Board, db.session))