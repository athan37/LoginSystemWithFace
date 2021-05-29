import tkinter as tk
from tkinter import ttk
from MongoConnector import MongoConnector
from Base import Base
from screen1 import Screen1
import os

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
        self.store          = {"connector": MongoConnector(), "global_dir" : os.getcwd(), "root" : self.root}
        #The root is the to the store just in case any screen need it

        self.root.title("App")
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(background="#000000")
        self.configureWidgetGrid(self.root, 1, 1)


        self.mainFrame = tk.Frame(root, bg="#FFF")
        self.mainFrame.grid(column=0, row=0, sticky="nsew")

        Screen1(self.mainFrame, self.store)
        print(self.store)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
