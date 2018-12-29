#!/usr/bin/env python
#
# Purpose: Take a single image of a user and store it in the subjects folder for
#          face recognition purposes.

import numpy as np
import cv2
import os
import time
from datetime import datetime

# how long before the face detection kicks in, how many images to capture, and GUI sizing
COUNTDOWN_SECONDS = 5
IMAGE_COUNT = 10
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# create the classifier for faces
fc = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')

# start video capture and set width/height of window
cap = cv2.VideoCapture(0)
cap.set(3, WINDOW_WIDTH)
cap.set(4, WINDOW_HEIGHT)

# print out some useful information
print("OpenCV Version Used: {}".format(cv2.__version__))
subject_id = raw_input("Please enter a subject ID: ")

# prompt user to get ready for picture
print("Picture will be taken in 10 seconds")
raw_input("Image for subject {} will be taken next - please have subject present in front of camera, then press ENTER...".format(subject_id))

# organize output contents by creating ID folder if it does not yet exist
subject_folder = "subjects/{}".format(subject_id)
if not os.path.exists(subject_folder):
    os.makedirs(subject_folder)

# set variables for whether a face was detected and loop until a face is captured
image_count = 0
while image_count < IMAGE_COUNT:
    # capture each frame of the video stream
    ret, frame = cap.read()

    # convert the frame to grayscale, which is what the classifier expects
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image using the classifier
    faces = fc.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10)

    # skip if no faces were detected, and
    # ensure we only have 1 subject in the frame, otherwise we won't have a good gold copy for the subject
    if len(faces) == 0:
        continue
    elif len(faces) > 1:
        print("ERR: More than 1 face detected")
        continue

    for (x,y,w,h) in faces:
        # perform histogram equalization for better contrast
        gray_enhanced = cv2.equalizeHist(gray[y:y+h, x:x+w])

        # keep track of date/time of image
        image_name = datetime.now().strftime("%Y%m%d-%H%M%S.jpg")

        cv2.imwrite("{}/{}".format(subject_folder, image_name), gray_enhanced)
        print("Captured and stored image as: {}/{}".format(subject_folder, image_name))
        image_count += 1
        time.sleep(1)

    cv2.imshow('image', frame)
    if cv2.waitKey(30) & 0xFF == 27:
        break

# release the capture and destroy any GUI windows
cap.release()
cv2.destroyAllWindows()
