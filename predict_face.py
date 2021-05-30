import os
import cv2
import json
import time
import joblib
import hashlib

import numpy as np
from operator import itemgetter
from extract_face import detectFace, getFeaturesFromImage

from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

import config as cfg


################################################################################
# Author:         Duc Anh
# Last modified:  30 May 2021

#This file contains utilities such as function to save and load Model and Pca,
# It has 2 main functions which help register with face and login with face.
# Next, it has the check hash from prediction, which it generates hash from
# person directory name and person predicted name and the object id of the person to
# compare the hash from the server.

################################################################################

#Decorator ====================================================================
def local_db(func):
    """
    A decorator that helps other function to operate on the local database
    or storage from the current directory. This makes data from the app more
    organized

    The wrapper inside first change the directory from the current directory
    to the local database. Now, the func inside can operate on this new path
    and after it finished operate, it can return some result (such as None
    or sth else) and that return will be saved and return by the wrapper.
    This is important for changing the new current dir to the original
    current dir before the function ends.

    Params:
    -------
        func : function
            The function that wants to perform some operations in the local
            database directory
    Return:
    -------
        function
            The wrapper function
    """
    def wrapper(*args, **kwargs):
        #Switch to local db
        db_name     = cfg.local["BASE_DB"]
        current_dir = os.getcwd()
        db_path     = os.path.join(current_dir, db_name)

        if not os.path.exists(db_path):
            os.mkdir(db_name)
        os.chdir(db_path)
        #Call the function inside and save the result, this is important for
        #fruitful function such as loadModelAndPCA function below
        return_from_func = func(*args, **kwargs)
        #Switch back to current directory for other use
        os.chdir(current_dir)
        return return_from_func
    return wrapper

#Function that will have data saved into local files ===========================
@local_db
def loadModelAndPCA(model_filename, pca_filename):
    '''
    Load the face recognition model and its pca to detect new face. It requires
    the .pkl files of the model and pca and using joblib to load these files.

    Parameters:
    -----------
    model_filename : str
        the file name of the trained model
    pca_filename: str
        the file name of the pca that will be loaded

    Return:
    --------
    tuple:
        return a tuple containing the svc_model from
        sklearn.svm._classes.SVC and the pca used for that svc from
        sklearn.decomposition._pca.PCA

    '''
    svc_model = joblib.load(model_filename)
    pca       = joblib.load(pca_filename)
    return svc_model, pca

@local_db #Screen 2 method
def loginWithFace(store, detector, recognizer, pca):
    '''
    This function create the dictionary that map the person directory name to
    the real name of the person. This is because the directory name must be
    unique, but the person name can be the same for many people.

    The function will get the local dictionary mapping the filename to the
    real user's name. It will use call the method check hash with prediction
    to both detect face and generate the hash to compare with the hash face
    given in the store.

    If the hash failed times are over 10, this the method will return false.
    If the hash is true for 3 times, the person can login.

    Parameters:
    -----------
    store : dict
        The store from the app
    detector: deep learning model
        The open cv face detection model
    recognizer: sklearn svc
        The support vector classification model
    pca: sklearn pca
        The dimension reduction class for the model

    Return:
    --------
    True if the hash matches 3 times, else it return False

    '''

    correct_time        = 0
    incorrect_time      = 0
    false_detection     = 0 #Avoid showing random thing to the cam for too long
    detection_state     = False
    map_person_dir_name = getPersonNameByDirectoryDict()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        success, frame = cap.read()
        if success:
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            box  = detectFace(detector, frame)
            if false_detection == 50:
                break

            if box is None:
                print("No face detected. Skip to next frame")
                false_detection += 1
                continue

            try:
                # map_person_dir_name = getPersonNameByDirectoryDict()
                pred_label, pred_proba = recognize(pca, detector, recognizer, frame)
                if pred_label not in map_person_dir_name.keys():
                    pred_label = "Unknown"
                pred_name = map_person_dir_name[pred_label]
                check_face_result   = checkHashFromPrediction(pred_name, store, detector, recognizer, pca)
                text = f"{pred_name}: {pred_proba}%"

                x1, y1, x2, y2 = box
                green = (0, 255, 0)
                red   = (0, 0, 255) #cv2 is BGR
                color = green if check_face_result else red

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX,
                            1, color, 2)
                cv2.imshow('Face Detection', frame)

                if check_face_result:
                    correct_time += 1
                else:
                    incorrect_time += 1

                #If detection passes 3 times, it means the face is correct
                if correct_time == 3:
                    detection_state = True
                    break

                if incorrect_time == 10:
                    print("Detection failed. Try again")
                    break

            except Exception as ex:
                print(ex)
                continue

            #Must have this line in order to show video in open cv
            if cv2.waitKey(1) == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    # os.chdir(current_dir)
    return detection_state

