def openCvCam(self):
    cv2.namedWindow(credentials[0])
    self.cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_alt2.xml')
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    currentFrame = 0
    while True:
        if self.cap.isOpened():
            self.faceDetected = 0  # não encontrou cara
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
                if faces is not None:
                    self.faceDetected = 1  # encontrou cara
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
                # Handles the mirroring of the current frame
                frame = cv2.flip(frame, 1)
                # Display the resulting frame
                cv2.imshow(credentials[0], frame)
                if self.faceDetected == 1 and self.printTaken == 1 or self.faceDetected == 0 and self.printTaken == 0:  # tem cara e já tirou print ou nao tem cara e nao tirou print
                    # Sends Post to save image of the current frame in jpg file in server
                    result, frame = cv2.imencode('.jpg', frame, encode_param)
                    jpg_as_text = base64.b64encode(frame)
                    json = {'image': jpg_as_text, 'studentName': credentials[0],
                            'timestamp': datetime.now().strftime("%Hh%Mm%Ss")}
                    postRequest = requests.post(url=URL + '/receiveImage', data=json)
                    if self.faceDetected == 0:  # se nao tem cara já tirou um print
                        self.printTaken = 1  # 1º print tirado
                if self.faceDetected == 1:  # encontrou cara novamente tira outro print
                    self.printTaken = 0  # segundo print tirado volta ao inicio cara e sem print
                if self.closeFlag == 1:
                    self.closeFlag = 0
                    break
                # To stop duplicate images
                currentFrame += 1