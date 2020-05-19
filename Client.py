import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import base64
import requests



#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect(('192.168.1.124', 8485))
#connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 320);
cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

URL="http://192.168.1.99:5000/receiveImage"

frame = cv2.imread("C:\\Users\plato\PycharmProjects\Client\\venv\App\\assets\mooncompositemain-800x800.jpg")
result, frame = cv2.imencode('.jpg', frame, encode_param)
jpg_as_text = base64.b64encode(frame)
print("jpg_as_text")
print(jpg_as_text)
json={'image':jpg_as_text}
r = requests.post(url = URL, data = json)



    #data = zlib.compress(pickle.dumps(frame, 0))
   # data = pickle.dumps(frame, 0)
    #size = len(data)


   # print("{}: {}".format(img_counter, size))
   # client_socket.sendall(struct.pack(">L", size) + data)
    #img_counter += 1

cam.release()