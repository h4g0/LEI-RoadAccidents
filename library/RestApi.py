from flask import Flask
from flask_restful import Resource,Api
##from tensorflow.keras.models import load_model
import json
import requests
##import cv2
import numpy as np

app = Flask("__accident_risk_api__")
api = Api(app)


def predict_risk_img(img,model):
  predictions = model.predict(np.array([im]))
  return np.argmax(predictions)

def acess_risk(img,accuracy="low"):
    
    global model1,model2

    danger = dict()
    if accuracy == low:
        danger["low accuracy"] =  int(predict_risk_img(img,model1) == 0)

    else:
        danger["low accuracy"] = int(predict_image(img,model1) == 0)
        if danger["low accuracy"] == 1:
            danger["high accuracy"]  = predict_image(img,model2)
        else:
            danger["high accuracy"] = danger["low accuracy"]

        danger["global"] = danger["low accuracy"] * danger["high accuracy"] 

    return danger
  

def getImageBing(latitude,longitude):
    key = "Aqk4d8d5q_eWvI3oGYPNI-NdIuS5fEt3U-AnDWxNAzyM2Dn_v2vn2BbgD_8F-jIh"
    link = f"https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/{latitude},{longitude}/19?mapSize=500,500&key={key}"
    file = name + ".png"
    buffer = requests.get(link).content
    img = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_UNCHANGED)
    
    return img

def preprocess_image(img):
    img = img[:475]
    img = cv2.resize(img,(128,128))
    img = img / 255

    return img

def get_image(latitude,longitude):
    img = getImageBing(latitude,longitude)
    img = preprocess_image(img)
    return img

def read_settings(f):
    with open(f) as fp:
        settings = json.load(fp)['settings']
    model1 = settings['model1']
    model2 = settings['model2']
    autoencoder = settings['autoencoder']
    cell_x = settings["cell_size_x"]
    cell_y = settings["cell_size_y"]

    model1 = load_model(model1)
    model2 = load_model(model2)
    autoencoder = load_model(autoencoder)

    return (model1,model2,autoencoder,cell_x,cell_y)

class PredictRisk(Resource):
    def get(self,latitude,longitude,accuracy):
        latitude = int(latitude)
        longitude = int(longitude)
        danger = {"high":10,"low":1}
        print(f"lat: {latitude},lon: {longitude},acc: {accuracy}")
        #getImageBing(latitude,longitude,key)
        return danger

api.add_resource(PredictRisk, '/risk_prediction_lat=<latitude>_lon=<longitude>_acc=<accuracy>')

if __name__ == "__main__":
    global key
    key = "Aqk4d8d5q_eWvI3oGYPNI-NdIuS5fEt3U-AnDWxNAzyM2Dn_v2vn2BbgD_8F-jIh"
    ##model1,model2,autoencoder,_,_ = read_settings("settings.json")
    app.run(debug=True)
