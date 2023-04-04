import socket
import cv2
import torch
import pandas
import datetime
import pickle
import struct

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 2048


#load models
path = './best.pt'
model = torch.hub.load("WongKinYiu/yolov7","custom",f"{path}")


def webcam():
    # ADD
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Connecting to the server. """
    client.connect(ADDR)

    frame = cv2.VideoCapture(0)
    k, h = 0, 1
    while True:
        _, img = frame.read()
        img = cv2.flip(img, 1)
        detect = model(img)
        # im = detect.render()[0]
        rs = detect.pandas().xyxy[0].to_dict(orient="records")
        # ar = np.array(rs)
        for location in rs:
            xmax, xmin, ymax, ymin = location['xmax'], location['xmin'], location['ymax'], location['ymin']
            cv2.rectangle(img, (round(xmin), round(ymin)), (round(xmax), round(ymax)), (0, 255, 0), 2)
            check = (xmax - xmin) / (ymax - ymin)
            if check > 1.5:
                k = h
                cv2.putText(img, 'Falling people', (round(xmin) - 10, round(ymin) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.6, (232, 71, 71),2)
            else:
                h = 1
            if k == 1:
                h = 0
                now = str(datetime.datetime.now())[0:19]
                client.send(now.encode())

                now = str(datetime.datetime.now())[0:19].replace(' ', '_').replace(':', '_').replace('-', '_')
                client.send(now.encode())

                data = pickle.dumps(img)
                client.sendall(struct.pack("L", len(data))+data)
        cv2.imshow('video', img)
        if cv2.waitKey(1) == ord('q'):
            break
webcam()