from datetime import datetime

from flask import Flask, jsonify ,render_template,request,session,make_response
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'asldjalksjdklasd'
admin = Admin(app)
db = SQLAlchemy(app)


class User(db.Model):
    """
    from test import db
    db.create_app()
    """
    __tablename__ = "user"

    idx = db.Column(db.Integer, primary_key=True)

    nickname = db.Column(db.String(20),unique=True)
    email = db.Column(db.String(20), unique=True)
    pw = db.Column(db.String(20))
    created = db.Column(db.DateTime, default=datetime.now)

    # no __init__()

class Comment(db.Model):
    __tablename__ = "comment"

    idx = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    who = db.Column(db.Integer, db.ForeignKey('user.idx'))

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/create/<name>/<id>/<pw>")
def create(name, id, pw):
    new = User()
    new.name = name
    new.id = id
    new.pw = pw
    db.session.add(new)
    db.session.commit()
    return jsonify({
        "id": id,
        "pw": pw,
        "data": [
            "heheheheheh",
            "wowowowowowo",
            "hell yeah",
        ]
    })



@app.route("/search/<name>/<id>/<pw>")
def search(name, id, pw, is_web=True):
    found = User.query.filter(
        User.name == name,
        User.id == id,
        User.pw == pw,
    ).first()
    if found:
        if is_web:
            return 'success! %s' % (found.id, )
        else:
            return found
    if is_web:
        return 'failed'
    else:
        return None


@app.route("/delete/<name>/<id>/<pw>")
def delete(name, id, pw):
    found = search(name, id, pw, is_web=False)
    db.session.delete(found)
    db.session.commit()
    return 'deleted!'
@app.route("/g_search",methods=['GET'])
def g_search():
    return "dasdsa"
@app.route("/register")
def register():
    return render_template(
        "register.html"
    )
@app.route("/r_success",methods=['GET','POST'])
def r_success():
    nickname = request.form['nickname']
    email = request.form['email']
    passwd = request.form['passwd']
    repasswd = request.form['repasswd']
    if passwd != repasswd:
        return "비밀번호가 다릅니다."
    if len(passwd) < 8:
        return '''
             <script>
             alert("비밀번호를 8자리 이상 적어주세요.");
            history.back();
             </script>
        '''
    if not len(email) or not len(nickname):
        return '''
             <script>
             alert("모두 채워 주세요.");
            history.back();
             </script>
            '''
    if is_already_registered(email,nickname) == 2:
        return '메일'
    if is_already_registered(email,nickname) == 3:
        return '별명'
    new = User()
    new.nickname = nickname
    new.email = email
    new.pw = passwd
    db.session.add(new)
    db.session.commit()
    return render_template(
        "index.html"
    )
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('index.html')
@app.route("/login")
def login():
    if session['logged_in']:
        return hello()
    return render_template(
        "login.html"
    )
@app.route("/l_success",methods=['GET','POST'])
def l_success():

    username = request.form['email']
    password = request.form['passwd']

    found = User.query.filter(
        User.email == username,
        User.pw == password,
    ).first()
    if found:
        session['logged_in'] = True
        resp = make_response(hello())
        resp.set_cookie('username', username)
        print(session['logged_in'])
        return resp
    else :
        return '''
             <script>
             alert("로그인 실패!");
            history.back();
             </script>
        '''

@app.route("/success")
def success():
    username = request.cookies.get('username')
    return "<h1>" + str(username)
def is_already_registered(email,nickname):
    found = User.query.filter(
        User.email == email,
    ).first()
    found2 = User.query.filter(
        User.nickname == nickname,
    ).first()
    if found:
        return 2
    if found2:
        return 3

    return False




if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)