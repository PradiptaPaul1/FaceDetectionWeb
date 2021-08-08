import cv2
import os
# from keras.models import load_model
# from keras.preprocessing.image import load_img, img_to_array
# import numpy as np

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# model = load_model('enew_mask_detector.h5')


img_width, img_height = 224, 224
font = cv2.FONT_HERSHEY_SIMPLEX
 # org
org = (1, 1)
class_lable = ' '
# fontScale
fontScale = 1  # 0.5
# Blue color in BGR
color = (255, 0, 0)
# Line thickness of 2 px
thickness = 2  # 1

class Video(object):
    def __init__(self, ip):
        self.video = cv2.VideoCapture(0)
        address = ("https://%s/video" % (ip))
        self.video.open(address)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()

        scale_percent = 40
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dsize = (width, height)
        frame1 = cv2.resize(frame, dsize)

        gray_img = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray_img,
                                          scaleFactor=1.2,
                                          minNeighbors=5,
                                          minSize=(200, 200),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
        for x, y, w, h in faces:
            x1, y1 = x + w, y + h
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 255), 1)
            cv2.line(frame1, (x, y), (x + 30, y), (255, 0, 255), 6)  # Top Left
            cv2.line(frame1, (x, y), (x, y + 30), (255, 0, 255), 6)

            cv2.line(frame1, (x1, y), (x1 - 30, y), (255, 0, 255), 6)  # Top Right
            cv2.line(frame1, (x1, y), (x1, y + 30), (255, 0, 255), 6)

            cv2.line(frame1, (x, y1), (x + 30, y1), (255, 0, 255), 6)  # Bottom Left
            cv2.line(frame1, (x, y1), (x, y1 - 30), (255, 0, 255), 6)

            cv2.line(frame1, (x1, y1), (x1 - 30, y1), (255, 0, 255), 6)  # Bottom right
            cv2.line(frame1, (x1, y1), (x1, y1 - 30), (255, 0, 255), 6)

        ret, jpg = cv2.imencode('.jpg',frame1)
        return jpg.tobytes()

class Video1(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()

        scale_percent = 40
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dsize = (width, height)
        frame1 = cv2.resize(frame, dsize)

        gray_img = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray_img,
                                          scaleFactor=1.2,
                                          minNeighbors=5,
                                          minSize=(200, 200),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
        for x, y, w, h in faces:
            x1, y1 = x + w, y + h
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 255), 1)
            cv2.line(frame1, (x, y), (x + 30, y), (255, 0, 255), 6)  # Top Left
            cv2.line(frame1, (x, y), (x, y + 30), (255, 0, 255), 6)

            cv2.line(frame1, (x1, y), (x1 - 30, y), (255, 0, 255), 6)  # Top Right
            cv2.line(frame1, (x1, y), (x1, y + 30), (255, 0, 255), 6)

            cv2.line(frame1, (x, y1), (x + 30, y1), (255, 0, 255), 6)  # Bottom Left
            cv2.line(frame1, (x, y1), (x, y1 - 30), (255, 0, 255), 6)

            cv2.line(frame1, (x1, y1), (x1 - 30, y1), (255, 0, 255), 6)  # Bottom right
            cv2.line(frame1, (x1, y1), (x1, y1 - 30), (255, 0, 255), 6)

        ret, jpg = cv2.imencode('.jpg',frame1)
        return jpg.tobytes()
