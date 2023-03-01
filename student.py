import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import firebaseHelper


def createStudent():
    db = firestore.client()

    file = open("students.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)

    index = 0
    for row in rows:
        index += 1
        indexStudent = "Student" + str(index)
        student = firebaseHelper.findStudentById(str(index))

        if not student:
            print(row)
            new_student_ref = db.collection(u'students').document(indexStudent)

            new_student_ref.set({
                header[0]: row[0],
                header[1]: row[1],
                header[2]: row[2]
            })
        else:
            if((student['Name'] != row[1]) or (student['Class'] != row[2])):
                new_student_ref = db.collection(
                    u'students').document(indexStudent)

                new_student_ref.set({
                    header[0]: row[0],
                    header[1]: row[1],
                    header[2]: row[2]
                })


createStudent()
