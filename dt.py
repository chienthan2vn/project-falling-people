import torch
from keras.models import load_model
import cv2
import numpy as np
import pandas as pd

#load models
path = './best.pt'
model = torch.hub.load("WongKinYiu/yolov7","custom",f"{path}")
def mode(sp):
    return model(sp)
#detect img
def img(url):
    frame = cv2.imread(url)
    detect = model(frame)
    # detect.crop()
    # detect.save(save_dir='detect')
    # im = detect.render()[0]
    rs = detect.pandas().xyxy[0].to_dict(orient="records")
    for location in rs:
        xmax, xmin, ymax, ymin = location['xmax'], location['xmin'], location['ymax'], location['ymin']
        check = (xmax - xmin) / (ymax - ymin)
        if check > 1.2:
            cv2.rectangle(frame, (round(xmin), round(ymin)), (round(xmax), round(ymax)), (0, 0, 255), 1)
            cv2.putText(frame, 'Falling people', (round(xmin) - 10, round(ymin) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.6, (232, 71, 71),2)
    cv2.imshow('gg', frame)
    cv2.waitKey()
# img('./test1.jpg')

#detect video
def video(url):
    frame = cv2.VideoCapture(url)
    fps = frame.get(cv2.CAP_PROP_FPS)
    img_array = []
    while True:
        ret, img = frame.read()
        if not ret: break
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detect = model(img)
        # im = detect.render()[0]
        rs = detect.pandas().xyxy[0].to_dict(orient="records")
        for location in rs:
            xmax, xmin, ymax, ymin = location['xmax'], location['xmin'], location['ymax'], location['ymin']
            check = (xmax - xmin) / (ymax - ymin)
            if check > 1.5:
                cv2.rectangle(img, (round(xmin), round(ymin)), (round(xmax), round(ymax)), (0, 255, 0), 2)
                cv2.putText(img, 'Falling people', (round(xmin) - 10, round(ymin) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.6, (232, 71, 71),2)
        cv2.imshow('video', img)
        if cv2.waitKey(1) == ord('q'):
            break
# video('./yolov7/test.mp4')

def webcam():
    frame = cv2.VideoCapture(0)
    while True:
        _, img = frame.read()
        img = cv2.flip(img, 1)
        detect = model(img)
        # im = detect.render()[0]
        rs = detect.pandas().xyxy[0].to_dict(orient="records")
        # ar = np.array(rs)
        for location in rs:
            xmax, xmin, ymax, ymin = location['xmax'], location['xmin'], location['ymax'], location['ymin']
            check = (xmax - xmin) / (ymax - ymin)
            if check > 1.5:
                cv2.rectangle(img, (round(xmin), round(ymin)), (round(xmax), round(ymax)), (0, 255, 0), 2)
                cv2.putText(img, 'Falling people', (round(xmin) - 10, round(ymin) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.6, (232, 71, 71),2)
        cv2.imshow('video', img)
        if cv2.waitKey(1) == ord('q'):
            break

webcam()