import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import firebaseHelper



def createClass():
    db = firestore.client()
    file = open("classes.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)

    index = 0
    for row in rows:
        index += 1
        print(row)
        indexStudent = "Class" + str(index)

        new_class_ref = db.collection(
            u'classes').document(indexStudent)
        doc = new_class_ref.get()

        if not doc.exists:
            new_class_ref.set({
                header[0]: row[0],
                header[1]: row[1],
                header[2]: row[2]
            })


createClass()
