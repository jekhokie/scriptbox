#!/usr/bin/env python
#
# Purpose: Parse a video stream from a web camera on a MacBook Pro (other devices may work, but have
#          not been tested) and detect/outline faces in the video stream.

import numpy as np
import cv2

# create the classifier for face and eye detection
fc = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
ec = cv2.CascadeClassifier('classifiers/haarcascade_eye.xml')

# print out some useful information
print("OpenCV Version Used: {}".format(cv2.__version__))
print("Press ESC to quit the application")

# start video capture and set width/height of window
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while(True):
    # capture each frame of the video stream
    ret, frame = cap.read()

    # convert the frame to grayscale, which is what the classifier expects
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image using the classifier
    faces = fc.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    # calculate the containers for the faces, and store a region of interest for eye parsing
    # (reduce computation requirements by only parsing area/region within the face box)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_orig = frame[y:y+h, x:x+w]

        # detect eyes in the face region
        eyes = ec.detectMultiScale(roi_gray, scaleFactor=1.2, minNeighbors=10)

        # calculate the containers for the eyes, and draw a box around each detected eye
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_orig, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(30) & 0xFF == 27:
        break

# release the capture and destroy any GUI windows
cap.release()
cv2.destroyAllWindows()
