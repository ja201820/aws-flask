import os, sys
from flask import Flask, request, Response
from flask.templating import render_template

app = Flask(__name__)
app.debug = True  # activating debug mode

# 사용자가 인덱스 페이지를 거치지 않고 바로 원하는 페이지로 접근할 수 있다면,
# 사용자는 그 페이지를 좋아할 것이고 다시 방문할 가능성이 커진다.
# main page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nst_get')
def nst_get():
    return render_template('test_get.html')

@app.route('/nst_post', methods=['GET', 'POST'])
def nst_post():
    if request.method == 'POST':
        # Reference image
        refer_img = request.form['refer.img']
        refer_img_path = 'static/images/'+str(refer_img)

    return render_template('test_post.html', refer_img=refer_img_path)




@app.route('/<user_name>/<int:user_id>')
def user(user_name, user_id):
    return f'Hello, {user_name}({user_id})!'

if __name__ == '__main__':
    app.run()
