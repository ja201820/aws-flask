import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector  # 468 face landmarks
from cvzone.PlotModule import LivePlot
import time
import os


def main(target_video_path):
    cap = cv2.VideoCapture(target_video_path)
    # cap = cv2.VideoCapture(0)

    # 비디오 저장
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # 또는 cap.get(3)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 또는 cap.get(4)
    fps = cap.get(cv2.CAP_PROP_FPS)  # 또는 cap.get(5)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # 코덱 정의
    out = cv2.VideoWriter('static/videos/ddd_result_/result.mp4', fourcc, fps, (int(width), int(height)))  # VideoWriter 객체 정의

    detector = FaceMeshDetector(maxFaces=1)
    plotY = LivePlot(640, 360, [20, 50], invert=True)

    idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243,
              252, 253, 254, 256, 339, 384, 385, 386, 387, 388, 359, 463]
    leftRatioList = []
    rightRatioList = []
    drowsyDetection = 0
    drowsySec = []
    drowsyTimer = 0
    color = (255, 0, 255)
    pTime = 0
    cTime = 0
    sec = 0



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
                        drowsySec.clear()
                    else:
                        print("居眠り運転を感知しました。エアコンを作動します。音楽をつけます。警察に通報します")
                        color = (255, 0, 255)
                        print(drowsyTimer)
                        drowsySec.clear()
                        drowsyDetection = 0

            cvzone.putTextRect(img, f'Drowsy Detection: {drowsyDetection}', (30, 50),
                               colorR=color)
            out.write(img)
            imgPlot = plotY.update(leftRatioAvg, color)
            img = cv2.resize(img, (640, 360))
            imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
        else:
            img = cv2.resize(img, (640, 360))
            imgStack = cvzone.stackImages([img, img], 2, 1)


        # Frame rate
        cTime = time.time()
        sec = cTime-pTime
        fps = 1/sec
        pTime = cTime
        cv2.putText(imgStack, str(int(fps)), (10, 350), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)


        cv2.imshow("Image", imgStack)
        # cv2.waitKey(20)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 작업 완료 후 해제
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main('static/videos/test2.mp4')