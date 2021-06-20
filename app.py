from flask import Flask, render_template, request, session, redirect
from func import ck_idpw # 내가 만든 id pw 체크 함수
import db

app = Flask(__name__)
app.secret_key = b'aaa!111/'

@app.route('/')
def hello():
    return render_template('taxi.html')

@app.route('/coin')
def coin():
    if 'user' in session:
        return '여기는 코인 거래소 로그인 사용자만~'
    else:
        return redirect('/login')  # 페이지 강제 이동

# 로그아웃(session 제거)
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/join_action', methods=['GET', 'POST'])
def join_action():
    if request.method == 'GET':
        return '나는 액션 GET 페이지야~'
    else:
        userid = request.form['userid']
        pwd = request.form['pwd']
        name = request.form['name']
        phone = request.form['phone']
        print(userid, pwd, name, phone)
        # 디비에 데이터 넣기
        db.insert_user(userid, pwd, name, phone)
        return '회원가입 성공!!@'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form['userid']
        pwd = request.form['pwd']
        print(userid, pwd)
        ret = db.get_idpw(userid, pwd)
        if ret != None:
            session['user'] = ret[3] # 로그인 처리
        return ck_idpw(ret)
        # if ck_idpw(userid, pwd):
        #     return '로그인 성공!!@'
        # else:
        #     return '가입 되지 않은 아이디나 패스워드 트림'

@app.route('/action_page', methods=['GET', 'POST'])
def action_page():
    if request.method == 'GET':
        return '나는 액션 GET 페이지야~'
    else:
        search = request.form['search']
        return '''당신은 '{}'로 검색을 했습니다<br>
        결과를 보여드리겠습니다. 잠시만 기다려주세요~<br>
        리스트 쫙~~~
        '''.format(search)

@app.route('/naver')
def naver():
    return render_template('naver.html')

@app.route('/taxi')
def taxi():
    return ''' 
    <!DOCTYPE html>
    <html>
    <body>

    <h2>모범택시</h2>
    <img src="https://img2.sbs.co.kr/img/sbs_cms/WE/2021/04/05/fNJ1617581491817.jpg" alt="모범택시" width="500" height="333">

    </body>
    </html>
    '''
# 웹브라우저에 http://127.0.0.1:5000/naver 
# 위와같이 접속 하면 안녕 나는 네이버야~
# 라는 글자를 나타나게 하시오

if __name__ == '__main__':
    app.run()