import os
import json
from firebase_admin import credentials

firebase_config = json.loads(os.environ.get("FIREBASE_CONFIG"))

cred = credentials.Certificate(firebase_config)