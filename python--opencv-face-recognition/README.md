# OpenCV Face Recognition

This is an extention to the OpenCV Face Detection project and will expand on face detection to apply
a subject name if the face is well-known (contained in the subjects list) to the program. The tutorial
has 2 scripts, the first being a support script to take a screen shot of a subject and store it, and
the second being the script which runs a continous video stream for capturing and attempting to recognize
the subjects based on the gold data set of the subjects.

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

## Usage - Subject Images

First, you'll want a set of subject images to use. The helper script `capture_subject.py` can be used
to take a single image of a subject identified by a subject ID and store it in the `subjects/` folder.
You will need at least 1 image per subject if you wish to have the program detect *and* recognize your
subjects.

To take an image of a subject, run the helper script and provide a subject ID (each subject should have
a unique ID, but each unique ID can have multiple source images to better enhance the recognition process):

```bash
$ python take_subject_image.py
# you should be prompted to provide a subject ID:
#   Please provide the subject ID:
# following face detection, a screen shot will be taken
# and stored of the subject, printing out the location of
# the image taken for reference
```

Following at least 1 subject image being taken, you can run the program to recognize subjects which exist
in the `subjects/` folder.

## Usage - Face Recognition

Now that you have subject images, you can run the application to detect and recognize the subjects you
have captured like so:

```bash
$ python recognize_face.py
```

A live video stream will ensue and any subject which is well known will be outlined with a blue box
with a corresponding name, while any face detected but not recognized will have a red box around it
indicating there is no subject match in the `subjects` folder.
