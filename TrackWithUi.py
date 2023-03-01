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


window = tk.Tk()
window.title("XUAN_DUNG-IT 2021")
window.configure(background='#151a30')
window.geometry('1280x670')
fontFamily = "SF Mono"
colorText = "#222b45"
bgInput = "#edf1f7"
lbl = tk.Label(window, text="Face Recognition Based Attendance System",
               bg=bgInput, fg=colorText, width=50, height=3, font=(fontFamily, 30, 'bold'))
lbl.place(x=100, y=30)

lbl1 = tk.Label(window, text="Student Attendance", width=30,
                bg=bgInput, fg=colorText, height=2, font=('times', 15, ' bold'))
lbl1.place(x=540, y=320)

message = tk.Label(window, text="", bg=bgInput, fg=colorText,
                   activeforeground="green", width=65, height=7, font=('times', 15, ' bold '))
message.place(x=400, y=400)

config = {
    "apiKey": "AIzaSyCLc3F9OSrgLZaQlZkKpHz_tY0kfQNO4I0",
    "authDomain": "fir-face-detect-9cd16.firebaseapp.com",
    "databaseURL": "https://fir-face-detect-9cd16-default-rtdb.firebaseio.com",
    "projectId": "fir-face-detect-9cd16",
    "storageBucket": "fir-face-detect-9cd16.appspot.com",
    "messagingSenderId": "328022831177",
    "appId": "1:328022831177:web:425a2789ca02c51a590f98",
    "measurementId": "G-8RB4QYNMNP"
}

firebase = firebase.FirebaseApplication(
    "https://fir-face-detect-9cd16-default-rtdb.firebaseio.com", None)
blob = Blob.from_string("gs://fir-face-detect-9cd16.appspot.com")
def trackImages(type = ""):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("./DataSet/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("students.csv")

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    findId = False
    date = False
    timeStamp = False
    nameStudent = False
    while True:
        ret, im = cam.read()
        im = cv2.flip(im, 1)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        cv2.imshow('Face Recognizing', im)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            print(Id)
            print(conf)
            isOKE = 45
            if(type == "Auto"):
                isOKE = 25
            if(conf < isOKE):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                nameStudent = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id)+"-"+nameStudent
                attendance.loc[len(attendance)] = [Id, nameStudent, date, timeStamp]
                findId = str(Id)
                if(type == "Auto"):
                    firebaseHelper.attendanceStudent(Id)

            else:
                Id2 = 'Unknown'
                tt = str(Id2)
            # if(conf > 75):
                # noOfFile = len(os.listdir("UnknownImages"))+1
                # cv2.imwrite("./UnknownImages/Image" +
                #             str(noOfFile) + ".jpg", im[y:y+h, x:x+w])
            cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')

        cv2.imshow('Face Recognizing', im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.release()
            cv2.destroyAllWindows()
            break

    res = "Student Code: " + findId + " | " + "Name: " + nameStudent + " | " + "Date: " + date + " | " + "Time: " + timeStamp
    message.configure(text=res)
    firebaseHelper.attendanceStudent(Id)

def trackImagesAuto():
    trackImages("Auto")


trackImg = tk.Button(window, text="Track Image", command=trackImages, fg="black", bg="white",
                     width=20, height=3, activebackground="Yellow", font=('times', 15, ' bold '))
trackImg.place(x=200, y=200)

trackImgAuto = tk.Button(window, text="Track Image Auto", command=trackImagesAuto, fg="black", bg="white", width=20, height=3, activebackground="Yellow", font=('times', 15, ' bold '))
trackImgAuto.place(x=440, y=200)

quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg="black",
                       bg="white", width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
quitWindow.place(x=700, y=200)

lbl3 = tk.Label(window, text="DESIGN BY KGCE BE-IT BATCH 2020, GROUP NO : 10",
                width=80, fg="white", bg="black", font=('times', 15, ' bold'))
lbl3.place(x=200, y=620)

window.mainloop()
