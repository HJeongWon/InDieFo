
from flask import (
    Flask ,
    render_template,
    request,
    session,
    make_response,
    redirect,
    url_for,
)
from db import (
    db,
    User,
    Board,
    migrate,

)
from sqlalchemy.sql import (
    func,

)
from admin import admin


app = Flask(__name__)
app.config.from_pyfile("configs.py")


admin.init_app(app)
db.init_app(app)

migrate.init_app(app,db)








@app.route("/")
def hello():
    return render_template("index.html")



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


def username():
    username = request.cookies.get('username')
    return username
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
@app.route("/<id>/main")
def g_main():
    return "Dsa"
@app.route("/<id>/write")
def write(id):
    if not session['logged_in']:
        return  '''
             <script>
             alert("로그인이 필요한 서비스 입니다.");
            history.back();
             </script>
        '''
    return render_template(
        "write.html"
    )
@app.route("/w_success",methods=['GET','POST'])
def w_success():

    board = Board()

    if request.method == "POST":
        title = request.form['title']
        text = request.form['textarea']


        board.title = title
        board.text = text
        board.writer = username()

        board.num = db.session.query(
            func.max(Board.num),
        ).one()[0]
        if board.num == None:
            board.num = 1
        else:
            board.num += 1






        db.session.add(board)
        db.session.commit()


    return redirect(url_for("list"))

@app.route("/list")
def list():
    pageCount = 1
    pageSize = 10
    if request.method=='GET':
        pageCount=int(request.args.get("page",1))
        board1 = Board.query.all()
        board1 = board1[(pageCount-1)*pageSize:pageCount*pageSize]
        return render_template("board.html",board = board1,)
    else:
        board1 = Board.query.all()
        board1 = board1[(pageCount-1)*pageSize:pageCount*pageSize]
        return render_template("board.html",board = board1,)


@app.route("/<int:id>")
def read(id):
    board = Board()
    board = board.query.get(id)
    board.count = db.session.query(
            func.max(Board.count),
        ).one()[0]
    if board.count == None:
        board.count = 0
    else:
        board.count += 1

    db.session.add(board)
    db.session.commit()

    return render_template(
        "read.html",board = board


    )


@app.route("/byebye")
def byebye():
    found = Board.query.all()
    for i in found:
        db.session.delete(i)
    db.session.commit()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)