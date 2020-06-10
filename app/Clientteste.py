import cv2, base64, requests
import numpy as np


face_cascade= cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_alt2.xml')
eye_cascade= cv2.CascadeClassifier('cascades\data\haarcascade_eye.xml')
perfil_cascade= cv2.CascadeClassifier('cascades\data\haarcascade_profileface.xml')

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

URL="http://192.168.1.81:5000/receiveImage"
# Capturing video from webcam:
cap = cv2.VideoCapture(0)
flag = 0

face_detect = dlib.get_frontal_face_detector()

rects = face_detect(gray, 1)
for (i, rect) in enumerate(rects):
    (x, y, w, h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 255), 3)

plt.figure(figsize=(12,8))
plt.imshow(gray, cmap='gray')
plt.show()

while True:

    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = face_detect(gray, 1)

    for (i, rect) in enumerate(rects):

        (x, y, w, h) = face_utils.rect_to_bb(rect)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Handles the mirroring of the current frame
        frame = cv2.flip(frame, 1)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        k = cv2.waitKey(30)
        if k % 256 == 27:
            break
        elif k % 256 == 32:
            # Sends Post to save image of the current frame in jpg file in server
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            jpg_as_text = base64.b64encode(frame)
            print("jpg_as_text")
            print(jpg_as_text)
            json = {'image': jpg_as_text}
            r = requests.post(url=URL, data=json)


        # To stop duplicate images
        currentFrame += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()