@local_db #Screen 1 method
def registerWithFace(store, name, username, detector, images_dir):
    '''
    Register user face and save it to the images_dir directory. This images_dir
    comes from Base class.

    First, the function will create a unique path name base on the username
    and the new person name (or the uncapitalized name with all white space
    removed).

    It will open the camera and record 20 images of the person to images_dir
    for training. If there is any problem during the execution, it will
    remove the person path (images_dir + new_personame) and all the content
    within that path.

    When the program finish the recording of the images, it then load all the
    data from the images dir again, create new pca and new svc model with new
    data. Then the new pca and the new model is saved in the local database.
    The mapping of the person directory and the name of the person is also saved
    in the local database.

    Parameters:
    -----------
    username : str
        The person's images directory
    detector: deep learning model
        The open cv face detection model
    filename: str
        The filename of this dict
    images_dir: str
        The directory of all images

    Return:
    --------
    bool
        Return true if the face is successfully recorded in the database and
        the new model is trained and saved.

    '''
    try:
        #new image directory name from username and name to avoid duplicate
        #Also change name to lower case without separating character
        new_name = "".join(name.lower().split())
        person_dir = f"{username}_{new_name}"

        current_dir = os.getcwd()
        #Change to the given images directory
        os.chdir(images_dir)
        #new image directory name from username and name to avoid duplicate
        #Also change name to lower case without separating character
        new_name = "".join(name.lower().split())
        person_dir = f"{username}_{new_name}"
        if os.path.exists(person_dir):
            print("User already resigerted")
            os.chdir(current_dir)
            return
        os.mkdir(person_dir)
        #Go to the new directory to write image
        os.chdir(os.path.join(os.getcwd(), person_dir))

        i = 0
        #This is for direct input video capture
        #https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gga023786be1ee68a9105bf2e48c700294dab6ac3effa04f41ed5470375c85a23504
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        print("Booting camera")
        while True:
            success, frame = cap.read()
            if success:
                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                box  = detectFace(detector, frame)

                if box is None:
                    print("No face detected. Skip to next frame")
                    continue

                cv2.imshow('Recording face', frame)


                img_name = f"img_{i}.jpg"
                cv2.imwrite(img_name, frame)
                i += 1

            if i == 30: #Get about 15 - 20 images
                break

            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()


        #Any post processing after detection must be after os.chdir
        #Change back to original directory
        os.chdir(current_dir)

        #Add this name to local dictionary
        print(f"Loading new data and retrain from path: {images_dir}")
        X, y = store["local_manager"].registerNewData(person_dir)
        print("Saving mapping label")
        savePersonNameToDict(person_dir, name)
        #Save the new model
        saveModelAndPCA(X, y)

    except Exception as ex:
        print(ex)
        import shutil
            #Try removing unfinished directory of this person
        try:
            shutil.rmtree(os.path.join(images_dir, person_dir))
        except Exception:
            pass

        return False

    return True

#Helpers ======================================================================
# The save model and pca and save person to dict funcs save files into local db;
# however, it's called by resigter with face, so that it doesn't need to add
# @local_db wrapper
def saveModelAndPCA(X, y, model_filename = cfg.models["MODEL_NAME"],
    pca_filename = cfg.models["PCA_NAME"]):
    '''
    Recieves features X and label y and train the data set. It will split
    traning/testing by ratio 80/20 by using train_test_split from sckit learn.
    Will save these thing to local database directory.

    After calling this function, it will save the model by joblib as .pkl files.
    If .pkl files exist, it will force override these file.

    Parameters:
    ----------
        X : np.ndarray
            feature array extracted from the 128 x 128 face gray image extracted
            from the original image. Each image array is flatten to a 16384
            length array.
        y : np.ndarray
            the label taken from the name of each person's images directory.
        model_filename : str
            the file name of the training model after being trained
        pca_filename: str
            the file name to save the pca used for this model

    Returns:
    --------
        None
    '''

    #Calling train test split function
    #Increase test size to 0.3 to better recognize face
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    n_samples, n_features = X_train.shape

    desired_n_components = 150 #After a few trial and error, I think this is a
                                # value that's not overfit the data
    #Keep the n_component close to 150 no matter the training size
    #It's better to apply pca on the whole dataset
    pca = PCA(n_components=min(n_samples - 1, desired_n_components),
                svd_solver='randomized', whiten=True).fit(X)

    #Perform grid search to search for C value. It's similar to finding best k
    #Serach C in range 1-2 only because we are using 'rbf' kernel
    #C can be float
    #Not specifying gamma here because it takes long time and most of the time
    #the best gamma is 0.001 for the training
    param_grid = {'C' : [c for c in range(1, 15 + 1, 1)]}
    recognizer = GridSearchCV(
        SVC(kernel='rbf', probability=True, gamma=0.001), param_grid
    )
    recognizer.fit(pca.transform(X), y)
    print(f"Best estimator: C={recognizer.best_params_}")

    #Force dump new 2 files, this is needed each time a user registers
    print("Writing model and pca......")
    joblib.dump(recognizer.best_estimator_, model_filename)
    joblib.dump(pca, pca_filename)
    print("Write model and pca successfully")
    print(f"Saved model as {cfg.models['MODEL_NAME']}  and saved pca as {cfg.models['PCA_NAME']}")

