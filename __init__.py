import os, sys
from flask import Flask, request, Response
from flask.templating import render_template

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

@app.route('/test_get')
def test_get():
    return render_template('test_get.html')

@app.route('/test_post', methods=['GET', 'POST'])
def test_post():
    if request.method == 'POST':
        # Reference Image
        refer_img = request.form['refer_img']
        refer_img_path = 'images/test_get/' + str(refer_img)

        # User Image (target image)
        user_img = request.files['user_img']
        user_img.save('./aws-flask/static/images/' + str(user_img.filename))
        user_img_path = 'images/' + str(user_img.filename)

        # Neural Style Transfer
        # transfer_img = neural_style_transfer.main(refer_img_path, user_img_path)
        # transfer_img_path = 'images/'+str(transfer_img.split('/')[-1])
        transfer_img_path = 'images/test_result_/test_reference1.png'

    return render_template('test_post.html', refer_img=refer_img_path,
                           user_img=user_img_path, transfer_img=transfer_img_path)


@app.route('/ocr_get')
def ocr_get():
    return render_template('ocr_get.html')

@app.route('/ocr_post', methods=['GET', 'POST'])
def ocr_post():
    if request.method == 'POST':

        # User Image (target image)
        ocr_img = request.files['ocr_img']
        ocr_img.save('./aws-flask/static/images/' + str(ocr_img.filename))
        ocr_img_path = 'images/' + str(ocr_img.filename)

        # Optical Character Recognition
        # tr_img = neural_style_transfer.main(refer_img_path, user_img_path)
        # transfer_img_path = '.static/images/'+str(transfer_img.split('/')[-1])

    return render_template('test_post.html', ocr_img=ocr_img_path)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
