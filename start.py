import os, sys
from flask import Flask, request, Response
from flask.templating import render_template
# import neural_style_transfer

# os.getcwd()
real_path = os.path.dirname(os.path.realpath(__file__))
sub_path = os.path.split(real_path)[0]
os.chdir(sub_path)

app = Flask(__name__)
app.debug = True  # activating debug mode

# 사용자가 인덱스 페이지를 거치지 않고 바로 원하는 페이지로 접근할 수 있다면,
# 사용자는 그 페이지를 좋아할 것이고 다시 방문할 가능성이 커진다.
# main page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aws_info')
def aws_info():
    return render_template('aws_info.html')

@app.route('/flask_info')
def flask_info():
    return render_template('flask_info.html')

@app.route('/dl_info')
def dl_info():
    return render_template('dl_info.html')

@app.route('/nst_get')
def nst_get():
    return render_template('nst_get.html')

@app.route('/nst_post', methods=['GET', 'POST'])
def nst_post():
    if request.method == 'POST':
        # Reference Image
        refer_img = request.form['refer_img']
        refer_img_path = 'images/nst_get/' + str(refer_img)

        # User Image (target image)
        user_img = request.files['user_img']
        user_img.save('./aws-flask/static/images/' + str(user_img.filename))
        user_img_path = 'images/' + str(user_img.filename)

        # Neural Style Transfer
        # transfer_img = neural_style_transfer.main(refer_img_path, user_img_path)
        # transfer_img_path = 'images/nst_result_/'+str(transfer_img.split('/')[-1])
        # transfer_img_path = 'images/nst_result_/nst_reference1.png'
    # return render_template('nst_post.html', refer_img=refer_img_path,
    #                         user_img=user_img_path, transfer_img=transfer_img_path)

    return render_template('nst_post.html', refer_img=refer_img_path, user_img=user_img_path)

@app.route('/tsc_get')
def tsc_get():
    return render_template('tsc_get.html')

@app.route('/tsc_post', methods=['GET', 'POST'])
def tsc_post():
    if request.method == 'POST':

        # User Image (target image)
        tsc_img = request.files['tsc_img']
        tsc_img.save('./aws-flask/static/images/' + str(tsc_img.filename))
        tsc_img_path = 'images/' + str(tsc_img.filename)

        # Optical Character Recognition
        # tr_img = neural_style_transfer.main(refer_img_path, user_img_path)
        # transfer_img_path = '.static/images/'+str(transfer_img.split('/')[-1])

    return render_template('tsc_post.html', tsc_img=tsc_img_path)


@app.route('/tlad_get')
def tlad_get():
    return render_template('tlad_get.html')

@app.route('/tlad_post', methods=['GET', 'POST'])
def tlad_post():
    # if request.method == 'POST':

    return render_template('tsc_post.html')


@app.route('/ddd_get')
def ddd_get():
    return render_template('ddd_get.html')


@app.route('/ddd_post', methods=['GET', 'POST'])
def ddd_post():
    # if request.method == 'POST':

    return render_template('ddd_post.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
