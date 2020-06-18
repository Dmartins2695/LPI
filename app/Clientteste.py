class camPage(QMainWindow):
    def __init__(self):
        super(camPage, self).__init__()
        loadUi('webCam.ui', self)
        self.cap = cv2.VideoCapture(0)
        self.printTaken = -1
        self.closeFlag = 0
        self.currentFrame = 0
        self.face_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_alt2.xml')
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        self.btn_disable.clicked.connect(self.closeCvCam)
        self.btn_enable.clicked.connect(self.openCvCam)
        self.btn_leave.clicked.connect(self.leave)

    def sendPrintimg(self, frame):
        result, frame = cv2.imencode('.jpg', frame, self.encode_param)
        jpg_as_text = base64.b64encode(frame)
        json = {'image': jpg_as_text, 'studentName': credentials[0],
                'timestamp': datetime.now().strftime("%Hh%Mm%Ss")}
        postRequest = requests.post(url=URL + '/receiveImage', data=json)

    def openCvCam(self):
        cv2.namedWindow(credentials[0])
        while True:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
                if len(faces) > 0:
                    if self.printTaken == 1:
                        self.sendPrintimg(frame)
                    self.printTaken = 0
                else:
                    if self.printTaken == 0:
                        self.sendPrintimg(frame)
                        self.printTaken = 1
                # Handles the mirroring of the current frame
                frame = cv2.flip(frame, 1)
                # Display the resulting frame
                cv2.imshow(credentials[0], frame)
                if self.closeFlag == 1:
                    self.closeFlag = 0
                    break
                # To stop duplicate images
                self.currentFrame += 1
        self.cap.release()
        cv2.destroyWindow(credentials[0])


    def closeCvCam(self):
        self.closeFlag = 1


    def leave(self):
        pass