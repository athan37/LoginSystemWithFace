import tkinter as tk
from tkinter import ttk
from MongoConnector import MongoConnector
from Base import Base
from screen1 import Screen1
import os
import cv2
from local_manager import LocalImagesDataManager
import config as cfg
################################################################################
# Class:          App
# Author:         Duc Anh
# Last modified:  29 May 2021

################################################################################

class App(Base):
    """
    This app will provide a root for all the screen. It first call the screen 1,
    and let all screen communicate to each other by themselves. The App class
    only provides the Tk root for these frames (screen) to operate on and clear
    themselves when the previous screen is disposed.

    Main class for the app. It depends on Screen1 class to display the first
    screen. It extends Base because I want to reuse the method
    configureWidgetGrid. This is different because this class is not a screen.
    So that, it doesn't call the super.__init__() because that will inherit all
    attributes from the Base class.

    Attributes:
        width : int
            the width of the root
        height : int
            the height of the root
        store : dict
            the initial store for the app. It begin with conenctor of the app
        root : tkinter Tk
            the Tk class from tkinter, which is the root

    Methods:
        None

    """
    def __init__(self, root):
        """
        Init class by recieving a root Tk. It set the screen size of the root,
        then configure the root so that all children frames can use the whole
        grid of the Tk. The store is initialized with a connector inside, so
        other screen can use it.

        Again, this class does not inheritance from the Base, it's not a screen.

        Params:
        -------
            root: tkinter Tk
                the Tk class from tkinter, which is the root

        """
        #Width and height of tk window
        self.width          = 1200
        self.height         = 600
        self.root           = root
        self.detector       = self.__getDetectorFromPath()
        self.store          = {
            "connector"     : MongoConnector(),
            "root"          : self.root,
            "detector"      : self.detector,
            "local_manager" : LocalImagesDataManager(self.detector)
        }
        #The root is points to the store just in case any screen need it

        self.root.title("App")
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(background="#000000")
        self.configureWidgetGrid(self.root, 1, 1)


        self.mainFrame = tk.Frame(root, bg="#FFF")
        self.mainFrame.grid(column=0, row=0, sticky="nsew")

        Screen1(self.mainFrame, self.store)
        print(self.store)

    def __getDetectorFromPath(self, filepath=cfg.detector["PATH"]):
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
        dnn_model_dir = os.path.join(os.getcwd(), filepath)
        prototxt_path = os.path.join(dnn_model_dir, cfg.detector["PROTO"])
        weights_path  = os.path.join(dnn_model_dir, cfg.detector["WEIGHTS"])
        detector      = cv2.dnn.readNet(prototxt_path, weights_path)

        return detector


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
