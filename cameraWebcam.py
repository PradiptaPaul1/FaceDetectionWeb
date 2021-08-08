import cv2
import os
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = load_model('enew_mask_detector.h5')

f = ['input', 'without_mask', 'with_mask']
for i in range(0, 3):
    folder_path = (f[i])
    test = os.listdir(folder_path)
    for images in test:
        if images.endswith('.jpg'):
            os.remove(os.path.join(folder_path, images))
    i = i + 1

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
        img_count = 0
        for x, y, w, h in faces:
            org = (x - 10, y - 10)
            img_count += 1
            color_face = frame1[y:y + h, x:x + w]  # color face
            cv2.imwrite(
                'input\%dface.jpg' % (img_count),
                color_face)
            img = load_img(
                'input\%dface.jpg' % (img_count),
                target_size=(img_width, img_height))

            img = img_to_array(img) / 255
            img = np.expand_dims(img, axis=0)
            pred_prob = model.predict(img)
            # print(pred_prob[0][0].round(2))
            pred = np.argmax(pred_prob)

            if pred == 0:
                print("User with mask - predic = ", pred_prob[0][0])
                class_lable = "Mask :"
                color = (0, 255, 0)
                class_lable = "{}: {:.2f}%".format(class_lable, (pred_prob[0][0]) * 100)

                cv2.imwrite('with_mask\%dface.jpg' % (
                    img_count), color_face)

            else:
                print('user not wearing mask - prob = ', pred_prob[0][1])
                class_lable = "No Mask :"
                color = (255, 0, 0)
                class_lable = "{}: {:.2f}%".format(class_lable, (pred_prob[0][1]) * 100)

                cv2.imwrite('without_mask\%dface.jpg' % (
                    img_count), color_face)

            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 6)
            # Using cv2.putText() method
            cv2.putText(frame1, class_lable, org, font,
                        fontScale, color, thickness, cv2.LINE_AA)


        ret, jpg = cv2.imencode('.jpg',frame1)
        return jpg.tobytes()
