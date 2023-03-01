from tkinter.constants import TRUE
import tornado.web
import tornado.ioloop
import json
from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from firebase import firebase
from google.cloud.storage.blob import Blob
from google.cloud import storage
import pyrebase
import tkinter.font as font
import time
import datetime
import pandas as pd
import csv
import os
import cv2
from tkinter import Message, Text
import tkinter as tk
import firebaseHelper
firebaseHelper.initConnectFirebase()
# import student
# import classFirebase
fontscale = 0.5
fontcolor = (0,0,255)

def checkImage(path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("./DataSet/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("students.csv")
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    font = cv2.FONT_HERSHEY_SIMPLEX
    im = cv2.imread(path)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.15, 5)
    print("I found {} face(s)".format(len(faces)))

    for(x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
        Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
        
        print(conf)
        print(Id)
        if(conf <=30):
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            aa=df.loc[df['Id'] == Id]['Name'].values
            tt= "ID: " + str(Id)
            nameStudent =  "Name: " + aa 
            confused = "Conf:" + str(conf)
            cv2.putText(im, str(tt),(x,y+h), font, fontscale, fontcolor ,1)
            cv2.putText(im, str(nameStudent),(x,y+h+20), font, fontscale, fontcolor ,1)
            cv2.putText(im, str(confused),(x,y+h+40), font, fontscale, fontcolor ,1)
            
            imS = cv2.resize(im, (400, 400))                    # Resize image
            cv2.imshow("output", imS)  
            if cv2.waitKey(1)==ord('q'):
                break
        
        
       
        # if(conf < isOKE):
        #     firebaseHelper.attendanceStudent(Id)
        #     return "SUCCESS"

        # return "FALSE"


checkImage('./SampleImages/aambrosio.19.0.jpg')

class uploadImgHandler(tornado.web.RequestHandler):
    def post(self):
        files = self.request.files["fileImage"]
        for f in files:
            fh = open(f"upload/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
        isSuccess = checkImage(f"upload/{f.filename}")
        self.write(str(isSuccess))
    def get(self):
        self.render("index.html")

if (__name__ == "__main__"):
    app = tornado.web.Application([
        ("/", uploadImgHandler),
        ("/img/(.*)", tornado.web.StaticFileHandler, {'path': 'upload'})
    ])

    app.listen(8080)
    print("Listening on port 8080")
    tornado.ioloop.IOLoop.instance().start()

