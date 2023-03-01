
import firebase_admin
from firebase_admin import credentials
import sys

def initConnectFirebase():
  cred = credentials.Certificate("serviceAccountKey.json")
  firebase_admin.initialize_app(cred)
  print("Connect Firebase Success")

sys.modules[__name__] = initConnectFirebase
