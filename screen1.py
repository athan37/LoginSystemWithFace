import tkinter as tk
from tkinter import ttk
from Base import Base
from operator import itemgetter
from predict_face import registerWithFace

################################################################################
# Class:          Screen1
# Author:         Duc Anh
# Last modified:  29 May 2021

################################################################################

class Screen1(Base):
    '''
    The first screen when the app opens. It has the login and the register page.
    User have to type user name to move to the next screen. Also, user can
    choose to either register by face (with the register form filled) or
    register normally.

    Attributes:
    ----------
    frame1 : tkinter frame
        The container for the left page
    frame2 : tkinter frame
        The container for the right page
    separator: tkk Separator
        The vertical line that divide the screen into 2 parts
    login_frame_lab : tkinter Label
        The label for the big LOGIN word
    login_user_label : tkinter Label
        The label for the username
    login_user_field: tkinter Stringvar
        The actual field for the username field
    login_user_entry: tkinter Entry
        The container for the username field
    login_btn_text: tkinter Stringvar
        Text on the Next button for left page
    login_btn: tkinter Button
        The Next button to the second screen
    register_frame_lab : tkinter Label
        The label for the big word Register
    register_name_label : tkinter Label
        The lable for the name field
    register_name_field : tkinter Stringvar
        The field for the name
    register_name_entry : tkinter Entry
        The container for the name field
    register_user_label : tkinter Label
        The lable for the username field
    register_user_field : tkinter Stringvar
        The field for the username
    register_user_entry : tkinter Entry
        The container for the username field
    register_password_label : tkinter Label
        The lable for the password field
    register_password_field : tkinter Stringvar
        The field for the password
    register_password_entry : tkinter Entry
        The container for the password field
    register_confirm_label : tkinter Label
        The lable for the confirm password field
    register_confirm_field : tkinter Stringvar
        The field for the confirm password
    register_confirm_entry : tkinter Entry
        The container for the confirm password field
    register_btn: tkinter btn
        The register button
    self.add_face_txt : tk.StringVar
        The label for add face btn
    add_face_btn: tkinter btn
        The register with face button

    Methods:
    -------
    login()
        The method to login to the next screen
    register()
        Register regularly with name, username, and password
    registerWithFace()
        Register with face recognition
    clearScreen()
        Remove both screen from this screen and the separator

    '''
    def __init__(self, parent, store):
        """
        This screen extends the Base class.

        Create the first screen for user to login. The left side of the screen
        display the username field. It also contain the register function on
        the right side of the screen. User can choose to login with face or not.

        It also use some state from the store such as username to display it
        again when the user click the back button from screen 2

        Params:
        -------
            parent: tkinter frame or tk()
                The parent frame attach to this base
            store: dict
                The storage for some data from current user or the mongo
                connector

        """
        super().__init__(parent, store)

        #Create components on frame 1 =========================================
        self.login_frame_lab  = tk.Label(self.frame1, text="Login", font=("Arial", 20, "bold"))
        self.login_user_label = tk.Label(self.frame1, text="Username: ")
        self.login_user_field = tk.StringVar()
        self.login_user_entry = tk.Entry(self.frame1, textvariable=self.login_user_field)
        self.login_btn_text   = tk.StringVar()
        self.login_btn        = tk.Button(self.frame1,
                                textvariable=self.login_btn_text,
                                width=15,height=2,
                                command = self.login)


        #Create components on frame 2 =========================================
        self.register_frame_lab      = tk.Label(self.frame2, text="Register", font=("Arial", 20, "bold"))
        self.register_name_label     = tk.Label(self.frame2, text="Name: ")
        self.register_name_field     = tk.StringVar()
        self.register_name_entry     = tk.Entry(self.frame2, textvariable=self.register_name_field)
        self.register_user_label     = tk.Label(self.frame2, text="Username: ")
        self.register_user_field     = tk.StringVar()
        self.register_user_entry     = tk.Entry(self.frame2, textvariable=self.register_user_field)
        self.register_password_label = tk.Label(self.frame2, text="Password: ")
        self.register_password_field = tk.StringVar()
        self.register_password_entry = tk.Entry(self.frame2, textvariable=self.register_password_field, show='*')
        self.register_confirm_label  = tk.Label(self.frame2, text="Confirm password: ")
        self.register_confirm_field  = tk.StringVar()
        self.register_confirm_entry  = tk.Entry(self.frame2, textvariable=self.register_confirm_field, show='*')

        self.register_btn = tk.Button(self.frame2, text="Register", width=10,
                            height=2, command = self.register)
        self.add_face_txt = tk.StringVar()
        self.add_face_txt.set("Register with face recognition")
        self.add_face_btn = tk.Button(self.frame2,
                            width = 25, height = 2,
                            command = self.registerWithFace,
                            textvariable = self.add_face_txt,
                            state = "normal" if store["has_cam"] else "disabled") #No params are needed for add face

        #Config row and col for parent, frame1, and frame2 =======================
        # Params: widget, hori_split, vert_split Or it means
        #Num rows and num cols: Ex: 1, 2 means 1 row and 2 cols for the big grid
        self.configureWidgetGrid(self.parent, 1, 2) # Login and register pages
        self.configureWidgetGrid(self.frame1, 9, 2) #Login, Username, Next btn
        self.configureWidgetGrid(self.frame2, 9, 2) #Havent register, (name, user, pass), (2 buttons)

        #Configuring columns and rows for containers ===========================
        self.separator.grid(column=0, row=0, sticky='nse')
        #Placing component on grid
        #Placing component for parent
        self.frame1.grid(column = 0, row = 0, columnspan = 1, rowspan = 1, sticky="nsew")
        self.frame2.grid(column = 1, row = 0, columnspan = 1, rowspan = 1, sticky="nsew")
        #Placing component for frame 1
        self.login_frame_lab.grid(column = 1, row = 0, rowspan = 2, sticky="w")
        self.login_user_label.grid(column = 0, row = 3)
        self.login_user_entry.grid(column = 1, row = 3, sticky="w")
        self.login_btn.grid(column = 1, row = 7)
        #Placing component for frame 2
        self.register_frame_lab.grid(column = 1, row = 0, rowspan=2, sticky="w")
        self.register_name_label.grid(column = 0, row = 2)
        self.register_name_entry.grid(column = 1, row = 2, sticky="w")
        self.register_user_label.grid(column = 0, row = 3)
        self.register_user_entry.grid(column = 1, row = 3, sticky="w")
        self.register_password_label.grid(column = 0, row = 4)
        self.register_password_entry.grid(column = 1, row = 4, sticky="w")
        self.register_confirm_label.grid(column = 0, row = 5)
        self.register_confirm_entry.grid(column = 1, row = 5, sticky="w")
        self.add_face_btn.grid(column = 0, row = 7)
        self.register_btn.grid(column = 1, row = 7)

        #Add some text or logic on frames. This will keep the username appear
        #from screen 1 after clicking the back button from screen 2
        self.login_btn_text.set("Next")
        if "username" in self.store.keys():
            self.login_user_field.set(store["username"])


    #Methods for buttons from both frames ======================================
    def login(self):
        """
        Login function for the app. It only requires the login form is filled,
        which contains username, name, and password.

        The input user name will be checked by the Mongo connector to check for
        its existance. If it does not exits, the app will display a warning and
        reset the button.

        If the user exists, it will store the _id, username, hash_face, and
        face_added of the user to self.store and move to the screen 2.

        Params:
        -------
            No params. The class can take the username from the attribute
        Return:
        -------
            None

        """
        #dict_.has_key() was replaced by in operator
        #https://stackoverflow.com/questions/33727149/dict-object-has-no-attribute-has-key
        self.login_btn_text.set("Loading user...")

        #Use the line below to update the button text
        self.frame1.update_idletasks()
        username_str = self.login_user_field.get().strip()

        if len(username_str) == 0:
            self.messagebox.showerror("Cannot proceed", "Please enter username")
            self.login_btn_text.set("Next")
            return #Break out of this function

        response = self.connector.getUserByUname(username_str)

        #Set image text
        #https://www.youtube.com/watch?v=itRLRfuL_PQ&list=PLqXS1b2lRpYRVrpyN19e3vzLZfFoPLTRL&index=2
        if response:
            #Update the store. Without recieving the hash_pass
            self.store["_id"], self.store["username"], self.store["name"], \
            self.store["hash_face"], self.store["face_added"] = \
            itemgetter("_id", "username", "name", "hash_face", "face_added")(response)

            self.clearScreen()
            #Finish screen1, now call screen2.
            #Import here to avoid circular import
            from screen2 import Screen2
            Screen2(self.parent, self.store)

        else:
            self.login_btn_text.set("Next")
            self.messagebox.showerror("Cannot proceed", "User does not exist")

    def register(self):
        """
        Check if all 3 field from the form is filled. It will show and error
        message if any of them has no character.

        If success, the methods will sent an user to the database, leaving the
        "face_added" attribute of the user to False.

        Params:
        -------
            None
        Return:
        -------
            bool
                Return true if all field is filled otherwise return false.

        """
        name     = self.register_name_field.get().strip()
        username = self.register_user_field.get().strip()
        password = self.register_password_field.get().strip()
        #break out of the function if the form is not filled
        if not self.checkNullFields(None, name = name, username = username, password = password):
            return

        if not self.checkCapitalizeName(name):
            self.messagebox.showerror("Enter a valid name",
                f"Name must have white space and capitalized")
            return

        if not self.check8CharsAnd1Num(password):
            self.messagebox.showerror("Weak password",
                f"Password must have at least 8 char and have digits")
            return


        #Check if password match the confirm password
        if self.register_password_field.get() != self.register_confirm_field.get():
            self.messagebox.showerror("Confirm password doesn't match",
                f"Check again confirm password")
            return

        #Regex

        exist = self.connector.getUserByUname(username)
        if exist:
            self.messagebox.showerror("Username exists", "Please choose another username")
        else:
            self.connector.addUser(name, username, password)
            #Clear field
            self.register_name_field.set("")
            self.register_user_field.set("")
            self.register_password_field.set("")
            self.register_confirm_field.set("")
            self.temporaryLabel(self.frame2, "Register successfully",
                                x=220, y=420, fg="#0F0", second=1)

    def registerWithFace(self):
        """
        Register with face recognition. This requires the user finish the form
        otherwise, it won't allow the user to use this method.

        When the face is registered successfully, it will set the form to empty
        and add the "face_added" property to the user and send this user to
        the database.
        Params:
        -------
            None
        Return:
        -------
            None

        """
        username = self.register_user_field.get().strip()
        name     = self.register_name_field.get().strip()
        password = self.register_password_field.get().strip()

        if not self.checkNullFields(None, name = name, username = username, password = password):
            return

        if not self.checkCapitalizeName(name):
            self.messagebox.showerror("Enter a valid name",
                f"Name must have white space and capitalized")
            return

        if not self.check8CharsAnd1Num(password):
            self.messagebox.showerror("Weak password",
                f"Password must have at least 8 char and have digits")
            return

        #Check if password match the confirm password
        if self.register_password_field.get() != self.register_confirm_field.get():
            self.messagebox.showerror("Confirm password doesn't match",
                f"Check again confirm password")
            return

        #Can add some more check here such as regex

        #Checking if username exist
        exist = self.connector.getUserByUname(username)
        if exist:
            self.messagebox.showerror("Username exists", "Please choose another username")
        else:
            success = registerWithFace(self.store, name, username, self.detector, self.images_dir)
            # self.store["retrain_thread"].start()
            if success:
                self.connector.addUser(name, username, password, face_added=True)
                self.temporaryLabel(self.frame2, "Register successfully",
                                    x=220, y=420, fg="#0F0", second=1)
                self.register_name_field.set("")
                self.register_user_field.set("")
                self.register_password_field.set("")
                self.register_confirm_field.set("")
            else:
                self.temporaryLabel(self.frame2, "Cannot add facial recognition",
                                    x=220, y=420, fg="#F00", second=1)
