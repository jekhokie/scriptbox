#!/usr/bin/env python
#
# Purpose: Perform face recognition based on the subjects in the subject directory.

import numpy as np
import cv2
import os
import yaml

# some configuration options
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
SUBJECTS_FOLDER = 'subjects'

# critical variables to application and classifer
subject_names = []
subject_faces = []
subject_ids = []

# create the classifier and recognizer for faces
fc = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
fr = cv2.face.LBPHFaceRecognizer_create()

# import subject names into an ordered list, with blank values for IDs not specified
def get_subject_names():
    # import subject mappings and print list
    print("Parsing subjects and creating ordered list...")
    with open('config/subject_mappings.yml', 'r') as yml:
        config = yaml.load(yml)

    # parse range of IDs, ensuring we fill in blank values so there are no gaps
    user_list = config['id_to_user']

    # ensure there is a zero-element (required)
    if 0 not in user_list:
        subject_names.append("")
        print("Adding user | ID: 0 | User: ''")

    for id, user in user_list.iteritems():
        subject_names.append(user)
        print("Adding user | ID: {} | User: {}".format(id, user))

# get all subject faces and corresponding IDs based on the subject dir structure
def get_subject_faces_and_ids():
    print("Obtaining training images available for subjects...")

    dirs = os.listdir(SUBJECTS_FOLDER)
    for subject_id in dirs:
        # ignore any hidden files
        if subject_id.startswith("."):
            continue

        # parse images within the folder
        subject_folder = "{}/{}".format(SUBJECTS_FOLDER, subject_id)
        subject_images = os.listdir(subject_folder)
        for subject_image in subject_images:
            # ignore any hidden files
            if subject_image.startswith("."):
                continue

            # read each image
            subject_image_path = "{}/{}".format(subject_folder, subject_image)
            subject_image_data = cv2.imread(subject_image_path)

            # train on each image
            print("Training on image: {}".format(subject_image_path))
            image = cv2.imread(subject_image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = fc.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10)

            # ensure we get a face in the image - if not, exit fatally as something has gone wrong
            if len(faces) == 1:
                (x, y, w, h) = faces[0]
                subject_faces.append(gray[y:y+h,x:x+w])
                subject_ids.append(int(subject_id))
            else:
                print("ERR: Could not detect a face (or detected multiple faces) in file: {}".format(subject_image))

get_subject_names()
print("--------------------------------------")

get_subject_faces_and_ids()
print("--------------------------------------")

# train the recognizer
print("Training recognizer...")
fr.train(subject_faces, np.array(subject_ids))

# start the application
print("Starting capture...")

# start video capture and set width/height of window
cap = cv2.VideoCapture(0)
cap.set(3, WINDOW_WIDTH)
cap.set(4, WINDOW_HEIGHT)

while(True):
    # capture each frame of the video stream, convert to grayscale
    # use classifier to detect, and recognizer to recognize
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = fc.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10)

    # calculate and display the containers for the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        id, confidence = fr.predict(gray[y:y+h,x:x+w])

        # confidence less than 100 is good - over 100 is bad and we will consider "unknown"
        if (confidence < 100):
            subject_name = subject_names[id]
            conf = "{}%".format(round(100 - confidence))
        else:
            subject_name = "<UNK>"
            conf = "{}%".format(round(100 - confidence))

        # output the identified name and corresponding confidence
        cv2.putText(frame, str("{} ({})".format(subject_name, conf)), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(30) & 0xFF == 27:
        break

# release the capture and destroy any GUI windows
cap.release()
cv2.destroyAllWindows()
