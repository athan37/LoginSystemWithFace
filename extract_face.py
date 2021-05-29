################################################################################
# Author:         Duc Anh
# Last modified:  29 May 2021

################################################################################
'''
This file is used to extract face. First, it will detect if there is a face in
each images from the images directory. It will then crop out the face if it
existed in the image. Here, the orginal data set is taken from Caltech.
Finally, the dataset will be generated each time the user register data, and
the model won't depends on the Caltech dataset. It only takes the julie image
(choosing randomly the directory with more than 15 sample) as the first dataset
and then wait for image from real user. This is because the model classes have
to be bigger than 1 to be train.

This file will use pre-trained open cv deep learning face detector. This
detector requires deploy.prototxt and res10_300x300_ssd_iter_140000.caffemodel.
These files are stored in the face_detector folder.
Documentation for opencv dnn: https://docs.opencv.org/master/d6/d0f/group__dnn.html

'''

import cv2
import numpy as np
import json
import os
#### Heplers, cannot be called outside this class ##############################
def __cropImageFromDetection(img, rect, size = 32):
    """
    This methods crop out the image using the rect data to extract the
    face region from the given image. After that, it will resize the image
    to size x size. The default is 128 x 128

    Params:
    -------
    img : numpy.ndarray
        The image that has face
    rect : array
        an array that stores x1, y1, x2, y2 position to crop the image.
        It's the position from the top left corner of the image to the
        lower right corner.

    Return:
    -------
        numpy.ndarray
            The cropped face with the dimension size x size
    """
    #Extract features inside the detected area
    [x1, y1, x2, y2] = rect
    #Extract, resize and convert to gray scale for this face region
    face_img  = img[y1 : y2, x1 : x2]

    try:
        face_img  = cv2.resize(face_img, (size, size))
        face_img  = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    except Exception:
        print("Cannot extract face")


    return face_img

################################################################################
def detectFace(detector, img):
    """
    This relies on the open cv dnn deep learning model to detect the face
    location from the image. The detector require a blob, so that, the
    method cv2.dnn.blobFromImage is used.

    Params:
    -------
    detector: deep learning model
        The open cv face detection model
    img : numpy.ndarray
        The image that has face
    Return:
    -------
        numpy.ndarray
            The cropped face with the dimension size x size
    """
    scale              = 1.0
    size               = (300, 300) #Input size Size taken from the deploy.prototxt
    mean_substract_val = (104, 177, 123)
    #mean_subtract_val for human face docs
    #https://github.com/opencv/opencv/tree/master/samples/dnn
    try:
        ### To use the detector above, we need to pass in an image as a blob, which can
        ### be created using cv2.dnn.blobFromImage
        blob  = cv2.dnn.blobFromImage(img, scale, size, mean_substract_val)
        #input the image and get face detection result
        detector.setInput(blob)
        detections = detector.forward()
        #This return an 4D array. Read more:
        #https://stackoverflow.com/questions/67355960/what-does-the-4d-array-returned-by-net-forward-in-opencv-dnn-means-i-have-lit
    except Exception:
        return None


    #Read data from this neural network
    #https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/
    h, w = img.shape[:2] # height x width because of num rows x num cols
    list_boxes = []
    scaled_box = None
    for i in range(detections.shape[2]):
        #Confidence probability of this detection
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            #this box is normalized
            #box return startX, startY, endX, endY
            box         = detections[0, 0, i, 3:7]
            #Return here

            scaled_box  = box * [w, h, w, h]
            list_boxes.append(scaled_box)

            #Only take take the image that has 1 face only
            if len(list_boxes) > 1:
                print("More than 1 face was detected")
                return None
            if len(list_boxes) == 0:
                print("No face detected")
                return None

        if type(scaled_box) == type(None):
            return None

    return scaled_box.astype("int") #Convert to integer array for slicing

def getFeaturesFromImage(detector, img):
    """
    This method get the face from the image, use __cropImageFromDetection
    to extract and resize the face. It then flatten the array and return it
    as 1 feature row.

    Params:
    -------
    detector: deep learning model
        The open cv face detection model
    img : numpy.ndarray
        The image that has face
    Return:
    -------
        numpy.ndarray
            The faltten array from the cropped face with the length
            size x size
    """
    face_area = detectFace(detector, img)

    #Check if inappropriate face was detected
    if face_area is not None:
        features  = __cropImageFromDetection(img, face_area)
        return features.flatten()

    return None

def loadDataFromImagesPath(detector, data_path, confidence_threshold = 0.5, minSample = 15):
    """
    This method load training set from the data_path, or the images directory
    that contains all faces of people.

    If the images from the directory is less than minSample, that directory
    will be ignored in order to improve the accuracy of the model

    Params:
    -------
    detector: deep learning model
        The open cv face detection model
    data_path : str
        The path to images directory
    confidence_threshold : float
        The minimum probaility of the prediction
    minSample : int
        The minimum number of images in the directory.
    Return:
    -------
        tuple
            The tuple contains features and labels numpy arrays
    """
    features = []
    labels   = []

    #Check if the filepath has enough data
    filtered_path = [(root, dirs, files) for (root, dirs, files) in os.walk(data_path) if len(os.listdir(root)) >= minSample]
    # pdb.set_trace()
    for root, dirs, files in filtered_path:
        for filename in files:
            person_name = root.split(os.sep)[-1]
            img_path    = os.path.join(root, filename)
            img         = cv2.imread(img_path)
            face_img    = getFeaturesFromImage(detector, img)

            if face_img is not None:
                #Append both features and label of this image at the same time
                features.append(face_img)
                labels.append(person_name)

    #Convert to np array for later processing
    features = np.asarray(features)
    labels   = np.asarray(labels)

    return features, labels
