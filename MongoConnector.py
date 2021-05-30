import pymongo
from pymongo import MongoClient
from User import User
import hashlib
import config as cfg
#Use object id
#https://stackoverflow.com/questions/16073865/search-by-objectid-in-mongodb-with-pymongo
from bson.objectid import ObjectId
#Customizing destructuring object
#https://stackoverflow.com/questions/54785148/destructuring-dicts-and-objects-in-python
from operator import itemgetter

################################################################################
# Class:          MongoConnector
# Author:         Duc Anh
# Last modified:  29 May 2021

################################################################################

class MongoConnector:
    """
    This class is the connector between the app and the mongo db database. It
    performs basic CRUD operation to the database to add information about users

    This data base is set up by the credientials:
    username: conaf67136@o3live.com
    password: 3gGz;p@@3sjSm26

    Can access the database via
    user1 --> <user>
    b8E7bGCO0BG7Nkay --> <password>

    Use the link below to connect to the database
    mongodb+srv://<user>:<password>@cluster0.uqkx9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority

    Attributes:
        client : pymongo.mongo_client.MongoClient
            The client that communicate with the database
        db : pymongo.database.Database
            The DCS211 database that the client has access to
        collection : pymongo.collection.Collection
            The collection "users"

    Methods:
        addUser(name, username, password, face_added=False)
            Add user to the database
        getUserByUname(username)
            Search for the username and return the person if exists
        updateUser(username, new_user)
            Update the user of the database
        getAllUsers()
            Get all user from the database
        deleteUserById(id)
            Find and delete the user with the given id
        loginWithPass(username, password)
            login with normall password
        closeConnection()
            close the current client

    """
    def __init__(self):
        """
        Init the client, db and collection attributes of this class

        Params:
        -------
            None

        """
        self.client     = pymongo.MongoClient(cfg.mongo["MONGO_URL"])
        self.db         = self.client.DCS211
        self.collection = self.db.users

    def getAllUsers(self):
        """
        Return a list of all user from the usesrs collection

        Params:
        -------
            None

        Return:
        ------
            A list of users

        """
        result   = self.collection.find({})
        return list(result)

    def addUser(self, name, username, password, face_added=False):
        """
        Add the user to the database. If the face_added is not set, it will be
        False

        Params:
        -------
            name : str
                The user's name
            username: str
                The user's username
            password: str
                The user's password
            face_added: bool
                If true, it means the user has face added. The default is set
                to false

        Return:
        ------
            None

        """
        #https://stackoverflow.com/questions/61517/python-dictionary-from-an-objects-fields
        user = User(name, username, password, face_added)

        result = self.collection.insert_one(user.toDict())

        if result:
            #Get the object id again to hash this twice and set the hash face again
            object_id = str(self.collection.find_one({"username" : username})['_id'])
            #Combine previous hash with the id from database
            new_random_string = user.getHashFace() + object_id
            new_hash_face     = hashlib.sha256(new_random_string.encode()).hexdigest()
            user.setHashFace(new_hash_face)

            query   = {"_id" : ObjectId(object_id)}
            update  = {"$set" : user.toDict()}
            self.collection.find_one_and_update(query, update)

            print("Success")

    def getUserByUname(self, username):
        """
        Find the user base on username

        Params:
        -------
            username: str
                User name of the person

        Return:
        ------
            None

        """
        result   = self.collection.find_one({"username" : username})
        return result

    def updateUser(self, query, **kwargs):
        """
        Update the user by the given info. The attribute of the user can be
        passed as attribute = new_values in the function. This is handy for
        changing little information without the need to write {$set: {}}

        Params:
        -------
            query: dict
                The information for finding the user
            kwargs : dict
                a dict containing attribute : new_values of this user.
                The user will be updated with new_attribute

        Return:
        ------
            dict
                The user before the update

        """
        #query should be a dict
        update = {"$set" : kwargs}
        result = self.collection.find_one_and_update(query, update)

        if result:
            print("Updated successfully")
        else:
            print("Update failed")
        return result

    def deleteUser(self, query):
        """
        Find and delete the user by the given query dictionary

        Params:
        -------
            query : dict
                Information to find this user

        Return:
        ------
            dict
                The dictionary of this user

        """
        result = self.collection.find_one_and_delete(query)

        return result

    def changePassword(self, store, password, new_password):
        """
        This methods is design specifically for the change password function
        in screen 3. It first try to login with the old password, then check
        if the new and the confirm password matches before updating it to the
        database.

        Params:
        -------
            store : dict
                The global storage of all screeen
            password : str
                The current password of the user
            new_password : str
                The new password of the user

        Return:
        ------
            bool
                Return true if the password is updated successfully

        """
        isValidOldPass = self.loginWithPass(store["username"], password)

        if isValidOldPass:
            #Create new user so that, I don't need to rehash the password and face_hash
            new_user = User(store["name"], store["username"], new_password, store["face_added"])
            new_hash_pass = new_user.getHashPass()
            self.updateUser({"_id" : store["_id"]}, hash_pass = new_hash_pass)
            print("Updated successfully")
            return True
        else:
            print("Password is not valid")
            return False

    def loginWithPass(self, username, password):
        """
        Login with normal pass. It will convert the password to sha256 hash
        from hashlib and compare that with the hash_pash of the user

        Params:
        -------
            username: str
                User name of the person
            password : str
                The given password to check

        Return:
        ------
            bool
                Return true if login successfully

        """
        #Check if this username exists
        user_doc = self.getUserByUname(username)
        if user_doc:
            hash_pass       = itemgetter("hash_pass")(user_doc)
            hash_from_user  = hashlib.sha256(password.encode()).hexdigest()

            #Compare the 2 hash
            if hash_pass == hash_from_user:
                return True
            else:
                print("Wrong password")
        else:
            print("Current user does not exist")
            return False

    def setTrueFaceAddedByUname(self, username):
        """
        This method set the face recognition to true when the user add it in
        screen 3.

        Params:
        -------
            username : str
                The username that will be used to find the document in the
                database

        Return:
        ------
            dict
                Return the previous version of the document
        """
        query  = {"username" : username}
        update = {"$set" : {"face_added" : True}}
        result = self.collection.find_one_and_update(query, update)
        return result

    def closeConnection(self):
        """
        Close the dabase connection

        Params:
        -------
            None

        Return:
        ------
            None

        """
        self.client.close()
