import os, sys
from flask import Flask, request, Response
from flask.templating import render_template
import s3_controller
import neural_style_transfer
import drowsy_driving_detection
import cv2
import cvzone
from time import time, localtime
import datetime
from cvzone.PlotModule import LivePlot
from cvzone.FaceMeshModule import FaceMeshDetector  # 468 face landmarks

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
        transfer_img = neural_style_transfer.main(refer_img_path, user_img_path)
        transfer_img_path = 'images/nst_result_/'+str(transfer_img.split('/')[-1])
        # transfer_img_path = 'images/nst_result_/nst_reference1.png'

        # S3 upload
        # s3_controller.handle_upload_img('aws-flask/static/' + transfer_img_path)

    return render_template('nst_post.html', refer_img=refer_img_path,
                            user_img=user_img_path, transfer_img=transfer_img_path)


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
    lists = s3_controller.get_list()
    return render_template('ddd_get.html', lists=lists)
    # return render_template('ddd_get.html')


@app.route('/ddd_post', methods=['GET', 'POST'])
def ddd_post():
    if request.method == 'POST':
        # User Video (target video)
        user_video = request.files['user_video']
        user_video.save('./aws-flask/static/videos/' + str(user_video.filename))
        user_video_path = 'videos/' + str(user_video.filename)

        lists = s3_controller.get_list()
        for list in lists:
            if list == user_video.filename:
                break
            else:
                # S3 upload
                s3_controller.handle_upload_video('aws-flask/static/' + user_video_path)

        # drowsy driving detection
        transfer_video = drowsy_driving_detection.main(user_video_path)
        transfer_video_path = 'videos/ddd_result_/' + str(transfer_video.split('/')[-1])

        lists = s3_controller.get_list()
        for list in lists:
            if list == user_video.filename:
                break
            else:
                # S3 upload
                s3_controller.handle_upload_video('aws-flask/static/' + transfer_video_path)

    return render_template('ddd_post.html', user_video=user_video_path, transfer_video=transfer_video_path)





@app.route('/ddd_realtime')
def ddd_realtime():
    """Video streaming home page."""
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'Image Streaming',
        'time': timeString
    }
    return render_template('ddd_realtime.html', **templateData)


def gen_frames():
    cap = cv2.VideoCapture(0)

    # path = 'static/videos/ddd_result_/'
    # fname = path + target_video_name + '.mp4'
    # width = 640  # 또는 cap.get(3), cv2.CAP_PROP_FRAME_WIDTH
    # height = 720  # 또는 cap.get(4), cv2.CAP_PROP_FRAME_HEIGHT
    # fps = cap.get(cv2.CAP_PROP_FPS)  # 또는 cap.get(5)
    # fourcc = cv2.VideoWriter_fourcc(*'avc1')  # 코덱 정의
    # out = cv2.VideoWriter('test.mp4', fourcc, fps, (int(width), int(height)))  # VideoWriter 객체 정의

    detector = FaceMeshDetector(maxFaces=1)
    plotY = LivePlot(640, 360, [20, 50], invert=True)

    idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243,
              252, 253, 254, 256, 339, 384, 385, 386, 387, 388, 359, 463]
    leftRatioList = []
    rightRatioList = []
    drowsyDetection = 0
    drowsySec = []
    color = (255, 0, 255)
    pTime = 0
    cTime = 0
    cTimeLog = 0

    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            # cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            break

        success, img = cap.read()
        img, faces = detector.findFaceMesh(img, draw=False)

        if faces:
            face = faces[0]
            for id in idList:
                cv2.circle(img, face[id], 3, color, cv2.FILLED)

            # Left Eye
            leftUp = face[159]
            leftDown = face[23]
            leftLeft = face[130]
            leftRight = face[243]
            leftLengthVer, _ = detector.findDistance(leftUp, leftDown)
            leftLengthHor, _ = detector.findDistance(leftLeft, leftRight)
            cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
            cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)
            # normalize
            leftRatio = int((leftLengthVer/leftLengthHor)*100)
            leftRatioList.append(leftRatio)
            if len(leftRatioList) > 3:
                leftRatioList.pop(0)
            leftRatioAvg = sum(leftRatioList) / len(leftRatioList)

            # Right Eye
            rightUp = face[386]
            rightDown = face[253]
            rightLeft = face[359]
            rightRight = face[463]
            rightLengthVer, _ = detector.findDistance(rightUp, rightDown)
            rightLengthHor, _ = detector.findDistance(rightLeft, rightRight)
            cv2.line(img, rightUp, rightDown, (0, 200, 0), 3)
            cv2.line(img, rightLeft, rightRight, (0, 200, 0), 3)
            # normalize
            rightRatio = int((rightLengthVer / rightLengthHor) * 100)
            rightRatioList.append(rightRatio)
            if len(rightRatioList) > 3:
                rightRatioList.pop(0)
            rightRatioAvg = sum(rightRatioList) / len(rightRatioList)

            # BlinkCounter
            # if ratioAvg < 36 and counter == 0:
            #     blinkCounter += 1
            #     color = (0, 200, 0)
            #     counter = 1
            # if counter != 0:
            #     counter += 1
            #     if counter > 10:
            #         counter = 0
            #         color = (255, 0, 255)

            # DrowsyDrivingDetection
            if leftRatioAvg < 38 and rightRatioAvg < 38:
                drowsySec.append(cTime)
                drowsyDetection += 1
                color = (0, 200, 0)
                if drowsyDetection > 100:
                    drowsyTimer = drowsySec[-1] - drowsySec[0]
                    if drowsyTimer > 7:
                        drowsyDetection = 0
                        print(drowsyTimer)
                        # tm = localtime(drowsySec[-1])
                        # cTimeLog = f'{tm.tm_year}_{tm.tm_mon}_{tm.tm_mday}_{tm.tm_hour}_{tm.tm_min}_{tm.tm_sec}'
                        drowsySec.clear()
                    else:
                        tm = localtime(drowsySec[-1])
                        cTimeLog = f'{tm.tm_year}_{tm.tm_mon}_{tm.tm_mday}_{tm.tm_hour}_{tm.tm_min}_{tm.tm_sec}'
                        print(f"{cTimeLog}に居眠り運転を感知しました。エアコンを作動します。音楽をつけます。警察に通報します")
                        cvzone.putTextRect(img, f"{cTimeLog}に居眠り運転を感知しました。", (100, 10),
                                           colorR=color)
                        color = (255, 0, 255)
                        print(drowsyTimer)
                        drowsySec.clear()
                        drowsyDetection = 0

            cvzone.putTextRect(img, f'Drowsy Detection: {drowsyDetection}', (30, 50),
                               colorR=color)

            imgPlot = plotY.update(leftRatioAvg, color)
            img = cv2.resize(img, (640, 360))
            imgStack = cvzone.stackImages([img, imgPlot], 1, 2)
            imgStack = cv2.resize(imgStack, (640, 720))
        else:
            img = cv2.resize(img, (640, 360))
            imgStack = cvzone.stackImages([img, img], 1, 2)

        # out.write(imgStack)
        cv2.imshow("Image", imgStack)
        # cv2.waitKey(20)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, buffer = cv2.imencode('.jpg', imgStack)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()
    # out.realease()
    cv2.destroyAllWindows()


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")