def savePersonNameToDict(person_dir, name, filename=cfg.local["MAP_DIR2NAME_FILE"]):
    '''
    This function create the dictionary that map the person directory name to
    the real name of the person. This is because the directory name must be
    unique, but the person name can be the same for many people.

    Parameters:
    -----------
    person_dir : str
        The person's images directory
    name: str
        The name of the person
    filename: str
        The filename of this dict

    Return:
    --------
    None

    '''
    #Create default key Unknown for unknown face
    dict_ = {
                "Unknown" : "Unknown",
            }

    if os.path.exists(filename):
        print("Fetching name dict....")
        with open(filename, "r") as infile:
            data = infile.read()
        dict_ = json.loads(data)
    else:
        print(f"Writing new {filename}")

    #Add new mapping either having filename or not
    print(f"This dict type is: {type(dict_)}")
    dict_[person_dir] = name
    with open(filename, "w") as outfile:
        json.dump(dict_, outfile)
    print(f"Write successfully {dict_}")

def recognize(pca, detector, recognizer, img):
    '''
    This function use the pca and the svc model to predict the face of the
    person from the input image.

    It get the feature from the face image using function from extract face. Then
    use the given pca to transform the image before the prediction. Then,
    it will use the svc model to predict the processed img of the face.

    The label that has the highest prediction probability will be returned.
    However, if the probablity is <= 70, the prediction is discarded because
    it's too low.

    Parameters:
    -----------
    pca: sklearn pca
        The dimension reduction class for the model
    detector: deep learning model
        The open cv face detection model
    recognizer: sklearn svc
        The support vector classification model
    img : numpy.ndarray
        the array represents the image
    Return:
    --------
    tuple
        A tuple contain the predict label (the person directory name) and the
        pred_proba (the prediction probablity). If the pred_proba <= 70,
        it will return ("Unknown", prediction probability)

    '''
    img_features    = getFeaturesFromImage(detector, img)
    #put img_features inside an array. This is similar to have a dataset with
    #only one array of features
    features        = pca.transform([img_features])
    [prediction]    = recognizer.predict_proba(features)
    max_idx         = np.argmax(prediction)

    #Get this person name and the probability of this prediction
    pred_label      = recognizer.classes_[max_idx]
    pred_proba      = round(prediction[max_idx] * 100, 1) #Convert to %

    #Ignore prediction with low probability
    return (pred_label, pred_proba) if pred_proba > 70 else ("Unknown", pred_proba)

def getPersonNameByDirectoryDict(filename=cfg.local["MAP_DIR2NAME_FILE"]):
    '''
    This is a helper function that will be called inside login with face only.
    So that it doesn't need to be wrapped with local_db

    Parameters:
    -----------
    filename : str
        The name of the dictionary

    Return:
    --------
    dict
        The dictionary that map person directory with person name
    '''
    dict_ = {}

    print(os.getcwd())
    if os.path.exists(filename):
        print("Fetching name dict....")
        with open(filename, "r") as infile:
            data = infile.read()
        dict_ = json.loads(data)
    else:
        print(f"Cannot find {filename}")
        return None

    return dict_

def checkHashFromPrediction(pred_name, store, detector, recognizer, pca):
    '''
    This method generate the new hash using the person username + predicted_name.
    Hash the result and combine with the id from the database of the user.
    Then the result is hash again and compare with the hash face from the
    store.

    Parameters:
    -----------
    pred_name : str
        The prediction name after converted using the mapping dict
    store : dict
        the store from the app
    detector: deep learning model
        The open cv face detection model
    recognizer: sklearn svc
        The support vector classification model
    pca: sklearn pca
        The dimension reduction class for the model

    Return:
    --------
    bool
        Return true if the hash matches the hash_face of the user
    '''
    object_id, username, hash_face = itemgetter("_id", "username", "hash_face")(store)
    #Generate hash again base on detection
    bytes_username    = (username.lower() + pred_name.lower()).encode()
    user_hash_face    = hashlib.sha256(bytes_username).hexdigest()
    new_random_string = user_hash_face + str(object_id)
    new_hash_face     = hashlib.sha256(new_random_string.encode()).hexdigest()

    if new_hash_face == hash_face:
        return True

    return False
