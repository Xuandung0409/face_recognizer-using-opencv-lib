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
import student
import classFirebase


def checkImage(path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("./DataSet/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("students.csv")
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    im = cv2.imread(path)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    print("I found {} face(s)".format(len(faces)))

    for(x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
        Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
        isOKE = 35
        print(conf) 
        print(Id)
        if(conf < isOKE):
            firebaseHelper.attendanceStudent(Id)
            return "SUCCESS"

        return "FALSE"

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

