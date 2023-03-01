from tkinter.constants import FALSE
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys
import time
import datetime
import firebaseHelper
import csv


def initConnectFirebase():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    print("Connect Firebase Success")


def findStudentById(id):
    db = firestore.client()
    indexStudent = "Student" + str(id)
    print(indexStudent)
    doc_ref = db.collection(u'students').document(indexStudent)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        print(f'Can not find Student ID= ${indexStudent}')
        return False


def getDateAttendance(format):
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime(
        '%d' + format + '%m' + format + '%Y')
    return date


def getTimeAttendance(format):
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(
        ts).strftime('%H' + format + '%M' + format + '%S')
    return timeStamp


def attendanceStudent(studentId):
    db = firestore.client()
    findUser = False
    findUser = findStudentInLocal(studentId)
    if(not findUser):
        findUser = firebaseHelper.findStudentById(str(studentId))
    if(not findUser):
        return
    isAttendance = checkStudentAttendance(findUser["Class"], findUser["Id"])
    print(isAttendance)
    if(isAttendance == True):
        print("Student ID:" + findUser["Id"] + "was attendance")
        return

    docStudentID = 'Student' + str(studentId)
    time = getTimeAttendance(":")
    day = getDateAttendance("-")
    new_attendance_ref = db.collection(u'attendances').document(
        day).collection(findUser['Class']).document(docStudentID)
    if(not new_attendance_ref.get().exists):
        new_attendance_ref.set({
            u"day": day,
            u"time": time,
            u"classId": findUser["Class"],
            u"studentId": findUser["Id"]
        })
        row = [findUser["Class"], findUser["Id"], findUser["Name"], day, time]
        with open('StudentAttendance.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
    else:
        print("Student was attendance")


def checkStudentAttendance(ClassId, StudentId):
    Date = getDateAttendance("-")
    file = open("StudentAttendance.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    isAttendance = False
    for row in csvreader:
        if(len(row) == 0):
            return False
        if((row[0] == ClassId) and (str(row[1]) == str(StudentId)) and (str(row[3]) == str(Date))):
            isAttendance = True
            break
    return isAttendance


def findStudentInLocal(StudentId):
    file = open("students.csv")
    csvreader = csv.reader(file)
    student = False
    for row in csvreader:
        if((str(row[0]) == str(StudentId))):
            student = {
                u"Id": row[0],
                u"Name": row[1],
                u"Class": row[2],
            }
            break
    return student
