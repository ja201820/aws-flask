import boto3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index2.html')


@app.route('/fileupload', methods=['POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        s3 = boto3.client('s3')
        s3.put_object(
            ACL="public-read",
            Bucket="{ja322-bucket}",
            Body=file,
            Key=file.filename,
            ContentType=file.content_type)

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run()