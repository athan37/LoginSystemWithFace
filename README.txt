Project teammates (list all):
-----------------------------
N/A

Project description & goals:
-----------------------------
This project is about using opencv and eigenface (basically it's PCA)
to recognize human faces. I also improve it to make a login system with 
the ability to register and detect face. Besides, it allows user to login 
normally using user name and password. In the end, it also use fetch the 
random useless fact api to make it more interesting.

Project goals:
- Explore how face detection works
- Show ability to perform basic login form validation
- Use of python tkinter GUI
- Utilize python libraries
- Demonstrate the ability to use basic OOP to make applications
- Use of external database such as MongoDB
- Utilize python function patterns
- Basic state management of the application

Project inputs & expected outputs:
----------------------------------
Similar to other login system, the program requires:
For registration:
Inputs:
- Name : Capitalize first character, each word have to have white space in between
- Username: Anything
- Password : Need to be at least 8 characters and at least 1 digit
- Confirm password : Have to match the password
- Short video of the person face (you can add this later after login normally)
Outputs: (when the user login)
- It will show registration successfully if the information is entered correctly
- The data is saved in the database
- Else it will show the error
- The face recognition may took 1-3 mins to register, so please wait for it

For login:
Inputs:
- Username (first screen)
- Password (Second screen) or Face Video
Outputs:
- If login successfully, it will automatically change to the screen 3
- Else, it will show message such as wrong password or cannot login with face
- The screen 3 should prints Welcome to the user by calling the name
- It should show a random fact

For changing password:
Inputs:
- Current password : has to match the current password from the server  
- New password     : needs to be at least 8 characters and at least 1 digit
- Confirm password : must match the new password
Outputs:
- It will show the message updated successfully if it's successful
- Otherwise, it will show error message that the current pass is wrong

For add face after login:
Inputs:
- A short video of the user: face straight, keep the same distance
Outputs:
- It will say updated successfully, and the user might need to wait for 1-3 mins 
to train the model again

For logout button:
Input:
A click from user 
Output:
It will return to the screen 1
The previous username is kept in the username field

For back button
Input:
A click from user 

Output:
It will return to the screen 1
The previous username is kept in the username field


Instructions for installing required libraries:
Basically, this app only need libraries inside pip
-----------------------------------------------
These libraries can be installed via pip install --user [library name]:
tkinter
pymongo
pymongo[srv]
numpy
opencv-python
sklearn
scikit-image
requests


Instructions for executing the project:
---------------------------------------
The face_detector directory contains 2 important files for face detection which
come from opencv dnn module. The app will load 2 files from that directory to
create a detector object.

This app needs a good internet connection otherwise something weird will happen
during the register process. 

The new_faces directory will always have some images there, about 250. That 
directory is used to help the model to have enough data to train. All of that 
data comes from the caltech dataset: http://www.vision.caltech.edu/Image_Datasets/faces/.

If you want to login with face, please make sure to keep the distance 
to the screen similar to when you register. The detection is vunerable to 
that change and the tilted face. 

In the shell, execute the app file (the main class of this application):
$python app.py

If the app tooks too long to response (10-20 second freeze) except for face registration, 
it might be due to the database server, either it is down or the access from new ip is not
allowed. Please wait to the next day or email athan@bates.edu.

Notes: Please don't modify the local_db directory or the new_face directory
manually. It may produce some mismatch between the server and the local face 
database.

Link to Zoom cloud recording of narrated execution:
---------------------------------------------------
I used drive to upload my recording
https://drive.google.com/file/d/1zruF5jxIcc_j90fzBckIrUxymbxDJrlt/view?usp=sharing