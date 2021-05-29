from Base import Base
from tkinter import ttk
import json
import requests
import tkinter as tk
import tkinter.font as font
from predict_face import registerWithFace

################################################################################
# Class:          Screen3
# Author:         Duc Anh
# Last modified:  29 May 2021

################################################################################

class Screen3(Base):
    '''
    This class is for the screen 3. It will split the page to 2 frames. The
    frame 1 works like a side bar, which can change the frame 2 depends on the
    button. The first version of frame 2 or the main page will say hello to the
    current user and display a random fact. The second page or the 2nd version
    of the frame 2 is about changing password. The third one allow the user
    to add again face recognition if that user haven't added.

    Attributes:
    ----------
    frame1 : tkinter frame
        The container for the left page
    frame2 : tkinter frame
        The container for the right page
    separator: tkk Separator
        The vertical line that divide the screen into 2 parts
    ======================Main page's attributes ===============================
    main_page_btn : tk Button
        The button to go to the main page
    change_pass_btn : tk Button
        The button to go to to the change pass page
    add_face_page_btn : tk Button
        The button to go to to the change name page
    logout_btn : tk Button
        Button that will logout the current user and go back to screen 1
    welcomeLab : tk Label
        The label for the big Welcome word with the name of the user
    randomFactLab : tk Label
        The random fact label
    =====================Change pass page's attributes =========================
    change_frame_lab : tkinter Label
        The label for the big word Change pass word
    change_current_label : tkinter Label
        The lable for the current password field
    change_current_field : tkinter Stringvar
        The field for the current password field
    change_current_entry : tkinter Entry
        The container for the current password field
    change_new_label : tkinter Label
        The lable for the new password field
    change_new_field : tkinter Stringvar
        The field for the new password
    change_new_entry : tkinter Entry
        The container for the new password field
    change_confirm_label : tkinter Label
        The lable for the confirm password field
    change_confirm_field : tkinter Stringvar
        The field for the confirm password
    change_confirm_entry : tkinter Entry
        The container for the confirm password field
    submit_btn : tk Button
        The button for submit new password
    =========================Add face page's attributes ========================
    frame2_label : tkinter Label
        The label for the big Login with the add face recognition word
    open_cam_btn : tkinter Button
        The button for opening camera to start login with face

    '''
    def __init__(self, parent, store):
        """
        Init the screen 3 and display the main page. It took about 1 second
        to fetch the data from the server so that the main page button have
        to wait for a bit. The screen is divided to 1 column for side bar
        and 5 columns for other frames.

        Initially it will set the main page button to be disabled because the
        screen 3 appears with the main page

        Params:
        -------
            parent: tkinter frame or tk()
                The parent frame attach to this base
            store: dict
                The storage for some data from current user or the mongo
                connector

        """
        super().__init__(parent, store)
        #Screen 3 has 3 state: main, pass, name
        self.main_page_btn   = tk.Button(self.frame1, borderwidth=0.5, anchor="w",
            text="Get Random Fact", command = self.mainPage)

        self.change_pass_btn = tk.Button(self.frame1, borderwidth=0.5, anchor="w",
            text="Change password", command = self.changePassPage)

        self.add_face_page_btn = tk.Button(self.frame1, borderwidth=0.5, anchor="w",
            text="Add face recognition", command = self.addFacePage)

        self.logout_btn      = tk.Button(self.frame1, borderwidth=0.5, anchor="w",
            text="Logout", command = self.logout)

        self.welcomeLab      = tk.Label(self.frame2,
            text=f"Welcome, {self.store['name']}!", font=("Arial", 20, "bold"))

        self.randomFactLab   = tk.Label(self.frame2,
            text=f'{self.getRandomFact()}', font=("Courier", 12), wraplength=800,
            justify="center")

        #Set font: https://pythonexamples.org/python-tkinter-button-change-font/#:~:text=You%20can%20also%20change%20font,font%20size%20of%20tkinter%20button.&text=Font%20size%20of%20the%20button%20is%2030.
        buttonFont = font.Font(size=10, weight="bold")
        self.main_page_btn['font']   = buttonFont
        self.change_pass_btn['font'] = buttonFont
        self.add_face_page_btn['font'] = buttonFont
        self.logout_btn ['font']     = buttonFont

        #Config row and col for parent, frame1, and frame2 =====================
        #Num rows and num cols: Ex: 1, 4 means 1 row and 4 cols for the big grid
        self.configureWidgetGrid(self.parent, 1, 6) #side bar 1 and the main screen 3 row span
        self.configureWidgetGrid(self.frame1, 5000, 1) #Set to 5000 making things closer
        self.configureWidgetGrid(self.frame2, 5, 1) #Havent register, (name, user, pass), (2 buttons)
        #Place components on containers ========================================
        #Adding things on frame 1
        self.separator.grid(column=0, row=0, sticky='nse')
        self.frame1.grid(row = 0, column = 0, columnspan=1, rowspan=1000, sticky="nsew")
        self.frame2.grid(row = 0, column = 1, columnspan=5, rowspan=1, sticky="nsew")
        self.main_page_btn.grid(  row = 800, column = 0, sticky="we", ipadx = 50)
        self.change_pass_btn.grid(row = 801, column = 0, sticky="we", ipadx = 50)
        self.add_face_page_btn.grid(row = 802, column = 0, sticky="we", ipadx = 50)
        self.logout_btn.grid(row = 900, column = 0)
        #Adding INITIAl things on frame 2
        self.welcomeLab.grid(row = 0, column = 0, rowspan = 2)
        self.randomFactLab.grid(row = 1, column = 0, rowspan = 3)
        #Initialy set the main page to disable
        self.store["current_page"]  = "main"
        self.main_page_btn["state"] = "disabled"

    def mainPage(self):
        """
        Create the main page for the frame 2. This will set the button to the
        main page disabled. Also it will fetch a random text from the random
        useless thing api.

        It also continue to retrain the data when the main page is reached
        Params:
        -------
            None

        Return:
        -------
            None

        """
        self.store["current_page"] = "main"
        self.disableButtonOfCurrentPage()
        self.removeFrame(self.frame2)
        self.frame2          = tk.Frame(self.parent, bd = 1)
        #Create again attribute
        self.welcomeLab      = tk.Label(self.frame2,
            text=f"Welcome, {self.store['name']}!", font=("Arial", 20, "bold"))

        self.randomFactLab   = tk.Label(self.frame2,
            text=f'{self.getRandomFact()}', font=("Courier", 12), wraplength=800,
            justify="center")

        #Configure again frame
        self.configureWidgetGrid(self.frame2, 5, 1)

        #Place thing on frame
        self.frame2.grid(row = 0, column = 1, columnspan=5, rowspan=1, sticky="nsew")
        self.welcomeLab.grid(row = 0, column = 0, rowspan = 2)
        self.randomFactLab.grid(row = 1, column = 0, rowspan = 3)

    def changePassPage(self):
        """
        Create the change pass page for the frame 2. This will set the button to
        the pass page disabled and prompting user for the new password to change

        Params:
        -------
            None

        Return:
        -------
            None

        """
        self.store["current_page"] = "pass"
        self.disableButtonOfCurrentPage()
        self.removeFrame(self.frame2)
        self.frame2               = tk.Frame(self.parent, bd = 1)

        self.change_frame_lab     = tk.Label(self.frame2, text="Change password", font=("Arial", 20, "bold"))

        self.change_current_label = tk.Label(self.frame2, text="Current password: ")
        self.change_current_field = tk.StringVar()
        self.change_current_entry = tk.Entry(self.frame2, textvariable=self.change_current_field, show='*')

        self.change_new_label     = tk.Label(self.frame2, text="New password: ")
        self.change_new_field     = tk.StringVar()
        self.change_new_entry     = tk.Entry(self.frame2, textvariable=self.change_new_field, show='*')

        self.change_confirm_label = tk.Label(self.frame2, text="Confirm password: ")
        self.change_confirm_field = tk.StringVar()
        self.change_confirm_entry = tk.Entry(self.frame2, textvariable=self.change_confirm_field, show='*')

        self.submit_btn = tk.Button(self.frame2, text="Submit", width=10,
                            height=2, command = self.submitNewPass)

        #Configure again frame
        self.configureWidgetGrid(self.frame2, 9, 2)

        #Place components on containers ========================================
        self.frame2.grid(row = 0, column = 1, columnspan=5, rowspan=1, sticky="nsew")
        self.change_frame_lab.grid(column = 0, row = 0, rowspan=2, columnspan=2)
        self.change_current_label.grid(column = 0, row = 2)
        self.change_current_entry.grid(column = 1, row = 2, sticky="w")
        self.change_new_label.grid(column = 0, row = 3)
        self.change_new_entry.grid(column = 1, row = 3, sticky="w")
        self.change_confirm_label.grid(column = 0, row = 4)
        self.change_confirm_entry.grid(column = 1, row = 4, sticky="w")

        self.submit_btn.grid(column = 0, row = 6, columnspan=2)

    def addFacePage(self):
        """
        Create the add face page for the frame 2. This will set the button to
        the add face page disabled.

        Params:
        -------
            None

        Return:
        -------
            None

        """
        self.store["current_page"] = "face"
        self.disableButtonOfCurrentPage()
        self.removeFrame(self.frame2)
        self.frame2        = tk.Frame(self.parent, bd = 1)

        self.frame2_label  = tk.Label(self.frame2,
                                font=("Arial", 20, "bold"),
                                text="Add face recognition")

        self.open_cam_btn  = tk.Button(self.frame2,
                                text="Open camera",
                                relief = tk.SUNKEN if self.store["face_added"] else tk.RAISED,
                                state = "normal" if self.store["has_cam"] else "disabled",
                                command = self.addFaceRecognition)

        #Configure again frame
        self.configureWidgetGrid(self.frame2, 3, 1)

        #Place components on containers ========================================
        self.frame2.grid(row = 0, column = 1, columnspan=5, rowspan=1, sticky="nsew")
        self.frame2_label.grid(column=0, row=0, columnspan=3, rowspan=1)
        self.open_cam_btn.grid(column=0, row=1, sticky='s')

        """""
        Change name has to be updated localy by finding the map
        This one should be easy, @localhost, -> open file -> update key ->
        write file again -> end
        """
        pass

    def addFaceRecognition(self):
        """
        This will call the method register with face again to save the user
        face to the local images directory.

        Params:
        -------
            None

        Return:
        -------
            None

        """
        if self.store["face_added"]:
            self.temporaryLabel(self.frame2, "Already added face",
                                x=350, y=250, fg="#F00", second=1)
            return
        name, username = self.store["name"], self.store["username"]
        success = registerWithFace(self.store, name, username, self.detector, self.images_dir)
        # self.store["retrain_thread"].start()
        if success:
            self.connector.setTrueFaceAddedByUname(username)
            self.temporaryLabel(self.frame2, "Face recognition has been added",
                                x=300, y=420, fg="#0F0", second=1)
        else:
            self.temporaryLabel(self.frame2, "Cannot add facial recognition",
                                x=300, y=420, fg="#F00", second=1)

    def submitNewPass(self):
        """
        This method will check and submit the new password of the user to the
        database sever. Some basic form validation is performed during the
        process.

        Params:
        -------
            None

        Return:
        -------
            None

        """
        current  = self.change_current_field.get()
        new      = self.change_new_field.get()
        confirm  = self.change_confirm_field.get()

        #Create warning with current Pass, new Pass and confirm Pass
        func = lambda label : f"{label.capitalize()} password"
        if not self.checkNullFields(func, current = current, new = new, confirm = confirm):
            return

        if not self.check8CharsAnd1Num(new):
            self.messagebox.showerror("Weak password",
                f"Password must have at least 8 char and have digits")
            return

        if self.change_new_field.get() != self.change_confirm_field.get():
            self.messagebox.showerror("Confirm password doesn't match",
                f"Check again confirm password")
            return

        ##Check here, make sure the hash changed correctly
        result = self.connector.changePassword(self.store, current, new)

        if result:
            self.temporaryLabel(self.frame2, "Password updated successfully",
                                x=250, y=420, fg="#0F0", second=1)
        else:
            self.temporaryLabel(self.frame2, "Old password doesn't match",
                                x=275, y=420, fg="#F00", second=1)

    def logout(self):
        """
        Remove the current user information from the store except the name, so
        that when go back to screen 1, the username is saved in the username
        field.

        Params:
        -------
            None

        Return:
        -------
            None

        """
        #Pop things out of the store if that belongs to the user
        self.store.pop("_id")
        self.store.pop("name")
        self.store.pop("face_added")
        self.store.pop("hash_face")
        self.store.pop("current_page")
        self.clearScreen()

        #Reconfgiure parent grid
        from screen1 import Screen1
        Screen1(self.parent, self.store)

    def getRandomFact(self):
        """
        Makes a request to the https://uselessfacts.jsph.pl api to get a
        random fact to make the app more interesting.

        Params:
        -------
            None

        Return:
        -------
            str
                The random useless fact from the api

        """
        #The api I used in this application https://uselessfacts.jsph.pl/
        url      = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)
        dict_    = json.loads(response.text)
        fact     = dict_["text"]

        return fact

    def disableButtonOfCurrentPage(self):
        """
        This methods help disable the button of the current page. For example,
        if the user is at the main page, the user cannot click on the main
        page butotn again because it's disabled. This prevents the user calling
        api too many times.

        Params:
        -------
            None

        Return:
        -------
            None
        """
        labels  = ["main", "pass", "face"]
        buttons = [self.main_page_btn, self.change_pass_btn, self.add_face_page_btn]
        map     = {labels[i] : buttons[i] for i in range(len(labels))}

        #Loop through the label, if the label mathces the current page, then the
        #button for that label will be set to disable
        for label in labels:
            button = map[label]
            if label == self.store["current_page"]:
                button["state"] = "disable"
            else:
                button["state"] = "active"
