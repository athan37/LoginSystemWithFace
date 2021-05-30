import tkinter as tk
from MongoConnector import MongoConnector
from Base import Base
from predict_face import loadModelAndPCA, loginWithFace
import config as cfg
################################################################################
# Class:          Screen2
# Author:         Duc Anh
# Last modified:  29 May 2021

################################################################################

class Screen2(Base):
    '''
    The second screen when the app opens. It has 2 frame, the left frame is for
    login normally, and the right frame is for login with face. User can click
    on the open cam button to use this feature.

    Attributes:
    ----------
    frame1 : tkinter frame
        The container for the left page
    frame2 : tkinter frame
        The container for the right page
    separator: tkk Separator
        The vertical line that divide the screen into 2 parts
    frame1_label : tkinter Label
        The label for the big "Login with password" word
    password_label : tkinter Label
        The label for the password field
    password_field : tkinter Stringvar
        The field for the password
    password_entry : tkinter Entry
        The container for the password field
    login_btn_label : tkinter Label
        The label for the login button
    login_btn : tkinter Button
        The login button
    back_btn : tkinter Button
        The back button
    frame2_label : tkinter Label
        The label for the big Login with facial recognition word
    open_cam_btn : tkinter Button
        The button for opening camera to start login with face

    Methods:
    -------
    login(username, password)
        The method to login to the next screen
    back()
        Method to go back to the previous screen
    clearScreen()
        Clear all frame in this screen
    register_with_face()
        Register with face recognition
    clearScreen()
        Remove both screen from this screen and the separator
    loginWithFace()
        Open the camera to allow user login with face
    '''

    def __init__(self, parent, store):
        """
        Init the screen 2 with 2 frame on. The first frame is for login with
        password and the second frame is for login with face.

        This only load the recognizer and pca if the user has the face added
        and the device has camera.

        Params:
        -------
            parent: tkinter frame or tk()
                The parent frame attach to this base
            store: dict
                The storage for some data from current user or the mongo
                connector

        """
        super().__init__(parent, store)

        #Create components on frame 1 ==========================================
        self.frame1_label    = tk.Label(self.frame1, text="Login with password", font=("Arial", 20, "bold"))
        self.password_label  = tk.Label(self.frame1, text="Password: ")
        self.password_field  = tk.StringVar()
        self.password_entry  = tk.Entry(self.frame1, textvariable=self.password_field, show='*')
        self.login_btn_label = tk.StringVar()
        self.login_btn_label.set("Login")
        self.login_btn       = tk.Button(self.frame1,
                                textvariable=self.login_btn_label,
                                width=15,height=2,
                                command = lambda : self.login(self.store["username"], self.password_field.get()))

        self.back_btn        = tk.Button(self.frame1,
                                        text="Back",
                                        width=10, height=2,
                                        command = self.back)


        #Create components on frame 2 ==========================================
        self.frame2_label  = tk.Label(self.frame2,
                                font=("Arial", 20, "bold"),
                                text="Login with facial recognition")
        self.open_cam_btn  = tk.Button(self.frame2,
                                text="Open camera",
                                relief = tk.RAISED if self.store["face_added"] else tk.SUNKEN,
                                state = "normal" if self.store["has_cam"] else "disabled",
                                command = self.loginWithFace)

        #Config row and col for parent, frame1, and frame2 =====================
        # Params: widget, hori_split, vert_split Or it means
        #Num rows and num cols: Ex: 1, 2 means 1 row and 2 cols for the big grid
        self.configureWidgetGrid(self.parent, 1, 2)
        self.configureWidgetGrid(self.frame1, 3, 2)
        self.configureWidgetGrid(self.frame2, 3, 1)

        #Place components on containers ========================================
        self.separator.grid(column=0, row=0, sticky='nse')
        #Display frame1 and frame 2 on parent using grid layout
        # Set sticky="nsew" to make screen resizable
        self.frame1.grid(row = 0, column = 0, columnspan=1, rowspan=1, sticky="nsew")
        self.frame2.grid(row = 0, column = 1, columnspan=1, rowspan=1, sticky="nsew")
        #Add components to frame 1 grid
        self.password_label.grid(column=0, row=1, sticky="e")
        self.password_entry.grid(column=1, row=1, sticky="w")
        self.login_btn.grid(column=1, row=2, sticky="wn")
        self.frame1_label.grid(column=0, row=0, columnspan=2)
        self.back_btn.grid(column=0, row=2, sticky="ws", padx=20, pady=20)
        #Add components to frame 2 grid
        self.frame2_label.grid(column=0, row=0, columnspan=2)
        self.open_cam_btn.grid(column=0, row=0, sticky='s')

        #Only load the model if this person has registered face
        if self.store["face_added"] == True and self.store["has_cam"]:
            import os
            print(os.getcwd())
            self.recognizer, self.pca = loadModelAndPCA(cfg.models["MODEL_NAME"],
                                                        cfg.models["PCA_NAME"])

    def login(self, username, password):
        """
        Login normally with username and password. This will call the method
        in database to check the password hash

        Params:
        -------
            username: str
                The input username
            password: str
                The input password

        Return:
        -------
            None
        """
        if len(password) == 0:
            self.messagebox.showerror("No password", "Please enter password")
            return #Break out of this function

        result = self.connector.loginWithPass(username, password)

        if result:
            self.clearScreen()
            from screen3 import Screen3
            Screen3(self.parent, self.store)
        else:
            self.temporaryLabel(self.frame1, "Wrong password",
                                x=200, y=175, fg="#F00", second=1)

    def back(self):
        """
        This change the app back to screen 1. It has import statement here to
        avoid circular import

        Before changing back, it needs to clean the current screen.
        Params:
        -------
            None

        Return:
        -------
            None

        """
        self.clearScreen()
        from screen1 import Screen1
        Screen1(self.parent, self.store)

    def loginWithFace(self):
        """
        Login with face. It will call the method from the predict face module
        to predict the face.

        If success, the app advances to the next screen

        Params:
        -------
            None

        Return:
        -------
            None
        """
        #store, detector, recognizer, pca
        if self.store["face_added"] == True:
            success = loginWithFace(self.store, self.detector, self.recognizer, self.pca)
            if success:
                self.clearScreen()
                from screen3 import Screen3
                Screen3(self.parent, self.store)
            else:
                self.temporaryLabel(self.frame2, "Login failed. Try again",
                                    x=220, y=420, fg="#F00", second=1)
        else:
            self.temporaryLabel(self.frame2, "You haven't added face recognition",
                                x=220, y=420, fg="#F00", second=1)
