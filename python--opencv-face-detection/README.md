# OpenCV Face Detection

Re-visiting the old world of OpenCV, this tutorial is an effort in re-learning how to do face
detection using [OpenCV](https://opencv.org/). This script/project will use an on-board web camera
on a MacBook Pro (2017 model - can use other devices via updating the camera indicator) to capture
video and identify any faces in the image by applying a green box around the detected face.

This should lay the groundwork for moving along into face *recognition* (detection being identification
that there is a face present, recognition being able to tag/identify the face with a particular
subject based on a trained algorithm). As of now, this script can perform the following (the associated
classifiers are located in the `classifiers/` directory for ease of use/reference within the script).

- Face Detection
- Eye Detection

The tutorial will display the detected elements in a window with a real-time video feed and associated
rectangles around the detected features of individuals in the image.

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--opencv-face-detection
```

Install the required environment and libraries:

```bash
$ virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## Usage

Simply execute the script and the window will appear with associated features outlined:

```bash
$ python detect_face.py
```
