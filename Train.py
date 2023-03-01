# import plaidml.keras
# plaidml.keras.install_backend()
# os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import os
import firebaseHelper
import tkinter.font as font
from PIL import Image, ImageTk
import numpy as np
import csv
import tkinter as tk
from tkinter import Message, Text
import cv2
firebaseHelper.initConnectFirebase()

im = cv2.imread("./SampleImages/img1.png", 1)

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

lbl1 = tk.Label(window, text="Student Code:", width=11, height=2,
                fg=colorText, bg=bgInput, font=(fontFamily, 15, ' bold '))
lbl1.place(x=100, y=200)

txt1 = tk.Text(window, width=30, bg=bgInput, height=1, bd="0",
               fg=colorText, font=(fontFamily, 15, ' bold '), insertwidth="0", padx="15", selectborderwidth="0", highlightthickness="0", pady="12", insertbackground="red", selectbackground="#7E8089")
txt1.place(x=250, y=200)

lbl2 = tk.Label(window, text="Student Name:", width=11, height=2,
                fg=colorText, bg=bgInput, font=(fontFamily, 15, ' bold '))
lbl2.place(x=100, y=270)

txt2 = tk.Text(window, width=30, bg=bgInput, height=1, bd="0",
               fg=colorText, font=(fontFamily, 15, ' bold '), insertwidth="0", padx="15", selectborderwidth="0", highlightthickness="0", pady="12", state="disabled")
txt2.place(x=250, y=270)

lbl3 = tk.Label(window, text="Message →", width=15, fg=colorText,
                bg="white", height=4, font=(fontFamily, 15, ' bold '))
lbl3.place(x=100, y=340)

message = tk.Label(window, text="", bg="white", fg=colorText,
                   width=100, height=4, font=(fontFamily, 15, ' bold '))
message.place(x=250, y=340)


def clearId():
    txt1.delete(0, 'end')


def clearName():
    txt2.delete(0, 'end')


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        pass


def takeImages():
    Id = (txt1.get("1.0", "end-1c"))
    if(not Id):
        res = "Please Input Student Code"
        message.configure(text=res)
    else:
        if(isNumber(Id)):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            findUser = firebaseHelper.findStudentById(str(Id))
            print("Start search user")
            print(findUser)
            message.configure(text="")
            if(findUser == False):
                res = "Student not exists"
                message.configure(text=res)
            else:
                res = "Student Infomation: " + "ID: " + findUser['Id'] + " | Name: " + findUser['Name'] + " | Class: " + findUser['Class']
                message.configure(text=res)
                name = findUser['Name']
                while(True):
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, 1.15, 6)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        sampleNum = sampleNum+1
                        cv2.imwrite("./SampleImages/ "+name + "."+Id + '.' +
                                    str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                        cv2.imshow('Face Detecting', img)
                    if cv2.waitKey(100) & 0xFF == ord('q'):
                        break
                    elif sampleNum > 80:
                        break
                cam.release()
                cv2.destroyAllWindows()
                res = "Images Saved for Student Code: " + Id + " Name : " + name
                row = [Id, name]
                with open('StudentRecord.csv', 'a+') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                csvFile.close()
                message.configure(text=res)
        else:
            if(Id.isalpha()):
                res = "Enter Numeric Id"
                message.configure(text=res)


def trainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("SampleImages")
    recognizer.train(faces, np.array(Id))
    recognizer.save("./DataSet/Trainner.yml")
    res = "Image Trained"
    message.configure(text=res)
    # removeImageAfterTrain("SampleImages")


def getImagesAndLabels(path):
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    Ids = []
    for imagePath in imagePaths:
        print(imagePath)
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces=detector.detectMultiScale(imageNp)
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)

    return faceSamples, Ids


def removeImageAfterTrain(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    for imagePath in imagePaths:
        os.remove(imagePath)


takeImg = tk.Button(window, text="Take Images", command=takeImages, fg=colorText, bg="white",
                    width=20, height=3, activebackground="Green", font=(fontFamily, 15, ' bold '))
takeImg.place(x=200, y=500)

trainImg = tk.Button(window, text="Train Images", command=trainImages, fg=colorText,
                     bg="white", width=20, height=3, activebackground="Green", font=(fontFamily, 15, ' bold '))
trainImg.place(x=500, y=500)

quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg=colorText,
                       bg="white", width=20, height=3, activebackground="Red", font=(fontFamily, 15, ' bold '))
quitWindow.place(x=800, y=500)

lbl4 = tk.Label(window, text="Senior Project",
                width=80, fg=colorText, bg="black", font=(fontFamily, 15, ' bold'))
lbl4.place(x=200, y=620)

window.mainloop()
