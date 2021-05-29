import hashlib

################################################################################
# Class:          User
# Author:         Duc Anh
# Last modified:  29 May 2021

################################################################################

class User:
    '''
    This class is used mainly to create the hash face and the hash password of
    the user when this user is created. So that, I don't need to work with
    with the hash lib for most of the time.

    Attributes:
    ----------
    name : str
        The name of the user
    username : str
        Then username of the user
    password: str
        The password of the user
    face_added : bool
        Set to True means that the person has registerd face
    hash_pass : str
        The hash for the password
    hash_face : str
        The hash for the user name and the name

    Methods:
    --------
    toDict()
        Represent all attributes of this user as a dictionary.

    Getters and setters:
    setHashFace(username, password)
        The the new hash face
    getHashPass()
        Get the hash password from this user
    getHashFace()
        Get the hash face from this user


    '''
    def __init__(self, name, username, password, face_added):
        """
        This method sets up the basic information of the user. It will
        create the hash_face and hash_pass for this user base on the
        password, username and name

        Params:
        -------
            name : str
                The name of the user
            username : str
                Then username of the user
            password: str
                The password of the user
            face_added : bool
                Set to True means that the person has registerd face

        Return:
        -------
            None
        """
        self.__name       = name
        self.__username   = username
        self.__password   = password
        self.__face_added = face_added

        # Convert username to bytes before hashing
        #https://stackoverflow.com/questions/33054527/typeerror-a-bytes-like-object-is-required-not-str-when-writing-to-a-file-in
        self.__hash_pass  = hashlib.sha256(password.encode()).hexdigest()

        #This hash is used for login with face. The name will be predicted from
        #the recognition
        #Combine username + name, will be combined with object id in database
        bytes_username    = (username.lower() + name.lower()).encode()
        self.__hash_face  = hashlib.sha256(bytes_username).hexdigest()

    def toDict(self):
        """
            This will return the private variable without the double underscore
            of python. This can be used to make update to the database.

            Params:
            ------
                None

            Returns:
            --------
                dict
                    Return the dictionary representing this user.
        """
        dict_ = {
            "name"      : self.__name,
            "username"  : self.__username,
            "face_added": self.__face_added,
            "hash_pass" : self.__hash_pass,
            "hash_face" : self.__hash_face,
        }

        return dict_

    #Some useful getters and setters of this class =============================
    def setHashFace(self, hash_face):
        self.__hash_face = hash_face

    def getHashPass(self):
        return self.__hash_pass

    def getHashFace(self):
        return self.__hash_face
