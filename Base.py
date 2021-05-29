import tkinter as tk
from tkinter import ttk
from MongoConnector import MongoConnector
from tkinter import messagebox
import os
import cv2
import threading
import re

################################################################################
# Class:          Base
# Author:         Duc Anh
# Last modified:  29 May 2021

################################################################################

class Base:
    '''
    All screen will extend this Base class. It contain some utilities for other
    class to use such as message box or the detector. The class will need a
    parent, expecting a frame or a window to be passed in and a store, which
    helps the state management of when the user logins.

    Attributes:
    ----------
    parent : tkinter window or frame
        The container for this screen
    messagebox : tkinter.messagebox
        The message box to show warning. Setting it here so other children
        classes don't need to import it
    store : dict
        This will contain information of the user after the user submitting
        username
    detector : opencv dnn_Net
        The detector that help face detection. It works like harr cascade but
        has more accuracy because of its deep learning nature.
    images_dir: str
        The file that a person's images will be saved. This is for face
        recognition.
    frame1 : tkinter frame
        The container for the left page
    frame2 : tkinter frame
        The container for the right page
    separator: tkk Separator
        The vertical line that divide the screen into 2 parts

    Methods:
    -------
    removeFrame(self, frame)
        Remove the frame and all of the children on that frames such as button,
        label...
    configureWidgetGrid(widget, horiz_split, vert_split)
        Divide the screen both horizontally and vertically to make a grid
    temporaryLabel(parent, text, x=0, y=0, fg="#000", second=2)
        Show a temporary label and make it disappear shortly
    __getDetectorFromPath(filepath="face_detector")
        Load the detector from local file
    checkCamera()
        Check if this device has camera
    resizeImage(img, new_w = None, new_h = None)
        Resize an image while keep the same width height ratio
    loadImage(parent, filename, new_h = None, new_w=None)
        Load image from the filename using Pillow to be used by Tkinter
    checkNullFields(func, **kwargs)
        Show a warning if any field in the form is empty
    clearScreen
        Helps clear both frame 1 and frame 2 and a separator of a frame
    '''
    def __init__(self, parent, store):
        """
        Recieve parent and the store to start the object of the base.

        Params:
        -------
            parent: tkinter frame or tk()
                The parent frame attach to this base
            store: dict
                The storage for some data from current user or the mongo
                connector. It act like a global storage for this app.

        """
        print(store)
        self.parent     = parent
        self.messagebox = messagebox
        self.store      = store
        self.connector  = store["connector"]
        self.detector   = self.__getDetectorFromPath("face_detector")
        self.images_dir = os.path.join(os.getcwd(), "new_faces")
        #Create frames and draw a separator for each screen
        #Draw a separator between 2 frames
        #https://stackoverflow.com/questions/42564608/why-isnt-this-ttk-separator-not-expanding-properly
        self.frame1     = tk.Frame(self.parent, bd = 1)
        self.frame2     = tk.Frame(self.parent, bd = 1)
        self.separator  = ttk.Separator(parent, orient=tk.VERTICAL)


        self.parent.grid_remove()
        self.parent.grid()
        #Add some information to the store
        self.store["has_cam"] = self.checkCamera()

        #Always change back to global dir when init the class
        #It's best to wait for the current thread to finish, otherwise the
        #directory will be wrong

        if "retrain_thread" in self.store:
            self.store["retrain_thread"].join()
        os.chdir(self.store["global_dir"])


    #A few helper methods for each screen =====================================

    def configureWidgetGrid(self, widget, horiz_split, vert_split):
        """
        Divide the screen by specifying how many vertical splits of the screen
        and how many horiontal splits of the screen. This method can help
        make the screen resizable and give better grid control by configuring
        all horiz_split and vert_split with the weight 1.

        Params:
        -------
            widget: tkinter container
                This can be a frame or a tk()
            horiz_split: int
                The number of horizontal split
            vert_split:
                The number of vertical splits of the page
        Return:
        -------
            None
        """
        for i in range(vert_split):
            widget.grid_columnconfigure(i, weight = 1)

        for j in range(horiz_split):
            widget.grid_rowconfigure(j, weight = 1)

    def checkNullFields(self, func, **kwargs):
        """
        Check if all fields from the form are filled. It will show and error
        message if any of them has no character.

        It then check if the password matches the confirm password

        Params:
        -------
            func : function
                The function that may change the label for each field in warning
            **kwargs: dict
                Expecting input such as label1 = field1, label2 = field2 ......
        Return:
        -------
            bool
                Return true if all field is filled otherwise return false.

        """
        labels      = list(kwargs.keys())
        fields      = list(kwargs.values())

        #Func exits means we need to change label
        if func:
            labels      = [func(label) for label in kwargs.keys()]

        if any([len(field) == 0 for field in fields]):
            print_warn  = []
            for i in range(len(fields)):
                if len(fields[i]) == 0:
                    print_warn.extend(labels[i])
                    print_warn.extend([",", " "])

            warning_string = ''.join(print_warn[:-2]) #Ignore the last ", " and " "
            self.messagebox.showerror("Not enough data", f"Please input {warning_string}")
            return False

        return True

    def check8CharsAnd1Num(self, stringToCheck):
        """
        This method check if a string has from 8 to 30 characters. It also
        search if the string have one digit or more.

        Params:
        ------
            stringToCheck : str
                The string to be checked
        Return:
        ------
            bool
                Return true if the re.search return any result
        """
        #A digit should appear somewhere, and the word should be in range
        #8 - 30 chars.
        #?= positve look ahead
        #https://stackoverflow.com/questions/24644334/regex-for-min-8-characters-and-at-least-1-number
        pattern = r"^(?=.+[0-9]).{8,30}$"
        return True if re.search(pattern, stringToCheck) else None

    def checkCapitalizeName(self, stringToCheck):
        """
        This method checks if a string is capitalized the first character
        of each word and have space in between. The maximum length for
        each word is 16. Not many people have that long name

        Params:
        ------
            stringToCheck : str
                The string to be checked
        Return:
        ------
            bool
                Return true if the re.search return any result
        """
        #https://stackoverflow.com/questions/15947614/regex-to-match-capitalized-words-with-a-single-space-between-them
        pattern = "^[A-Z]\w{1,16}( [A-Z]\w{1,16})*$"
        return True if re.search(pattern, stringToCheck) else None

    def temporaryLabel(self, parent, text, x=0, y=0, fg="#000", second=2):
        """
        Create a label on specific position and destroy it after a few second.
        The default is 2 second.

        Params:
        -------
            parent: tkinter container
                This can be a frame or a tk()
            text: str
                Some message that you want to display
            x: int
                The position x. Positive direction is east
            y: int
                The position y. Positive direction is downward
            fg: int
                The foreground for this label
            second: int
                The time in second that you want this label to appear
        Return:
        -------
            None
        """
        #https://stackoverflow.com/questions/59997984/placing-a-tkinter-label-on-screen-for-a-few-seconds-then-destroying-it
        temp_label = tk.Label(parent, text=text, font=("arial", "15"), fg=fg)
        temp_label.place(x=x, y=y)
        parent.update_idletasks()
        parent.after(int(second * 1000), temp_label.destroy())

    def removeFrame(self, frame):
        """
        Completly removes a frame and all of its children.

        Params:
        -------
            frame: tkinter frame
                The frame to be removed from the screen
        Return:
        -------
            None
        """
        for widget in frame.winfo_children():
            widget.destroy()

        frame.pack_forget()

    def clearScreen(self):
        """
        Clear the screen by removing both frame 1 and frame 2. It also destroy
        the separator
        Params:
        -------
            None
        Return:
        -------
            None

        """
        self.removeFrame(self.frame1)
        self.removeFrame(self.frame2)
        self.separator.destroy()
        #Here, the app will lose the row and column configuration and does not
        #apply new configuration. Don't know why?. So that, I destroy the
        #parent (in this case, a frame), create a new frame and set it again.
        self.parent.destroy()
        mainFrame = tk.Frame(self.store["root"], bg="#FFF")
        self.parent = mainFrame
        self.parent.grid(column=0, row=0, sticky="nsew")

    def __getDetectorFromPath(self, filepath="face_detector"):
        """
        Load the pre-trained model from open cv dnn face detection module. It
        will require a path that has a proto file "deploy.prototxt" and the net
        "res10_300x300_ssd_iter_140000.caffemodel"

        Params:
        -------
            filepath: str
                The path to a folder that has the 2 file for this detection
                module
        Return:
        -------
            open cv dnn Net:
                The deep learning model for face detection
        """
        dnn_model_dir = os.path.join(self.store["global_dir"], filepath)
        prototxt_path = os.path.join(dnn_model_dir, "deploy.prototxt")
        weights_path  = os.path.join(dnn_model_dir, "res10_300x300_ssd_iter_140000.caffemodel")
        detector      = cv2.dnn.readNet(prototxt_path, weights_path)

        return detector

    def checkCamera(self):
        #how to check if cam exits
        #https://stackoverflow.com/questions/48049886/how-to-correctly-check-if-a-camera-is-available
        """
        Check the camera of this device

        Params
        -------
            None
        Return:
        -------
            bool
                return true if this device has camera
        """
        if "has_cam" in self.store.keys():
            return self.store["has_cam"]

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if cap is None or not cap.isOpened():
            return False
        #Close the cam
        cap.release()
        cv2.destroyAllWindows()
        return True
