"""
Configure files for the application. We can set the name for the local directory,
the models, or the data files here. Please keep the same file format,
DEFAULT_IMGS_DIR and the detector configuration. You can change the mongo
url with your own credentials and change the name of the mongo connector
database and collection with your choice. It should match with whatever you
create in your database.

    Ex:
        Create database "DB" and collection "COLLECTION":
        You should change MongoConnector.py to this:
            self.client     = pymongo.MongoClient(cfg.mongo["MONGO_URL"])
            self.db         = self.client.DB
            self.collection = self.db.COLLECTION

"""

local = {
    "BASE_DB" : "my_local_db",
    "IMG_DIR" : "images",
    "DEFAULT_IMGS_DIR"  : "default_faces", #Keep this one, it's default
    "MAP_DIR2NAME_FILE" : "mapping.json", #Must have json
}

data  = {
    #Must be .csv file
    "X_NAME" : "features.csv",
    "y_NAME" : "labels.csv"
}

models = {
    #Must be .pkl file
    "LE_NAME"    : "my_labelEncoder.pkl",
    "MODEL_NAME" : "SVC.pkl",
    "PCA_NAME"   : "pca.pkl",
}


detector = {
    "PATH"    : "face_detector",
    "PROTO"   : "deploy.prototxt",
    "WEIGHTS" : "res10_300x300_ssd_iter_140000.caffemodel"
}

mongo = {
    "MONGO_URL" : "mongodb+srv://user1:b8E7bGCO0BG7Nkay@cluster0.uqkx9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
}
