"""
Very basic blind of facial and/or eyes using CV.
Not a main focus but was potentially needed.
"""

# OpenCV program to detect face in real time
# import libraries of python OpenCV
# where its functionality resides
import cv2

# load the required trained XML classifiers
# https://github.com/opencv/opencv/tree/master
# data/haarcascades/haarcascade_frontalface_default.xml
# Trained XML classifiers describes some features of some
# object we want to detect a cascade function is trained
# from a lot of positive(faces) and negative(non-faces)
# images.
face_cascade = cv2.CascadeClassifier('facial_models/haarcascade_frontalface_default.xml')

# https://github.com/opencv/opencv/tree/master
# /data/haarcascades/haarcascade_eye.xml
# Trained XML file for detecting eyes
####Easiest way to copy into the director.  Will work on later.

eye_cascade = cv2.CascadeClassifier('facial_models/haarcascade_eye.xml')
#Note the eye detector works but has high level of mis or no ID.
# Need to try different of not use this model.

#Changing to basic img
img = cv2.imread('blind_face.jpg')
print(type(img))
    # convert to gray scale of each frames
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detects faces of different sizes in the input image
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in faces:
    # To draw a rectangle in a face

    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    img[y:y+h, x:x+w] = cv2.blur(roi_color, (31,31))
    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    # Detects eyes of different sizes in the input image
    eyes = eye_cascade.detectMultiScale(roi_gray)

    #To draw a rectangle in eyes
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,0), -1)

    # Display an image in a window
cv2.imshow('img', img)

    # Wait for Esc key to stop
cv2.waitKey(0)

# Close the window

# De-allocate any associated memory usage
cv2.destroyAllWindows()